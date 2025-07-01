# app/services/websocket_service.py
import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set
from fastapi import WebSocket, WebSocketDisconnect
import redis.asyncio as redis
from app.config import settings

logger = logging.getLogger(__name__)

class WebSocketManager:
    """Gestor avanzado de conexiones WebSocket con soporte para Redis"""
    
    def __init__(self, redis_url: Optional[str] = None):
        # Conexiones locales
        self.active_connections: Dict[int, List[Dict]] = {}
        self.connection_info: Dict[WebSocket, Dict] = {}
        
        # Redis para escalabilidad (opcional)
        self.redis_client = None
        if redis_url:
            self.redis_client = redis.from_url(redis_url)
        
        # Tareas de limpieza
        self.cleanup_tasks: Set[asyncio.Task] = set()
        
        # Configuración
        self.heartbeat_interval = 30  # segundos
        self.connection_timeout = 300  # 5 minutos
        
    async def initialize(self):
        """Inicializar el servicio WebSocket"""
        if self.redis_client:
            try:
                await self.redis_client.ping()
                logger.info("Conectado a Redis para WebSocket")
            except Exception as e:
                logger.warning(f"No se pudo conectar a Redis: {e}")
                self.redis_client = None
        
        # Iniciar tarea de limpieza
        cleanup_task = asyncio.create_task(self._cleanup_connections())
        self.cleanup_tasks.add(cleanup_task)
        
    async def shutdown(self):
        """Cerrar todas las conexiones y limpiar recursos"""
        # Cancelar tareas de limpieza
        for task in self.cleanup_tasks:
            task.cancel()
        
        # Cerrar todas las conexiones WebSocket
        for chat_id, connections in self.active_connections.items():
            for conn_data in connections:
                try:
                    await conn_data["websocket"].close()
                except:
                    pass
        
        # Cerrar Redis
        if self.redis_client:
            await self.redis_client.close()
            
    async def connect(self, websocket: WebSocket, chat_id: int, user_id: int, user_data: Dict):
        """Conectar un usuario a un chat específico"""
        await websocket.accept()
        
        # Preparar datos de conexión
        connection_data = {
            "websocket": websocket,
            "user_id": user_id,
            "user_name": user_data.get("nombre", "Usuario"),
            "user_role": user_data.get("role", "cliente"),
            "connected_at": datetime.now(),
            "last_activity": datetime.now(),
            "is_active": True
        }
        
        # Agregar a conexiones locales
        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = []
        
        self.active_connections[chat_id].append(connection_data)
        
        # Mapear websocket a información
        self.connection_info[websocket] = {
            "chat_id": chat_id,
            "user_id": user_id,
            "user_name": user_data.get("nombre", "Usuario"),
            "user_role": user_data.get("role", "cliente"),
            "connected_at": datetime.now()
        }
        
        logger.info(f"Usuario {user_data.get('nombre')} conectado al chat {chat_id}")
        
        # Publicar conexión en Redis (si está disponible)
        if self.redis_client:
            await self._publish_redis_event({
                "tipo": "user_connected",
                "chat_id": chat_id,
                "user_id": user_id,
                "user_name": user_data.get("nombre"),
                "timestamp": datetime.now().isoformat()
            })
        
        # Notificar a otros usuarios
        await self.broadcast_to_chat(chat_id, {
            "tipo": "user_connected",
            "user_id": user_id,
            "user_name": user_data.get("nombre"),
            "user_role": user_data.get("role"),
            "timestamp": datetime.now().isoformat()
        }, exclude_user=user_id)
        
        # Enviar lista de usuarios activos al recién conectado
        active_users = self.get_chat_users(chat_id)
        await self.send_personal_message({
            "tipo": "active_users",
            "usuarios": active_users,
            "timestamp": datetime.now().isoformat()
        }, websocket)
        
    async def disconnect(self, websocket: WebSocket, reason: str = "normal"):
        """Desconectar un usuario"""
        if websocket not in self.connection_info:
            return
            
        info = self.connection_info[websocket]
        chat_id = info["chat_id"]
        user_id = info["user_id"]
        user_name = info["user_name"]
        
        # Remover de conexiones activas
        if chat_id in self.active_connections:
            self.active_connections[chat_id] = [
                conn for conn in self.active_connections[chat_id] 
                if conn["websocket"] != websocket
            ]
            
            # Limpiar chat vacío
            if not self.active_connections[chat_id]:
                del self.active_connections[chat_id]
        
        # Remover mapeo
        del self.connection_info[websocket]
        
        logger.info(f"Usuario {user_name} desconectado del chat {chat_id} - Razón: {reason}")
        
        # Publicar desconexión en Redis
        if self.redis_client:
            await self._publish_redis_event({
                "tipo": "user_disconnected",
                "chat_id": chat_id,
                "user_id": user_id,
                "user_name": user_name,
                "reason": reason,
                "timestamp": datetime.now().isoformat()
            })
        
        # Notificar a otros usuarios
        await self.broadcast_to_chat(chat_id, {
            "tipo": "user_disconnected",
            "user_id": user_id,
            "user_name": user_name,
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        })
        
    async def send_personal_message(self, message: Dict, websocket: WebSocket):
        """Enviar mensaje personal a una conexión específica"""
        try:
            await websocket.send_text(json.dumps(message, default=str))
            
            # Actualizar última actividad
            if websocket in self.connection_info:
                # Buscar y actualizar en active_connections
                info = self.connection_info[websocket]
                chat_id = info["chat_id"]
                
                if chat_id in self.active_connections:
                    for conn in self.active_connections[chat_id]:
                        if conn["websocket"] == websocket:
                            conn["last_activity"] = datetime.now()
                            break
                            
        except Exception as e:
            logger.error(f"Error enviando mensaje personal: {e}")
            await self.disconnect(websocket, "error_sending")
            
    async def broadcast_to_chat(self, chat_id: int, message: Dict, exclude_user: Optional[int] = None):
        """Enviar mensaje a todos los usuarios de un chat"""
        if chat_id not in self.active_connections:
            return
            
        # Preparar mensaje
        message_str = json.dumps(message, default=str)
        
        # Lista de conexiones a remover (conexiones rotas)
        broken_connections = []
        
        for conn_data in self.active_connections[chat_id]:
            # Excluir usuario si se especifica
            if exclude_user and conn_data["user_id"] == exclude_user:
                continue
                
            try:
                await conn_data["websocket"].send_text(message_str)
                # Actualizar última actividad
                conn_data["last_activity"] = datetime.now()
                
            except Exception as e:
                logger.warning(f"Conexión rota detectada: {e}")
                broken_connections.append(conn_data["websocket"])
        
        # Limpiar conexiones rotas
        for broken_ws in broken_connections:
            await self.disconnect(broken_ws, "connection_broken")
            
    async def broadcast_to_user(self, user_id: int, message: Dict):
        """Enviar mensaje a todas las conexiones de un usuario específico"""
        message_str = json.dumps(message, default=str)
        broken_connections = []
        
        for chat_id, connections in self.active_connections.items():
            for conn_data in connections:
                if conn_data["user_id"] == user_id:
                    try:
                        await conn_data["websocket"].send_text(message_str)
                        conn_data["last_activity"] = datetime.now()
                    except Exception as e:
                        logger.warning(f"Conexión rota para usuario {user_id}: {e}")
                        broken_connections.append(conn_data["websocket"])
        
        # Limpiar conexiones rotas
        for broken_ws in broken_connections:
            await self.disconnect(broken_ws, "connection_broken")
            
    def get_chat_users(self, chat_id: int) -> List[Dict]:
        """Obtener lista de usuarios activos en un chat"""
        if chat_id not in self.active_connections:
            return []
            
        users = []
        for conn_data in self.active_connections[chat_id]:
            users.append({
                "user_id": conn_data["user_id"],
                "user_name": conn_data["user_name"],
                "user_role": conn_data["user_role"],
                "connected_at": conn_data["connected_at"].isoformat(),
                "last_activity": conn_data["last_activity"].isoformat(),
                "is_active": conn_data["is_active"]
            })
        
        return users
        
    def get_connection_stats(self) -> Dict:
        """Obtener estadísticas de conexiones"""
        total_connections = sum(len(conns) for conns in self.active_connections.values())
        active_chats = len(self.active_connections)
        
        return {
            "total_connections": total_connections,
            "active_chats": active_chats,
            "chats": {
                chat_id: len(conns) 
                for chat_id, conns in self.active_connections.items()
            }
        }
        
    async def handle_websocket_message(self, websocket: WebSocket, message: str):
        """Manejar mensajes recibidos vía WebSocket"""
        try:
            data = json.loads(message)
            message_type = data.get("tipo")
            
            if websocket not in self.connection_info:
                await websocket.send_text(json.dumps({
                    "tipo": "error",
                    "mensaje": "Conexión no autorizada"
                }))
                return
                
            info = self.connection_info[websocket]
            chat_id = info["chat_id"]
            user_id = info["user_id"]
            
            # Manejar diferentes tipos de mensajes
            if message_type == "ping":
                await self.send_personal_message({
                    "tipo": "pong",
                    "timestamp": datetime.now().isoformat()
                }, websocket)
                
            elif message_type == "typing":
                await self.broadcast_to_chat(chat_id, {
                    "tipo": "user_typing",
                    "user_id": user_id,
                    "user_name": info["user_name"],
                    "timestamp": datetime.now().isoformat()
                }, exclude_user=user_id)
                
            elif message_type == "stop_typing":
                await self.broadcast_to_chat(chat_id, {
                    "tipo": "user_stop_typing",
                    "user_id": user_id,
                    "user_name": info["user_name"],
                    "timestamp": datetime.now().isoformat()
                }, exclude_user=user_id)
                
            elif message_type == "message_read":
                mensaje_id = data.get("mensaje_id")
                if mensaje_id:
                    await self.broadcast_to_chat(chat_id, {
                        "tipo": "message_read",
                        "mensaje_id": mensaje_id,
                        "user_id": user_id,
                        "timestamp": datetime.now().isoformat()
                    }, exclude_user=user_id)
                    
        except json.JSONDecodeError:
            await websocket.send_text(json.dumps({
                "tipo": "error",
                "mensaje": "Formato de mensaje inválido"
            }))
        except Exception as e:
            logger.error(f"Error manejando mensaje WebSocket: {e}")
            await websocket.send_text(json.dumps({
                "tipo": "error",
                "mensaje": "Error interno del servidor"
            }))
            
    async def _cleanup_connections(self):
        """Tarea de limpieza de conexiones inactivas"""
        while True:
            try:
                await asyncio.sleep(60)  # Ejecutar cada minuto
                
                current_time = datetime.now()
                expired_connections = []
                
                for chat_id, connections in self.active_connections.items():
                    for conn_data in connections:
                        # Verificar timeout
                        time_diff = current_time - conn_data["last_activity"]
                        if time_diff.total_seconds() > self.connection_timeout:
                            expired_connections.append(conn_data["websocket"])
                
                # Desconectar conexiones expiradas
                for expired_ws in expired_connections:
                    await self.disconnect(expired_ws, "timeout")
                    
                if expired_connections:
                    logger.info(f"Limpiadas {len(expired_connections)} conexiones expiradas")
                    
            except Exception as e:
                logger.error(f"Error en limpieza de conexiones: {e}")
                
    async def _publish_redis_event(self, event: Dict):
        """Publicar evento en Redis para escalabilidad"""
        if not self.redis_client:
            return
            
        try:
            channel = f"chat:events:{event.get('chat_id', 'global')}"
            await self.redis_client.publish(channel, json.dumps(event, default=str))
        except Exception as e:
            logger.error(f"Error publicando evento Redis: {e}")
            
    async def send_notification_message(self, chat_id: int, message: str, notification_type: str = "info"):
        """Enviar mensaje de notificación del sistema"""
        await self.broadcast_to_chat(chat_id, {
            "tipo": "system_notification",
            "mensaje": message,
            "notification_type": notification_type,
            "timestamp": datetime.now().isoformat()
        })

# Instancia global del gestor WebSocket
websocket_manager = WebSocketManager(
    redis_url=getattr(settings, 'REDIS_URL', None)
)