from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.models.user import User
from decimal import Decimal
import enum

# Enums
class EstadoCotizacion(str, enum.Enum):
    BORRADOR = "BORRADOR"
    ENVIADA = "ENVIADA"
    ACEPTADA = "ACEPTADA"
    RECHAZADA = "RECHAZADA"
    VENCIDA = "VENCIDA"
    CONVERTIDA = "CONVERTIDA"

class TipoServicio(str, enum.Enum):
    MANTENIMIENTO = "MANTENIMIENTO"
    REPARACION = "REPARACION"
    PINTURA = "PINTURA"
    MECANICA = "MECANICA"
    ELECTRICIDAD = "ELECTRICIDAD"
    SUSPENSION = "SUSPENSION"
    FRENOS = "FRENOS"
    MOTOR = "MOTOR"
    TRANSMISION = "TRANSMISION"
    AIRE_ACONDICIONADO = "AIRE_ACONDICIONADO"

# Modelos
class Cotizacion(Base):
    __tablename__ = "cotizaciones"
    
    id = Column(Integer, primary_key=True, index=True)
    numero_cotizacion = Column(String(20), unique=True, index=True)
    
    cliente_id = Column(Integer, ForeignKey("usuarios.usuario_id"), nullable=False)
    automovil_id = Column(Integer, ForeignKey("automoviles.id"), nullable=False)
    empleado_id = Column(Integer, ForeignKey("usuarios.usuario_id"), nullable=False)
    
    estado = Column(Enum(EstadoCotizacion), default=EstadoCotizacion.BORRADOR)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_vencimiento = Column(DateTime(timezone=True), nullable=False)
    fecha_aceptacion = Column(DateTime(timezone=True), nullable=True)
    
    descripcion_general = Column(Text, nullable=False)
    observaciones = Column(Text, nullable=True)
    tiempo_estimado_horas = Column(Integer, nullable=False)
    kilometraje_actual = Column(Integer, nullable=True)
    
    subtotal = Column(Numeric(10, 2), nullable=False, default=Decimal("0.00"))
    impuestos = Column(Numeric(10, 2), nullable=False, default=Decimal("0.00"))
    descuento = Column(Numeric(10, 2), nullable=False, default=Decimal("0.00"))
    total = Column(Numeric(10, 2), nullable=False, default=Decimal("0.00"))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # CORREGIDO: Cambiar back_populates para que coincida con el modelo Usuario
    cliente = relationship(User, foreign_keys=[cliente_id], back_populates="cotizaciones")
    
    # Para el empleado, necesitas agregar la relación correspondiente en el modelo Usuario
    # O puedes hacer esta relación sin back_populates por ahora:
    empleado = relationship(User, foreign_keys=[empleado_id])
    
    automovil = relationship("Automovil", back_populates="cotizaciones")
    items = relationship("ItemCotizacion", back_populates="cotizacion", cascade="all, delete-orphan")

class ItemCotizacion(Base):
    __tablename__ = "items_cotizacion"
    
    id = Column(Integer, primary_key=True, index=True)
    cotizacion_id = Column(Integer, ForeignKey("cotizaciones.id"), nullable=False)
    
    tipo_servicio = Column(Enum(TipoServicio), nullable=False)
    descripcion = Column(String(255), nullable=False)
    detalle = Column(Text, nullable=True)
    
    cantidad = Column(Integer, nullable=False, default=1)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    precio_total = Column(Numeric(10, 2), nullable=False)
    
    tiempo_estimado_horas = Column(Numeric(4, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    cotizacion = relationship("Cotizacion", back_populates="items")