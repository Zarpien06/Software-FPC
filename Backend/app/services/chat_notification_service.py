# app/services/chat_notification_service.py
import asyncio
import logging
from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.chat import Chat, MensajeChat
from app.models.user import User
from app.services.websocket_service import websocket_manager
from app.services.notification_service import NotificationService

logger = logging.getLogger(__name__)

class ChatNotificationService:
    """Servicio para gestionar notificaciones relacionadas con el chat"""
    
    def __init__(self):
        self.notification_service = NotificationService()
        
    async def notify_new_message(self, db: Session, mensaje: MensajeChat):
        """Notificar nuevo mensaje en el chat"""
        try:
            # Obtener información del chat y usuarios
            chat = db.query(Chat).filter(Chat.id == mensaje.chat_id).first()
            if not chat:
                return
                
            remitente = db.query(User).filter(User.id == mensaje.remitente_id).first()
            if not remitente:
                return
            
            # Determinar destinatarios (todos menos el remitente)
            destinatarios = []
            if chat.cliente_id != mensaje.remitente_id:
                destinatarios.append(chat.cliente_id)
            if chat.mecanico_id and chat.mecanico_id != mensaje.remitente_id:
                destinatarios.append(chat.mecanico_id)
            
            # Enviar notificación WebSocket en tiempo real
            await websocket_manager.broadcast_to_chat(chat.id, {
                "tipo": "new_message",
                "mensaje": {
                    "id": mensaje.id,
                    "contenido": mensaje.contenido,
                    "tipo_mensaje": mensaje.tipo_mensaje.value,
                    "remitente_id": mensaje.remitente_id,
                    "remitente_nombre": remitente.nombre,
                    "created_at": mensaje.created_at.isoformat(),
                    "archivo_url": mensaje.archivo_url
                },
                "chat_id": chat.id,
                "timestamp": datetime.now().isoformat()
            }, exclude_user=mensaje.remitente_id)
            
            # Enviar notificaciones push/email a usuarios desconectados
            await self._send_offline_notifications(db, chat, mensaje, remitente, destinatarios)
            
        except Exception as e:
            logger.error(f"Error notificando nuevo mensaje: {e}")
            
    async def notify_message_read(self, db: Session, mensaje_id: int, reader_id: int):
        """Notificar que un mensaje fue leído"""
        try:
            mensaje = db.query(MensajeChat).filter(MensajeChat.id == mensaje_id).first()
            if not mensaje:
                return
                
            reader = db.query(User).filter(User.id == reader_id).first()
            if not reader:
                return
            
            # Notificar al remitente original
            await websocket_manager.broadcast_to_user(mensaje.remitente_id, {
                "tipo": "message_read",
                "mensaje_id": mensaje_id,
                "reader_id": reader_id,
                "reader_name": reader.nombre,
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"Error notificando mensaje leído: {e}")
            
    async def notify_chat_created(self, db: Session, chat: Chat):
        """Notificar creación de nuevo chat"""
        try:
            # Obtener información de usuarios
            cliente = db.query(User).filter(User.id == chat.cliente_id).first()
            mecanico = db.query(User).filter(User.id == chat.mecanico_id).first() if chat.mecanico_id else None
            
            # Notificar al cliente
            await websocket_manager.broadcast_to_user(chat.cliente_id, {
                "tipo": "chat_created",
                "chat": {
                    "id": chat.id,
                    "titulo": chat.titulo,
                    "proceso_id": chat.proceso_id,
                    "mecanico_nombre": mecanico.nombre if mecanico else None,
                    "created_at": chat.created_at.isoformat()
                },
                "timestamp": datetime.now().isoformat()
            })
            
            # Notificar al mecánico si está asignado
            if mecanico:
                await websocket_manager.broadcast_to_user(chat.mecanico_id, {
                    "tipo": "chat_assigned",
                    "chat": {
                        "id": chat.id,
                        "titulo": chat.titulo,
                        "proceso_id": chat.proceso_id,
                        "cliente_nombre": cliente.nombre,
                        "created_at": chat.created_at.isoformat()
                    },
                    "timestamp": datetime.now().isoformat()
                })
                
            # Enviar notificación del sistema al chat
            await websocket_manager.send_notification_message(
                chat.id,
                f"Chat creado. Participantes: {cliente.nombre}" + 
                (f" y {mecanico.nombre}" if mecanico else ""),
                "info"
            )
            
        except Exception as e:
            logger.error(f"Error notificando creación de chat: {e}")
            
    async def notify_mechanic_assigned(self, db: Session, chat: Chat, new_mechanic_id: int):
        """Notificar asignación de mecánico al chat"""
        try:
            mecanico = db.query(User).filter(User.id == new_mechanic_id).first()
            cliente = db.query(User).filter(User.id == chat.cliente_id).first()
            
            if not mecanico or not cliente:
                return
            
            # Notificar al cliente
            await websocket_manager.broadcast_to_user(chat.cliente_id, {
                "tipo": "mechanic_assigned",
                "chat_id": chat.id,
                "mecanico": {
                    "id": mecanico.id,
                    "nombre": mecanico.nombre,
                    "email": mecanico.email
                },
                "timestamp": datetime.now().isoformat()
            })
            
            # Notificar al mecánico
            await websocket_manager.broadcast_to_user(new_mechanic_id, {
                "tipo": "chat_assigned",
                "chat": {
                    "id": chat.id,
                    "titulo": chat.titulo,
                    "proceso_id": chat.proceso_id,
                    "cliente_nombre": cliente.nombre
                },
                "timestamp": datetime.now().isoformat()
            })
            
            # Notificar en el chat
            await websocket_manager.send_notification_message(
                chat.id,
                f"El mecánico {mecanico.nombre} se ha unido al chat",
                "info"
            )
            
        except Exception as e:
            logger.error(f"Error notificando asignación de mecánico: {e}")
            
    async def notify_chat_status_change(self, db: Session, chat: Chat, new_status: bool):
        """Notificar cambio de estado del chat"""
        try:
            status_text = "activado" if new_status else "desactivado"
            
            # Notificar a todos los participantes
            participants = [chat.cliente_id]
            if chat.mecanico_id:
                participants.append(chat.mecanico_id)
                
            for user_id in participants:
                await websocket_manager.broadcast_to_user(user_id, {
                    "tipo": "chat_status_changed",
                    "chat_id": chat.id,
                    "nuevo_estado": new_status,
                    "timestamp": datetime.now().isoformat()
                })
            
            # Notificar en el chat
            await websocket_manager.send_notification_message(
                chat.id,
                f"El chat ha sido {status_text}",
                "warning" if not new_status else "info"
            )
            
        except Exception as e:
            logger.error(f"Error notificando cambio de estado: {e}")
            
    async def _send_offline_notifications(self, db: Session, chat: Chat, mensaje: MensajeChat, 
                                        remitente: User, destinatarios: List[int]):
        """Enviar notificaciones a usuarios desconectados"""
        try:
            # Verificar qué usuarios están desconectados
            for user_id in destinatarios:
                # Verificar si el usuario está conectado
                is_online = False
                for chat_id, connections in websocket_manager.active_connections.items():
                    if any(conn["user_id"] == user_id for conn in connections):
                        is_online = True
                        break
                
                # Si no está conectado, enviar notificación push/email
                if not is_online:
                    user = db.query(User).filter(User.id == user_id).first()
                    if user:
                        await self._send_push_notification(user, chat, mensaje, remitente)
                        await self._send_email_notification(user, chat, mensaje, remitente)
                        
        except Exception as e:
            logger.error(f"Error enviando notificaciones offline: {e}")
            
    async def _send_push_notification(self, user: User, chat: Chat, mensaje: MensajeChat, remitente: User):
        """Enviar notificación push"""
        try:
            # Implementar lógica de notificación push
            # (Firebase, OneSignal, etc.)
            title = f"Nuevo mensaje de {remitente.nombre}"
            body = mensaje.contenido[:100] + ("..." if len(mensaje.contenido) > 100 else "")
            
            # Aquí implementarías la lógica específica de tu proveedor de push notifications
            logger.info(f"Push notification enviada a {user.email}: {title}")
            
        except Exception as e:
            logger.error(f"Error enviando push notification: {e}")
            
    async def _send_email_notification(self, user: User, chat: Chat, mensaje: MensajeChat, remitente: User):
        """Enviar notificación por email"""
        try:
            subject = f"Nuevo mensaje en el chat - {chat.titulo}"
            
            body = f"""
            Hola {user.nombre},
            
            Has recibido un nuevo mensaje de {remitente.nombre} en el chat "{chat.titulo}":
            
            "{mensaje.contenido}"
            
            Puedes responder accediendo a tu panel de control.
            
            Saludos,
            Equipo FullPaint
            """
            
            await self.notification_service.send_email(
                to_email=user.email,
                subject=subject,
                body=body
            )
            
        except Exception as e:
            logger.error(f"Error enviando email notification: {e}")

# Instancia global del servicio
chat_notification_service = ChatNotificationService()