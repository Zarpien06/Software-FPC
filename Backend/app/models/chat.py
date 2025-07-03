# app/models/chat.py

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class TipoMensaje(str, enum.Enum):
    TEXTO = "texto"
    IMAGEN = "imagen"
    AUDIO = "audio"
    ARCHIVO = "archivo"

class EstadoMensaje(str, enum.Enum):
    ENVIADO = "ENVIADO"
    LEIDO = "LEIDO"

class TipoMensajeModel(Base):
    __tablename__ = "tipos_mensaje"

    tipo_id = Column(String(20), primary_key=True)
    descripcion = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<TipoMensaje(tipo_id={self.tipo_id})>"

class MensajeChat(Base):
    __tablename__ = "chat"

    mensaje_id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    vehiculo_id = Column(Integer, ForeignKey("automoviles.id"))
    remitente_id = Column(Integer, ForeignKey("usuarios.usuario_id"))
    receptor_id = Column(Integer, ForeignKey("usuarios.usuario_id"))
    mensaje = Column(Text, nullable=True)
    tipo_id = Column(String(20), ForeignKey("tipos_mensaje.tipo_id"), default=TipoMensaje.TEXTO)
    archivo_url = Column(String(255), nullable=True)
    leido = Column(Boolean, default=False)
    fecha_envio = Column(DateTime(timezone=True), server_default=func.now())

    chat = relationship("Chat", back_populates="mensajes")
    remitente = relationship("Usuario", foreign_keys=[remitente_id], back_populates="mensajes_enviados")
    receptor = relationship("Usuario", foreign_keys=[receptor_id], back_populates="mensajes_recibidos")
    tipo_mensaje = relationship("TipoMensajeModel", foreign_keys=[tipo_id])
    vehiculo = relationship("Automovil", back_populates="mensajes_chat")

    def __repr__(self):
        return f"<MensajeChat(id={self.mensaje_id}, tipo={self.tipo_id}, leido={self.leido})>"

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    proceso_id = Column(Integer, ForeignKey("procesos.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("usuarios.usuario_id"), nullable=False)
    mecanico_id = Column(Integer, ForeignKey("usuarios.usuario_id"), nullable=True)
    titulo = Column(String(200), nullable=False)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    proceso = relationship("Proceso", back_populates="chats")
    cliente = relationship("Usuario", foreign_keys=[cliente_id], back_populates="chats_como_cliente")
    mecanico = relationship("Usuario", foreign_keys=[mecanico_id], back_populates="chats_como_mecanico")
    mensajes = relationship("MensajeChat", back_populates="chat", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Chat(id={self.id}, proceso_id={self.proceso_id}, titulo='{self.titulo}')>"

class ConexionChat(Base):
    __tablename__ = "conexiones_chat"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.usuario_id"), nullable=False)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    session_id = Column(String(100), nullable=False, unique=True)
    activa = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_activity = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    usuario = relationship("Usuario", back_populates="conexiones_chat")
    chat = relationship("Chat")

    def __repr__(self):
        return f"<ConexionChat(usuario_id={self.usuario_id}, chat_id={self.chat_id}, activa={self.activa})>"
