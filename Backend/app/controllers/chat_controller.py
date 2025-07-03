# app/controllers/chat_controller.py
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func, desc
from fastapi import HTTPException, status
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from app.models.chat import Chat, MensajeChat, ConexionChat, TipoMensaje, EstadoMensaje
from app.models.user import Usuario
from app.models.proceso import Proceso
from app.schemas.chat import (
    ChatCreate, ChatUpdate, ChatResponse, ChatFiltros,
    MensajeChatCreate, MensajeChatUpdate, MensajeChatResponse, MensajeFiltros,
    ConexionChatCreate, ChatEstadisticas, ChatDetalle
)

class ChatController:
    """Controlador para gestión de chats y mensajes"""
    
    @staticmethod
    def crear_chat(db: Session, chat_data: ChatCreate, cliente_id: int) -> ChatResponse:
        """Crear nuevo chat para un proceso"""
        try:
            # Verificar que el proceso existe
            proceso = db.query(Proceso).filter(Proceso.id == chat_data.proceso_id).first()
            if not proceso:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Proceso no encontrado"
                )
            
            # Verificar que no existe un chat activo para este proceso
            chat_existente = db.query(Chat).filter(
                and_(
                    Chat.proceso_id == chat_data.proceso_id,
                    Chat.activo == True
                )
            ).first()
            
            if chat_existente:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe un chat activo para este proceso"
                )
            
            # Verificar mecánico si se proporciona
            if chat_data.mecanico_id:
                mecanico = db.query(Usuario).filter(
                    and_(
                        Usuario.id == chat_data.mecanico_id,
                        Usuario.rol.has(nombre="Empleado")
                    )
                ).first()
                if not mecanico:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Mecánico no encontrado"
                    )
            
            # Crear el chat
            nuevo_chat = Chat(
                proceso_id=chat_data.proceso_id,
                cliente_id=cliente_id,
                mecanico_id=chat_data.mecanico_id,
                titulo=chat_data.titulo
            )
            
            db.add(nuevo_chat)
            db.commit()
            db.refresh(nuevo_chat)
            
            # Crear mensaje de bienvenida automático
            mensaje_bienvenida = MensajeChat(
                chat_id=nuevo_chat.id,
                remitente_id=cliente_id,
                contenido=f"Chat iniciado para el proceso: {proceso.descripcion}",
                tipo_mensaje=TipoMensaje.NOTIFICACION
            )
            db.add(mensaje_bienvenida)
            db.commit()
            
            return ChatController._construir_chat_response(db, nuevo_chat)
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear chat: {str(e)}"
            )
    
    @staticmethod
    def obtener_chats(
        db: Session, 
        filtros: ChatFiltros, 
        usuario_id: int,
        es_admin: bool = False,
        page: int = 1, 
        per_page: int = 20
    ) -> Dict[str, Any]:
        """Obtener lista de chats con filtros"""
        try:
            query = db.query(Chat).options(
                joinedload(Chat.cliente),
                joinedload(Chat.mecanico),
                joinedload(Chat.proceso)
            )
            
            # Filtros de seguridad: solo mostrar chats donde el usuario participa
            if not es_admin:
                query = query.filter(
                    or_(
                        Chat.cliente_id == usuario_id,
                        Chat.mecanico_id == usuario_id
                    )
                )
            
            # Aplicar filtros
            if filtros.proceso_id:
                query = query.filter(Chat.proceso_id == filtros.proceso_id)
            
            if filtros.cliente_id:
                query = query.filter(Chat.cliente_id == filtros.cliente_id)
                
            if filtros.mecanico_id:
                query = query.filter(Chat.mecanico_id == filtros.mecanico_id)
                
            if filtros.activo is not None:
                query = query.filter(Chat.activo == filtros.activo)
                
            if filtros.fecha_desde:
                query = query.filter(Chat.created_at >= filtros.fecha_desde)
                
            if filtros.fecha_hasta:
                query = query.filter(Chat.created_at <= filtros.fecha_hasta)
                
            if filtros.buscar:
                query = query.filter(
                    or_(
                        Chat.titulo.ilike(f"%{filtros.buscar}%"),
                        Chat.proceso.has(Proceso.descripcion.ilike(f"%{filtros.buscar}%"))
                    )
                )
            
            # Ordenar por última actividad
            query = query.order_by(desc(Chat.updated_at))
            
            # Paginación
            total = query.count()
            chats = query.offset((page - 1) * per_page).limit(per_page).all()
            
            # Construir respuesta
            chats_response = []
            for chat in chats:
                chat_resp = ChatController._construir_chat_response(db, chat)
                chats_response.append(chat_resp)
            
            return {
                "chats": chats_response,
                "total": total,
                "page": page,
                "per_page": per_page,
                "total_pages": (total + per_page - 1) // per_page
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener chats: {str(e)}"
            )
    
    @staticmethod
    def obtener_chat_detalle(db: Session, chat_id: int, usuario_id: int, es_admin: bool = False) -> ChatDetalle:
        """Obtener detalle completo de un chat"""
        try:
            query = db.query(Chat).options(
                joinedload(Chat.cliente),
                joinedload(Chat.mecanico),
                joinedload(Chat.proceso),
                joinedload(Chat.mensajes).joinedload(MensajeChat.remitente)
            )
            
            # Verificar acceso
            if not es_admin:
                query = query.filter(
                    and_(
                        Chat.id == chat_id,
                        or_(
                            Chat.cliente_id == usuario_id,
                            Chat.mecanico_id == usuario_id
                        )
                    )
                )
            else:
                query = query.filter(Chat.id == chat_id)
            
            chat = query.first()
            if not chat:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Chat no encontrado"
                )
            
            # Construir respuesta detallada
            chat_response = ChatController._construir_chat_response(db, chat)
            
            # Obtener mensajes recientes (últimos 50)
            mensajes_recientes = db.query(MensajeChat).filter(
                MensajeChat.chat_id == chat_id
            ).options(
                joinedload(MensajeChat.remitente)
            ).order_by(desc(MensajeChat.created_at)).limit(50).all()
            
            mensajes_resp = []
            for mensaje in reversed(mensajes_recientes):  # Ordenar cronológicamente
                mensaje_resp = ChatController._construir_mensaje_response(mensaje)
                mensajes_resp.append(mensaje_resp)
            
            # Obtener participantes activos
            participantes = ChatController._obtener_participantes_activos(db, chat_id)
            
            return ChatDetalle(
                **chat_response.dict(),
                mensajes_recientes=mensajes_resp,
                participantes_activos=participantes
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener detalle del chat: {str(e)}"
            )
    
    @staticmethod
    def actualizar_chat(db: Session, chat_id: int, chat_data: ChatUpdate, usuario_id: int, es_admin: bool = False) -> ChatResponse:
        """Actualizar información del chat"""
        try:
            # Buscar el chat
            query = db.query(Chat)
            if not es_admin:
                query = query.filter(
                    or_(
                        Chat.cliente_id == usuario_id,
                        Chat.mecanico_id == usuario_id
                    )
                )
            
            chat = query.filter(Chat.id == chat_id).first()
            if not chat:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Chat no encontrado"
                )
            
            # Actualizar campos
            if chat_data.titulo is not None:
                chat.titulo = chat_data.titulo
            
            if chat_data.mecanico_id is not None:
                # Verificar que el mecánico existe
                if chat_data.mecanico_id > 0:
                    mecanico = db.query(Usuario).filter(
                        and_(
                            Usuario.id == chat_data.mecanico_id,
                            Usuario.rol.has(nombre="Empleado")
                        )
                    ).first()
                    if not mecanico:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail="Mecánico no encontrado"
                        )
                chat.mecanico_id = chat_data.mecanico_id
            
            if chat_data.activo is not None:
                chat.activo = chat_data.activo
            
            chat.updated_at = datetime.now()
            db.commit()
            db.refresh(chat)
            
            return ChatController._construir_chat_response(db, chat)
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar chat: {str(e)}"
            )
    
    @staticmethod
    def eliminar_chat(db: Session, chat_id: int, usuario_id: int, es_admin: bool = False) -> bool:
        """Eliminar chat (soft delete)"""
        try:
            query = db.query(Chat)
            if not es_admin:
                query = query.filter(Chat.cliente_id == usuario_id)
            
            chat = query.filter(Chat.id == chat_id).first()
            if not chat:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Chat no encontrado"
                )
            
            # Soft delete
            chat.activo = False
            chat.updated_at = datetime.now()
            db.commit()
            
            return True
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al eliminar chat: {str(e)}"
            )
    
    # Métodos para mensajes
    @staticmethod
    def enviar_mensaje(db: Session, mensaje_data: MensajeChatCreate, remitente_id: int) -> MensajeChatResponse:
        """Enviar nuevo mensaje en el chat"""
        try:
            # Verificar que el chat existe y el usuario tiene acceso
            chat = db.query(Chat).filter(
                and_(
                    Chat.id == mensaje_data.chat_id,
                    Chat.activo == True,
                    or_(
                        Chat.cliente_id == remitente_id,
                        Chat.mecanico_id == remitente_id
                    )
                )
            ).first()
            
            if not chat:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Chat no encontrado o sin acceso"
                )
            
            # Crear el mensaje
            nuevo_mensaje = MensajeChat(
                chat_id=mensaje_data.chat_id,
                remitente_id=remitente_id,
                contenido=mensaje_data.contenido,
                tipo_mensaje=mensaje_data.tipo_mensaje,
                archivo_url=mensaje_data.archivo_url,
                respuesta_a=mensaje_data.respuesta_a
            )
            
            db.add(nuevo_mensaje)
            
            # Actualizar timestamp del chat
            chat.updated_at = datetime.now()
            
            db.commit()
            db.refresh(nuevo_mensaje)
            
            return ChatController._construir_mensaje_response(nuevo_mensaje)
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al enviar mensaje: {str(e)}"
            )
    
    @staticmethod
    def obtener_mensajes(
        db: Session, 
        chat_id: int, 
        usuario_id: int, 
        page: int = 1, 
        per_page: int = 50,
        es_admin: bool = False
    ) -> Dict[str, Any]:
        """Obtener mensajes de un chat con paginación"""
        try:
            # Verificar acceso al chat
            chat_query = db.query(Chat)
            if not es_admin:
                chat_query = chat_query.filter(
                    or_(
                        Chat.cliente_id == usuario_id,
                        Chat.mecanico_id == usuario_id
                    )
                )
            
            chat = chat_query.filter(Chat.id == chat_id).first()
            if not chat:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Chat no encontrado"
                )
            
            # Obtener mensajes
            query = db.query(MensajeChat).filter(
                MensajeChat.chat_id == chat_id
            ).options(
                joinedload(MensajeChat.remitente)
            ).order_by(desc(MensajeChat.created_at))
            
            total = query.count()
            mensajes = query.offset((page - 1) * per_page).limit(per_page).all()
            
            # Construir respuesta
            mensajes_response = []
            for mensaje in reversed(mensajes):  # Ordenar cronológicamente
                mensaje_resp = ChatController._construir_mensaje_response(mensaje)
                mensajes_response.append(mensaje_resp)
            
            return {
                "mensajes": mensajes_response,
                "total": total,
                "page": page,
                "per_page": per_page,
                "total_pages": (total + per_page - 1) // per_page
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener mensajes: {str(e)}"
            )
    
    @staticmethod
    def marcar_mensajes_como_leidos(db: Session, chat_id: int, usuario_id: int) -> bool:
        """Marcar todos los mensajes no leídos como leídos"""
        try:
            # Verificar acceso al chat
            chat = db.query(Chat).filter(
                and_(
                    Chat.id == chat_id,
                    or_(
                        Chat.cliente_id == usuario_id,
                        Chat.mecanico_id == usuario_id
                    )
                )
            ).first()
            
            if not chat:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Chat no encontrado"
                )
            
            # Marcar mensajes como leídos (excepto los propios)
            db.query(MensajeChat).filter(
                and_(
                    MensajeChat.chat_id == chat_id,
                    MensajeChat.remitente_id != usuario_id,
                    MensajeChat.estado != EstadoMensaje.LEIDO
                )
            ).update({
                MensajeChat.estado: EstadoMensaje.LEIDO,
                MensajeChat.leido_at: datetime.now()
            })
            
            db.commit()
            return True
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al marcar mensajes como leídos: {str(e)}"
            )
    
    @staticmethod
    def obtener_estadisticas_chat(db: Session, usuario_id: int, es_admin: bool = False) -> ChatEstadisticas:
        """Obtener estadísticas generales del chat"""
        try:
            # Base query para chats del usuario
            if es_admin:
                chats_query = db.query(Chat)
                mensajes_query = db.query(MensajeChat)
            else:
                chats_query = db.query(Chat).filter(
                    or_(
                        Chat.cliente_id == usuario_id,
                        Chat.mecanico_id == usuario_id
                    )
                )
                mensajes_query = db.query(MensajeChat).join(Chat).filter(
                    or_(
                        Chat.cliente_id == usuario_id,
                        Chat.mecanico_id == usuario_id
                    )
                )
            
            # Estadísticas básicas
            total_chats = chats_query.count()
            chats_activos = chats_query.filter(Chat.activo == True).count()
            total_mensajes = mensajes_query.count()
            
            # Mensajes no leídos
            mensajes_no_leidos = mensajes_query.filter(
                and_(
                    MensajeChat.remitente_id != usuario_id,
                    MensajeChat.estado != EstadoMensaje.LEIDO
                )
            ).count()
            
            # Usuarios conectados (últimos 5 minutos)
            tiempo_limite = datetime.now() - timedelta(minutes=5)
            usuarios_conectados = db.query(ConexionChat).filter(
                and_(
                    ConexionChat.activa == True,
                    ConexionChat.last_activity >= tiempo_limite
                )
            ).distinct(ConexionChat.usuario_id).count()
            
            # Promedio de tiempo de respuesta
            promedio_respuesta = ChatController._calcular_promedio_respuesta(db, usuario_id, es_admin)
            
            return ChatEstadisticas(
                total_chats=total_chats,
                chats_activos=chats_activos,
                total_mensajes=total_mensajes,
                mensajes_no_leidos=mensajes_no_leidos,
                usuarios_conectados=usuarios_conectados,
                promedio_respuesta_minutos=promedio_respuesta
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener estadísticas: {str(e)}"
            )
    
    # Métodos para WebSocket
    @staticmethod
    def crear_conexion(db: Session, conexion_data: ConexionChatCreate, usuario_id: int) -> bool:
        """Crear o actualizar conexión WebSocket"""
        try:
            # Verificar si ya existe conexión activa
            conexion_existente = db.query(ConexionChat).filter(
                and_(
                    ConexionChat.usuario_id == usuario_id,
                    ConexionChat.chat_id == conexion_data.chat_id,
                    ConexionChat.activa == True
                )
            ).first()
            
            if conexion_existente:
                # Actualizar conexión existente
                conexion_existente.session_id = conexion_data.session_id
                conexion_existente.last_activity = datetime.now()
            else:
                # Crear nueva conexión
                nueva_conexion = ConexionChat(
                    usuario_id=usuario_id,
                    chat_id=conexion_data.chat_id,
                    session_id=conexion_data.session_id
                )
                db.add(nueva_conexion)
            
            db.commit()
            return True
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear conexión: {str(e)}"
            )
    
    @staticmethod
    def desconectar_usuario(db: Session, session_id: str) -> bool:
        """Desconectar usuario del chat"""
        try:
            conexion = db.query(ConexionChat).filter(
                ConexionChat.session_id == session_id
            ).first()
            
            if conexion:
                conexion.activa = False
                db.commit()
            
            return True
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al desconectar usuario: {str(e)}"
            )
    
    @staticmethod
    def actualizar_actividad(db: Session, session_id: str) -> bool:
        """Actualizar última actividad de conexión"""
        try:
            db.query(ConexionChat).filter(
                ConexionChat.session_id == session_id
            ).update({
                ConexionChat.last_activity: datetime.now()
            })
            
            db.commit()
            return True
            
        except Exception as e:
            db.rollback()
            return False
    
    # Métodos privados auxiliares
    @staticmethod
    def _construir_chat_response(db: Session, chat: Chat) -> ChatResponse:
        """Construir respuesta de chat con información relacionada"""
        # Obtener estadísticas del chat
        total_mensajes = db.query(MensajeChat).filter(
            MensajeChat.chat_id == chat.id
        ).count()
        
        # Último mensaje
        ultimo_mensaje = db.query(MensajeChat).filter(
            MensajeChat.chat_id == chat.id
        ).order_by(desc(MensajeChat.created_at)).first()
        
        # Mensajes no leídos para el usuario actual (esto se puede ajustar según contexto)
        mensajes_no_leidos = db.query(MensajeChat).filter(
            and_(
                MensajeChat.chat_id == chat.id,
                MensajeChat.estado != EstadoMensaje.LEIDO
            )
        ).count()
        
        return ChatResponse(
            id=chat.id,
            titulo=chat.titulo,
            proceso_id=chat.proceso_id,
            cliente_id=chat.cliente_id,
            mecanico_id=chat.mecanico_id,
            activo=chat.activo,
            created_at=chat.created_at,
            updated_at=chat.updated_at,
            cliente_nombre=chat.cliente.nombre if chat.cliente else None,
            cliente_email=chat.cliente.email if chat.cliente else None,
            mecanico_nombre=chat.mecanico.nombre if chat.mecanico else None,
            mecanico_email=chat.mecanico.email if chat.mecanico else None,
            proceso_descripcion=chat.proceso.descripcion if chat.proceso else None,
            automovil_placa=chat.proceso.automovil.placa if chat.proceso and chat.proceso.automovil else None,
            total_mensajes=total_mensajes,
            mensajes_no_leidos=mensajes_no_leidos,
            ultimo_mensaje=ultimo_mensaje.contenido[:100] if ultimo_mensaje else None,
            ultimo_mensaje_fecha=ultimo_mensaje.created_at if ultimo_mensaje else None
        )
    
    @staticmethod
    def _construir_mensaje_response(mensaje: MensajeChat) -> MensajeChatResponse:
        """Construir respuesta de mensaje con información del remitente"""
        # Información del mensaje padre si es respuesta
        mensaje_padre_contenido = None
        mensaje_padre_remitente = None
        
        if mensaje.respuesta_a:
            mensaje_padre = mensaje.mensaje_padre
            if mensaje_padre:
                mensaje_padre_contenido = mensaje_padre.contenido[:50]
                mensaje_padre_remitente = mensaje_padre.remitente.nombre if mensaje_padre.remitente else "Usuario"
        
        return MensajeChatResponse(
            id=mensaje.id,
            chat_id=mensaje.chat_id,
            remitente_id=mensaje.remitente_id,
            contenido=mensaje.contenido,
            tipo_mensaje=mensaje.tipo_mensaje,
            archivo_url=mensaje.archivo_url,
            respuesta_a=mensaje.respuesta_a,
            estado=mensaje.estado,
            created_at=mensaje.created_at,
            leido_at=mensaje.leido_at,
            remitente_nombre=mensaje.remitente.nombre if mensaje.remitente else "Usuario",
            remitente_email=mensaje.remitente.email if mensaje.remitente else None,
            remitente_rol=mensaje.remitente.rol.nombre if mensaje.remitente and mensaje.remitente.rol else None,
            mensaje_padre_contenido=mensaje_padre_contenido,
            mensaje_padre_remitente=mensaje_padre_remitente
        )
    
    @staticmethod
    def _obtener_participantes_activos(db: Session, chat_id: int) -> List[dict]:
        """Obtener lista de participantes activos en el chat"""
        tiempo_limite = datetime.now() - timedelta(minutes=5)
        
        participantes = db.query(ConexionChat).filter(
            and_(
                ConexionChat.chat_id == chat_id,
                ConexionChat.activa == True,
                ConexionChat.last_activity >= tiempo_limite
            )
        ).options(
            joinedload(ConexionChat.usuario)
        ).all()
        
        resultado = []
        for participante in participantes:
            if participante.usuario:
                resultado.append({
                    "usuario_id": participante.usuario_id,
                    "nombre": participante.usuario.nombre,
                    "email": participante.usuario.email,
                    "rol": participante.usuario.rol.nombre if participante.usuario.rol else None,
                    "ultima_actividad": participante.last_activity
                })
        
        return resultado
    
    @staticmethod
    def _calcular_promedio_respuesta(db: Session, usuario_id: int, es_admin: bool = False) -> float:
        """Calcular promedio de tiempo de respuesta en minutos"""
        try:
            # Esta es una implementación básica, se puede mejorar con lógica más compleja
            if es_admin:
                # Para admin, calcular promedio general
                chats_activos = db.query(Chat).filter(Chat.activo == True).all()
            else:
                # Para usuario, solo sus chats
                chats_activos = db.query(Chat).filter(
                    and_(
                        Chat.activo == True,
                        or_(
                            Chat.cliente_id == usuario_id,
                            Chat.mecanico_id == usuario_id
                        )
                    )
                ).all()
            
            if not chats_activos:
                return 0.0
            
            total_tiempo = 0
            total_respuestas = 0
            
            for chat in chats_activos:
                # Obtener mensajes del chat ordenados por fecha
                mensajes = db.query(MensajeChat).filter(
                    MensajeChat.chat_id == chat.id
                ).order_by(MensajeChat.created_at).all()
                
                # Calcular tiempo entre mensajes de diferentes usuarios
                for i in range(1, len(mensajes)):
                    mensaje_anterior = mensajes[i-1]
                    mensaje_actual = mensajes[i]
                    
                    if mensaje_anterior.remitente_id != mensaje_actual.remitente_id:
                        tiempo_respuesta = (mensaje_actual.created_at - mensaje_anterior.created_at).total_seconds() / 60
                        if tiempo_respuesta <= 60:  # Solo contar respuestas dentro de 1 hora
                            total_tiempo += tiempo_respuesta
                            total_respuestas += 1
            
            return total_tiempo / total_respuestas if total_respuestas > 0 else 0.0
            
        except Exception:
            return 0.0