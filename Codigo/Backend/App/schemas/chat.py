# app/schemas/chat.py
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class TipoMensajeSchema(str, Enum):
    TEXTO = "TEXTO"
    IMAGEN = "IMAGEN"
    ARCHIVO = "ARCHIVO"
    NOTIFICACION = "NOTIFICACION"

class EstadoMensajeSchema(str, Enum):
    ENVIADO = "ENVIADO"
    ENTREGADO = "ENTREGADO"
    LEIDO = "LEIDO"

# Esquemas para Chat
class ChatBase(BaseModel):
    titulo: str = Field(..., min_length=3, max_length=200, description="Título del chat")
    proceso_id: int = Field(..., gt=0, description="ID del proceso asociado")
    mecanico_id: Optional[int] = Field(None, gt=0, description="ID del mecánico asignado")

class ChatCreate(ChatBase):
    """Esquema para crear un nuevo chat"""
    pass

class ChatUpdate(BaseModel):
    """Esquema para actualizar un chat existente"""
    titulo: Optional[str] = Field(None, min_length=3, max_length=200)
    mecanico_id: Optional[int] = Field(None, gt=0)
    activo: Optional[bool] = None

class ChatResponse(ChatBase):
    """Esquema de respuesta para chat"""
    id: int
    cliente_id: int
    activo: bool
    created_at: datetime
    updated_at: datetime
    
    # Información del cliente
    cliente_nombre: Optional[str] = None
    cliente_email: Optional[str] = None
    
    # Información del mecánico
    mecanico_nombre: Optional[str] = None
    mecanico_email: Optional[str] = None
    
    # Información del proceso
    proceso_descripcion: Optional[str] = None
    automovil_placa: Optional[str] = None
    
    # Estadísticas del chat
    total_mensajes: int = 0
    mensajes_no_leidos: int = 0
    ultimo_mensaje: Optional[str] = None
    ultimo_mensaje_fecha: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Esquemas para Mensajes
class MensajeChatBase(BaseModel):
    contenido: str = Field(..., min_length=1, max_length=2000, description="Contenido del mensaje")
    tipo_mensaje: TipoMensajeSchema = Field(default=TipoMensajeSchema.TEXTO)
    archivo_url: Optional[str] = Field(None, max_length=500, description="URL del archivo adjunto")
    respuesta_a: Optional[int] = Field(None, gt=0, description="ID del mensaje al que responde")

class MensajeChatCreate(MensajeChatBase):
    """Esquema para crear un nuevo mensaje"""
    chat_id: int = Field(..., gt=0, description="ID del chat")

class MensajeChatUpdate(BaseModel):
    """Esquema para actualizar un mensaje (solo contenido)"""
    contenido: Optional[str] = Field(None, min_length=1, max_length=2000)
    estado: Optional[EstadoMensajeSchema] = None

class MensajeChatResponse(MensajeChatBase):
    """Esquema de respuesta para mensaje"""
    id: int
    chat_id: int
    remitente_id: int
    estado: EstadoMensajeSchema
    created_at: datetime
    leido_at: Optional[datetime] = None
    
    # Información del remitente
    remitente_nombre: Optional[str] = None
    remitente_email: Optional[str] = None
    remitente_rol: Optional[str] = None
    
    # Información del mensaje padre (si es respuesta)
    mensaje_padre_contenido: Optional[str] = None
    mensaje_padre_remitente: Optional[str] = None
    
    class Config:
        from_attributes = True

# Esquemas para WebSocket
class MensajeWebSocket(BaseModel):
    """Esquema para mensajes en tiempo real vía WebSocket"""
    tipo: str = Field(..., description="Tipo de evento WebSocket")
    chat_id: int
    mensaje: Optional[dict] = None
    usuario_id: int
    timestamp: datetime = Field(default_factory=datetime.now)

class ConexionChatCreate(BaseModel):
    """Esquema para crear conexión de chat"""
    chat_id: int = Field(..., gt=0)
    session_id: str = Field(..., min_length=10, max_length=100)

class ConexionChatResponse(BaseModel):
    """Esquema de respuesta para conexión"""
    id: int
    usuario_id: int
    chat_id: int
    session_id: str
    activa: bool
    created_at: datetime
    last_activity: datetime
    
    class Config:
        from_attributes = True

# Esquemas para estadísticas y reportes
class ChatEstadisticas(BaseModel):
    """Estadísticas generales del chat"""
    total_chats: int = 0
    chats_activos: int = 0
    total_mensajes: int = 0
    mensajes_no_leidos: int = 0
    usuarios_conectados: int = 0
    promedio_respuesta_minutos: float = 0.0

class ChatDetalle(ChatResponse):
    """Chat con información detallada incluyendo mensajes recientes"""
    mensajes_recientes: List[MensajeChatResponse] = []
    participantes_activos: List[dict] = []
    
    class Config:
        from_attributes = True

# Esquemas para filtros y búsquedas
class ChatFiltros(BaseModel):
    """Filtros para búsqueda de chats"""
    proceso_id: Optional[int] = None
    cliente_id: Optional[int] = None
    mecanico_id: Optional[int] = None
    activo: Optional[bool] = None
    fecha_desde: Optional[datetime] = None
    fecha_hasta: Optional[datetime] = None
    buscar: Optional[str] = Field(None, max_length=100, description="Búsqueda en título o contenido")
    
class MensajeFiltros(BaseModel):
    """Filtros para búsqueda de mensajes"""
    chat_id: Optional[int] = None
    remitente_id: Optional[int] = None
    tipo_mensaje: Optional[TipoMensajeSchema] = None
    estado: Optional[EstadoMensajeSchema] = None
    fecha_desde: Optional[datetime] = None
    fecha_hasta: Optional[datetime] = None
    buscar: Optional[str] = Field(None, max_length=100, description="Búsqueda en contenido")
    
# Respuestas paginadas
class ChatListResponse(BaseModel):
    """Respuesta paginada para lista de chats"""
    chats: List[ChatResponse]
    total: int
    page: int = 1
    per_page: int = 20
    total_pages: int
    
class MensajeListResponse(BaseModel):
    """Respuesta paginada para lista de mensajes"""
    mensajes: List[MensajeChatResponse]
    total: int
    page: int = 1
    per_page: int = 50
    total_pages: int