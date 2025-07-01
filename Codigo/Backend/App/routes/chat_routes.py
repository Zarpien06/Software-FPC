# app/routes/chat_routes.py
from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, WebSocketDisconnect, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import Optional, List, Dict
import json
import uuid
from datetime import datetime
import logging

from app.database import get_db
from app.auth.auth_handler import get_current_user, decode_token
from app.controllers.chat_controller import ChatController
from app.schemas.chat import (
    ChatCreate, ChatUpdate, ChatResponse, ChatDetalle, ChatListResponse,
    MensajeChatCreate, MensajeChatUpdate, MensajeChatResponse, MensajeListResponse,
    ChatFiltros, MensajeFiltros, ChatEstadisticas, MensajeWebSocket,
    ConexionChatCreate, ConexionChatResponse
)
from app.schemas.user import UserResponse

router = APIRouter(prefix="/api/v1/chat", tags=["Chat en Vivo"])
security = HTTPBearer()
logger = logging.getLogger(__name__)

# Manager para conexiones WebSocket
class ConnectionManager:
    def __init__(self):
        # Diccionario para almacenar conexiones activas por chat_id
        self.active_connections: Dict[int, List[Dict]] = {}
        # Diccionario para mapear websockets a información de usuario
        self.connection_info: Dict[WebSocket, Dict] = {}

    async def connect(self, websocket: WebSocket, chat_id: int, user_id: int, user_name: str):
        """Conectar un usuario a un chat específico"""
        await websocket.accept()
        
        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = []
        
        connection_data = {
            "websocket": websocket,
            "user_id": user_id,
            "user_name": user_name,
            "connected_at": datetime.now()
        }
        
        self.active_connections[chat_id].append(connection_data)
        self.connection_info[websocket] = {
            "chat_id": chat_id,
            "user_id": user_id,
            "user_name": user_name
        }
        
        logger.info(f"Usuario {user_name} conectado al chat {chat_id}")
        
        # Notificar a otros usuarios que alguien se conectó
        await self.broadcast_to_chat(chat_id, {
            "tipo": "user_connected",
            "user_id": user_id,
            "user_name": user_name,
            "timestamp": datetime.now().isoformat()
        }, exclude_user=user_id)

    def disconnect(self, websocket: WebSocket):
        """Desconectar un usuario"""
        if websocket in self.connection_info:
            info = self.connection_info[websocket]
            chat_id = info["chat_id"]
            user_id = info["user_id"]
            user_name = info["user_name"]
            
            # Remover de active_connections
            if chat_id in self.active_connections:
                self.active_connections[chat_id] = [
                    conn for conn in self.active_connections[chat_id] 
                    if conn["websocket"] != websocket
                ]
                
                # Si no hay más conexiones en este chat, remover el chat
                if not self.active_connections[chat_id]:
                    del self.active_connections[chat_id]
            
            # Remover de connection_info
            del self.connection_info[websocket]
            
            logger.info(f"Usuario {user_name} desconectado del chat {chat_id}")
            
            # Notificar a otros usuarios que alguien se desconectó
            # Esto se hace en el except del websocket endpoint

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Enviar mensaje personal a una conexión específica"""
        try:
            await websocket.send_text(json.dumps(message, default=str))
        except Exception as e:
            logger.error(f"Error enviando mensaje personal: {e}")

    async def broadcast_to_chat(self, chat_id: int, message: dict, exclude_user: Optional[int] = None):
        """Enviar mensaje a todos los usuarios conectados a un chat específico"""
        if chat_id not in self.active_connections:
            return
        
        disconnected_connections = []
        
        for connection_data in self.active_connections[chat_id]:
            # Excluir usuario si se especifica
            if exclude_user and connection_data["user_id"] == exclude_user:
                continue
                
            try:
                await connection_data["websocket"].send_text(json.dumps(message, default=str))
            except Exception as e:
                logger.error(f"Error broadcasting a chat {chat_id}: {e}")
                disconnected_connections.append(connection_data)
        
        # Limpiar conexiones desconectadas
        for disconnected in disconnected_connections:
            self.active_connections[chat_id].remove(disconnected)
            if disconnected["websocket"] in self.connection_info:
                del self.connection_info[disconnected["websocket"]]

    def get_chat_users(self, chat_id: int) -> List[Dict]:
        """Obtener usuarios activos en un chat"""
        if chat_id not in self.active_connections:
            return []
        
        return [
            {
                "user_id": conn["user_id"],
                "user_name": conn["user_name"],
                "connected_at": conn["connected_at"]
            }
            for conn in self.active_connections[chat_id]
        ]

# Instancia global del manager
manager = ConnectionManager()

# ========================= ENDPOINTS REST API =========================

@router.post("/", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
async def crear_chat(
    chat_data: ChatCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Crear un nuevo chat para un proceso"""
    try:
        chat_controller = ChatController(db)
        nuevo_chat = await chat_controller.crear_chat(chat_data, current_user.id)
        return nuevo_chat
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error creando chat: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.get("/", response_model=ChatListResponse)
async def listar_chats(
    page: int = Query(1, ge=1, description="Número de página"),
    per_page: int = Query(20, ge=1, le=100, description="Elementos por página"),
    proceso_id: Optional[int] = Query(None, description="Filtrar por proceso"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    buscar: Optional[str] = Query(None, description="Buscar en título"),
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Listar chats con filtros y paginación"""
    try:
        filtros = ChatFiltros(
            proceso_id=proceso_id,
            activo=activo,
            buscar=buscar
        )
        
        chat_controller = ChatController(db)
        resultado = await chat_controller.listar_chats(
            filtros=filtros,
            user_id=current_user.id,
            user_role=current_user.role_name,
            page=page,
            per_page=per_page
        )
        return resultado
    except Exception as e:
        logger.error(f"Error listando chats: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.get("/{chat_id}", response_model=ChatDetalle)
async def obtener_chat(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Obtener detalles de un chat específico"""
    try:
        chat_controller = ChatController(db)
        chat = await chat_controller.obtener_chat_detalle(chat_id, current_user.id, current_user.role_name)
        if not chat:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat no encontrado")
        return chat
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo chat {chat_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.put("/{chat_id}", response_model=ChatResponse)
async def actualizar_chat(
    chat_id: int,
    chat_data: ChatUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Actualizar información de un chat"""
    try:
        chat_controller = ChatController(db)
        chat_actualizado = await chat_controller.actualizar_chat(chat_id, chat_data, current_user.id, current_user.role_name)
        if not chat_actualizado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat no encontrado")
        return chat_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error actualizando chat {chat_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_chat(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Eliminar un chat (solo administradores)"""
    try:
        chat_controller = ChatController(db)
        eliminado = await chat_controller.eliminar_chat(chat_id, current_user.id, current_user.role_name)
        if not eliminado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat no encontrado")
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        logger.error(f"Error eliminando chat {chat_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

# ========================= ENDPOINTS DE MENSAJES =========================

@router.post("/{chat_id}/mensajes", response_model=MensajeChatResponse, status_code=status.HTTP_201_CREATED)
async def enviar_mensaje(
    chat_id: int,
    mensaje_data: MensajeChatCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Enviar un mensaje a un chat"""
    try:
        # Validar que el chat_id coincida
        if mensaje_data.chat_id != chat_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID de chat no coincide")
        
        chat_controller = ChatController(db)
        nuevo_mensaje = await chat_controller.enviar_mensaje(mensaje_data, current_user.id)
        
        # Broadcast del mensaje a todos los usuarios conectados al chat
        mensaje_websocket = {
            "tipo": "nuevo_mensaje",
            "chat_id": chat_id,
            "mensaje": {
                "id": nuevo_mensaje.id,
                "contenido": nuevo_mensaje.contenido,
                "tipo_mensaje": nuevo_mensaje.tipo_mensaje,
                "remitente_id": nuevo_mensaje.remitente_id,
                "remitente_nombre": nuevo_mensaje.remitente_nombre,
                "created_at": nuevo_mensaje.created_at.isoformat(),
                "archivo_url": nuevo_mensaje.archivo_url,
                "respuesta_a": nuevo_mensaje.respuesta_a
            },
            "timestamp": datetime.now().isoformat()
        }
        
        await manager.broadcast_to_chat(chat_id, mensaje_websocket, exclude_user=current_user.id)
        
        return nuevo_mensaje
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error enviando mensaje: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.get("/{chat_id}/mensajes", response_model=MensajeListResponse)
async def listar_mensajes(
    chat_id: int,
    page: int = Query(1, ge=1, description="Número de página"),
    per_page: int = Query(50, ge=1, le=100, description="Elementos por página"),
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Listar mensajes de un chat con paginación"""
    try:
        chat_controller = ChatController(db)
        resultado = await chat_controller.listar_mensajes(
            chat_id=chat_id,
            user_id=current_user.id,
            user_role=current_user.role_name,
            page=page,
            per_page=per_page
        )
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        logger.error(f"Error listando mensajes del chat {chat_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.put("/mensajes/{mensaje_id}", response_model=MensajeChatResponse)
async def actualizar_mensaje(
    mensaje_id: int,
    mensaje_data: MensajeChatUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Actualizar un mensaje (solo el remitente puede editar contenido)"""
    try:
        chat_controller = ChatController(db)
        mensaje_actualizado = await chat_controller.actualizar_mensaje(mensaje_id, mensaje_data, current_user.id)
        if not mensaje_actualizado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mensaje no encontrado")
        
        # Broadcast de actualización de mensaje
        if mensaje_data.contenido:  # Solo si se actualizó el contenido
            mensaje_websocket = {
                "tipo": "mensaje_actualizado",
                "chat_id": mensaje_actualizado.chat_id,
                "mensaje_id": mensaje_id,
                "nuevo_contenido": mensaje_actualizado.contenido,
                "timestamp": datetime.now().isoformat()
            }
            await manager.broadcast_to_chat(mensaje_actualizado.chat_id, mensaje_websocket)
        
        return mensaje_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        logger.error(f"Error actualizando mensaje {mensaje_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.post("/mensajes/{mensaje_id}/marcar-leido", status_code=status.HTTP_200_OK)
async def marcar_mensaje_leido(
    mensaje_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Marcar un mensaje como leído"""
    try:
        chat_controller = ChatController(db)
        marcado = await chat_controller.marcar_mensaje_leido(mensaje_id, current_user.id)
        if not marcado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mensaje no encontrado")
        
        return {"message": "Mensaje marcado como leído"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error marcando mensaje {mensaje_id} como leído: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

# ========================= ENDPOINTS DE ESTADÍSTICAS =========================

@router.get("/estadisticas/generales", response_model=ChatEstadisticas)
async def obtener_estadisticas(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Obtener estadísticas generales del sistema de chat"""
    try:
        chat_controller = ChatController(db)
        estadisticas = await chat_controller.obtener_estadisticas(current_user.id, current_user.role_name)
        
        # Agregar usuarios conectados desde el manager
        total_conectados = sum(len(connections) for connections in manager.active_connections.values())
        estadisticas.usuarios_conectados = total_conectados
        
        return estadisticas
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

@router.get("/{chat_id}/participantes", response_model=List[dict])
async def obtener_participantes_activos(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    """Obtener usuarios actualmente conectados a un chat"""
    try:
        # Verificar acceso al chat
        chat_controller = ChatController(db)
        chat = await chat_controller.obtener_chat_detalle(chat_id, current_user.id, current_user.role_name)
        if not chat:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat no encontrado")
        
        participantes = manager.get_chat_users(chat_id)
        return participantes
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo participantes del chat {chat_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

# ========================= WEBSOCKET ENDPOINT =========================

@router.websocket("/{chat_id}/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    chat_id: int,
    token: str = Query(..., description="JWT Token para autenticación"),
    db: Session = Depends(get_db)
):
    """WebSocket endpoint para chat en tiempo real"""
    try:
        # Verificar token JWT
        try:
            payload = decode_token(token)
            user_id = payload.get("user_id")
            if not user_id:
                await websocket.close(code=4001, reason="Token inválido")
                return
        except Exception:
            await websocket.close(code=4001, reason="Token inválido")
            return
        
        # Verificar acceso al chat
        chat_controller = ChatController(db)
        user_info = await chat_controller.verificar_acceso_chat(chat_id, user_id)
        if not user_info:
            await websocket.close(code=4003, reason="Acceso denegado al chat")
            return
        
        # Conectar usuario
        await manager.connect(websocket, chat_id, user_id, user_info["nombre"])
        
        try:
            while True:
                # Escuchar mensajes del cliente
                data = await websocket.receive_text()
                message_data = json.loads(data)
                
                # Procesar diferentes tipos de mensajes
                if message_data.get("tipo") == "typing":
                    # Usuario está escribiendo
                    typing_message = {
                        "tipo": "user_typing",
                        "chat_id": chat_id,
                        "user_id": user_id,
                        "user_name": user_info["nombre"],
                        "timestamp": datetime.now().isoformat()
                    }
                    await manager.broadcast_to_chat(chat_id, typing_message, exclude_user=user_id)
                
                elif message_data.get("tipo") == "stop_typing":
                    # Usuario dejó de escribir
                    stop_typing_message = {
                        "tipo": "user_stop_typing",
                        "chat_id": chat_id,
                        "user_id": user_id,
                        "timestamp": datetime.now().isoformat()
                    }
                    await manager.broadcast_to_chat(chat_id, stop_typing_message, exclude_user=user_id)
                
                elif message_data.get("tipo") == "ping":
                    # Ping para mantener conexión viva
                    await manager.send_personal_message({
                        "tipo": "pong",
                        "timestamp": datetime.now().isoformat()
                    }, websocket)
                
        except WebSocketDisconnect:
            pass
        except Exception as e:
            logger.error(f"Error en WebSocket para chat {chat_id}: {e}")
        finally:
            # Limpiar conexión
            info = manager.connection_info.get(websocket)
            manager.disconnect(websocket)
            
            # Notificar desconexión si teníamos información del usuario
            if info:
                disconnect_message = {
                    "tipo": "user_disconnected",
                    "user_id": info["user_id"],
                    "user_name": info["user_name"],
                    "timestamp": datetime.now().isoformat()
                }
                await manager.broadcast_to_chat(chat_id, disconnect_message)
                
    except Exception as e:
        logger.error(f"Error general en WebSocket: {e}")
        try:
            await websocket.close(code=4000, reason="Error interno del servidor")
        except:
            pass