from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Numeric, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class TipoReporte(str, enum.Enum):
    SERVICIO_PRINCIPAL = "SERVICIO_PRINCIPAL"
    SERVICIO_FINAL = "SERVICIO_FINAL"
    DIAGNOSTICO = "DIAGNOSTICO"
    INSPECCION = "INSPECCION"
    MANTENIMIENTO = "MANTENIMIENTO"
    REPARACION = "REPARACION"
    REVISION_TECNICA = "REVISION_TECNICA"

class EstadoReporte(str, enum.Enum):
    BORRADOR = "BORRADOR"
    FINALIZADO = "FINALIZADO"
    APROBADO = "APROBADO"
    ARCHIVADO = "ARCHIVADO"

class Reporte(Base):
    __tablename__ = "reportes"

    id = Column(Integer, primary_key=True, index=True)
    codigo_reporte = Column(String(50), unique=True, index=True, nullable=False)
    titulo = Column(String(200), nullable=False)
    tipo_reporte = Column(Enum(TipoReporte), nullable=False, default=TipoReporte.SERVICIO_PRINCIPAL)
    estado = Column(Enum(EstadoReporte), nullable=False, default=EstadoReporte.BORRADOR)

    # Relaciones
    automovil_id = Column(Integer, ForeignKey("automoviles.id"))
    proceso_id = Column(Integer, ForeignKey("procesos.id"), nullable=True)
    usuario_creador_id = Column(Integer, ForeignKey("usuarios.usuario_id"), nullable=False)
    tecnico_responsable_id = Column(Integer, ForeignKey("usuarios.usuario_id"), nullable=True)

    # Contenido del reporte
    descripcion_trabajo = Column(Text, nullable=False)
    observaciones_tecnicas = Column(Text)
    recomendaciones = Column(Text)
    trabajo_realizado = Column(Text)
    materiales_utilizados = Column(Text)
    tiempo_empleado = Column(Integer, comment="Tiempo en minutos")

    # Información técnica
    kilometraje_inicial = Column(Integer)
    kilometraje_final = Column(Integer)
    diagnostico_inicial = Column(Text)
    problemas_encontrados = Column(Text)
    solucion_aplicada = Column(Text)

    # Costos
    costo_mano_obra = Column(Numeric(10, 2), default=0.00)
    costo_materiales = Column(Numeric(10, 2), default=0.00)
    costo_total = Column(Numeric(10, 2), default=0.00)

    # Calidad y garantía
    nivel_satisfaccion = Column(Integer, comment="Escala 1-5")
    garantia_dias = Column(Integer, default=0)
    requiere_seguimiento = Column(Boolean, default=False)
    fecha_seguimiento = Column(DateTime)

    # Archivos adjuntos
    fotos_antes = Column(Text, comment="URLs separadas por comas")
    fotos_despues = Column(Text, comment="URLs separadas por comas")
    documentos_adjuntos = Column(Text, comment="URLs separadas por comas")

    # Firmas y aprobaciones
    firma_tecnico = Column(String(255))
    firma_supervisor = Column(String(255))
    firma_cliente = Column(String(255))
    fecha_aprobacion_cliente = Column(DateTime)

    # Metadatos
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    fecha_finalizacion = Column(DateTime)
    version = Column(Integer, default=1)

    # Relaciones
    automovil = relationship("Automovil", back_populates="reportes")
    proceso = relationship("Proceso", back_populates="reportes")
    usuario_creador = relationship("Usuario", foreign_keys=[usuario_creador_id], back_populates="reportes_creados")
    tecnico_responsable = relationship("Usuario", foreign_keys=[tecnico_responsable_id], back_populates="reportes_asignados")

    def __repr__(self):
        return f"<Reporte(id={self.id}, codigo='{self.codigo_reporte}', tipo='{self.tipo_reporte}', estado='{self.estado}')>"

    def generar_codigo_reporte(self):
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        tipo_codigo = self.tipo_reporte.value[:3].upper()
        return f"RPT-{tipo_codigo}-{timestamp}-{self.id or '000'}"

    def calcular_costo_total(self):
        self.costo_total = (self.costo_mano_obra or 0) + (self.costo_materiales or 0)
        return self.costo_total

    def puede_ser_editado(self):
        return self.estado in [EstadoReporte.BORRADOR]

    def puede_ser_aprobado(self):
        return self.estado == EstadoReporte.FINALIZADO

    def es_visible_para_cliente(self):
        return self.estado in [EstadoReporte.FINALIZADO, EstadoReporte.APROBADO]
