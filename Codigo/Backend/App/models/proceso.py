# app/models/proceso.py

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Enum, DECIMAL
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class EstadoProceso(enum.Enum):
    PENDIENTE    = "PENDIENTE"
    EN_PROGRESO  = "EN_PROGRESO"
    COMPLETADO   = "COMPLETADO"
    CANCELADO    = "CANCELADO"
    PAUSADO      = "PAUSADO"

class TipoProceso(enum.Enum):
    MANTENIMIENTO = "MANTENIMIENTO"
    REPARACION    = "REPARACION"
    DIAGNOSTICO   = "DIAGNOSTICO"
    PINTURA       = "PINTURA"
    MECANICA      = "MECANICA"
    ELECTRICA     = "ELECTRICA"
    CARROCERIA    = "CARROCERIA"
    INSPECCION    = "INSPECCION"

class PrioridadProceso(enum.Enum):
    BAJA     = "BAJA"
    MEDIA    = "MEDIA"
    ALTA     = "ALTA"
    URGENTE  = "URGENTE"

class Proceso(Base):
    __tablename__ = "procesos"

    id                       = Column(Integer, primary_key=True, index=True, autoincrement=True)
    codigo_proceso           = Column(String(50), unique=True, nullable=False, index=True)
    nombre                   = Column(String(200), nullable=False)
    descripcion              = Column(Text)
    tipo_proceso             = Column(Enum(TipoProceso), nullable=False, default=TipoProceso.MANTENIMIENTO)
    estado                   = Column(Enum(EstadoProceso), nullable=False, default=EstadoProceso.PENDIENTE)
    prioridad                = Column(Enum(PrioridadProceso), nullable=False, default=PrioridadProceso.MEDIA)
    fecha_inicio_programada  = Column(DateTime, nullable=False)
    fecha_fin_programada     = Column(DateTime)
    fecha_inicio_real        = Column(DateTime)
    fecha_fin_real           = Column(DateTime)
    duracion_estimada_horas  = Column(DECIMAL(5, 2))
    duracion_real_horas      = Column(DECIMAL(5, 2))
    costo_estimado           = Column(DECIMAL(15, 2))
    costo_real               = Column(DECIMAL(15, 2))
    costo_mano_obra          = Column(DECIMAL(15, 2))
    costo_repuestos          = Column(DECIMAL(15, 2))
    kilometraje_actual       = Column(Integer)
    observaciones_iniciales  = Column(Text)
    observaciones_finales    = Column(Text)
    trabajo_realizado        = Column(Text)
    repuestos_utilizados     = Column(Text)
    garantia_dias            = Column(Integer, default=0)
    fecha_vencimiento_garantia = Column(DateTime)
    calificacion_cliente     = Column(Integer)
    comentarios_cliente      = Column(Text)
    requiere_inspeccion      = Column(Boolean, default=False)
    inspeccion_realizada     = Column(Boolean, default=False)
    fecha_inspeccion         = Column(DateTime)
    resultado_inspeccion     = Column(Text)

    # 🔑 Claves foráneas apuntando a usuarios.usuario_id
    automovil_id            = Column(Integer, ForeignKey("automoviles.id"), nullable=False)
    tecnico_responsable_id  = Column(Integer, ForeignKey("usuarios.usuario_id"))
    inspector_id            = Column(Integer, ForeignKey("usuarios.usuario_id"))
    cliente_id              = Column(Integer, ForeignKey("usuarios.usuario_id"))
    creado_por              = Column(Integer, ForeignKey("usuarios.usuario_id"))
    actualizado_por         = Column(Integer, ForeignKey("usuarios.usuario_id"))

    activo          = Column(Boolean, default=True)
    creado_en       = Column(DateTime, default=func.now())
    actualizado_en  = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relaciones
    automovil            = relationship("Automovil", back_populates="procesos")
    tecnico_responsable  = relationship(
        "Usuario",
        foreign_keys=[tecnico_responsable_id],
        back_populates="procesos_como_tecnico"
    )
    inspector            = relationship(
        "Usuario",
        foreign_keys=[inspector_id],
        back_populates="procesos_como_inspector"
    )
    cliente              = relationship(
        "Usuario",
        foreign_keys=[cliente_id],
        back_populates="procesos_como_cliente"
    )
    creador              = relationship(
        "Usuario",
        foreign_keys=[creado_por]
    )
    actualizador         = relationship(
        "Usuario",
        foreign_keys=[actualizado_por]
    )
    historial_servicios   = relationship(
        "HistorialServicio",
        back_populates="proceso",
        cascade="all, delete-orphan"
    )
    chats = relationship(
        "Chat",
        back_populates="proceso", 
        cascade="all, delete-orphan"
    )
    reportes = relationship("Reporte", 
        back_populates="proceso"
    )


    def __repr__(self):
        return (
            f"<Proceso(id={self.id}, codigo='{self.codigo_proceso}', "
            f"tipo='{self.tipo_proceso.name}', estado='{self.estado.name}')>"
        )

    @property
    def duracion_real_calculada(self):
        if self.fecha_inicio_real and self.fecha_fin_real:
            delta = self.fecha_fin_real - self.fecha_inicio_real
            return round(delta.total_seconds() / 3600, 2)
        return None

    @property
    def esta_en_garantia(self):
        if self.fecha_vencimiento_garantia:
            from datetime import datetime
            return datetime.now() < self.fecha_vencimiento_garantia
        return False

    @property
    def porcentaje_progreso(self):
        estados = {
            EstadoProceso.PENDIENTE: 0,
            EstadoProceso.EN_PROGRESO: 50,
            EstadoProceso.PAUSADO: 50,
            EstadoProceso.COMPLETADO: 100,
            EstadoProceso.CANCELADO: 0
        }
        return estados.get(self.estado, 0)

    def calcular_costo_total(self):
        return (self.costo_mano_obra or 0) + (self.costo_repuestos or 0)

    def actualizar_estado_automatico(self):
        from datetime import datetime
        ahora = datetime.now()
        if self.estado == EstadoProceso.PENDIENTE and self.fecha_inicio_real:
            self.estado = EstadoProceso.EN_PROGRESO
        elif self.estado == EstadoProceso.EN_PROGRESO and self.fecha_fin_real:
            self.estado = EstadoProceso.COMPLETADO
