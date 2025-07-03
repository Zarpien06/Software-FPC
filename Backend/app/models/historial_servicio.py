# app/models/historial_servicio.py
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, DECIMAL, ForeignKey, Boolean, Enum as SQLEnum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class TipoMantenimiento(str, enum.Enum):
    PREVENTIVO       = "PREVENTIVO"
    CORRECTIVO       = "CORRECTIVO"
    PREDICTIVO       = "PREDICTIVO"
    EMERGENCIA       = "EMERGENCIA"
    REVISION         = "REVISION"
    CAMBIO_ACEITE    = "CAMBIO_ACEITE"
    CAMBIO_FILTROS   = "CAMBIO_FILTROS"
    REVISION_FRENOS  = "REVISION_FRENOS"
    ALINEACION       = "ALINEACION"
    BALANCEO         = "BALANCEO"

class EstadoHistorial(str, enum.Enum):
    PROGRAMADO    = "PROGRAMADO"
    EN_PROCESO    = "EN_PROCESO"
    COMPLETADO    = "COMPLETADO"
    CANCELADO     = "CANCELADO"
    REPROGRAMADO  = "REPROGRAMADO"

class HistorialServicio(Base):
    __tablename__ = "historial_servicios"
    
    id                       = Column(Integer, primary_key=True, index=True, autoincrement=True)
    codigo_servicio          = Column(String(50), unique=True, index=True, nullable=False)
    fecha_servicio           = Column(DateTime, nullable=False)
    tipo_mantenimiento       = Column(SQLEnum(TipoMantenimiento), nullable=False)
    estado                   = Column(SQLEnum(EstadoHistorial), default=EstadoHistorial.PROGRAMADO)
    descripcion              = Column(Text, nullable=False)
    observaciones            = Column(Text)
    trabajo_realizado        = Column(Text)
    repuestos_utilizados     = Column(Text)
    kilometraje_actual       = Column(Integer)
    kilometraje_proximo_servicio = Column(Integer)
    costo_mano_obra          = Column(DECIMAL(10, 2), default=0.00)
    costo_repuestos          = Column(DECIMAL(10, 2), default=0.00)
    costo_total              = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    fecha_inicio             = Column(DateTime)
    fecha_fin                = Column(DateTime)
    fecha_proximo_servicio   = Column(DateTime)
    garantia_dias            = Column(Integer, default=0)
    fecha_vencimiento_garantia = Column(DateTime)
    calificacion_servicio    = Column(Integer)
    comentarios_cliente      = Column(Text)

    # Claves foráneas corregidas:
    automovil_id = Column(Integer, ForeignKey("automoviles.id"), nullable=False)
    tecnico_id   = Column(Integer, ForeignKey("usuarios.usuario_id"))
    cliente_id   = Column(Integer, ForeignKey("usuarios.usuario_id"))
    proceso_id   = Column(Integer, ForeignKey("procesos.id"))

    activo        = Column(Boolean, default=True)
    creado_en     = Column(DateTime, server_default=func.now())
    actualizado_en= Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relaciones ORM
    automovil    = relationship("Automovil", back_populates="historial_servicios")
    proceso      = relationship("Proceso", back_populates="historial_servicios")
    tecnico      = relationship(
        "Usuario",
        foreign_keys=[tecnico_id],
        back_populates="servicios_como_tecnico"
    )
    cliente      = relationship(
        "Usuario",
        foreign_keys=[cliente_id],
        back_populates="servicios_como_cliente"
    )

    def __repr__(self):
        return (
            f"<HistorialServicio(id={self.id}, codigo='{self.codigo_servicio}', "
            f"tipo='{self.tipo_mantenimiento}', estado='{self.estado}')>"
        )

    @property
    def esta_en_garantia(self) -> bool:
        if not self.fecha_vencimiento_garantia:
            return False
        from datetime import datetime
        return datetime.now() < self.fecha_vencimiento_garantia

    @property
    def duracion_servicio(self) -> float:
        if self.fecha_inicio and self.fecha_fin:
            delta = self.fecha_fin - self.fecha_inicio
            return round(delta.total_seconds() / 3600, 2)
        return 0.0
