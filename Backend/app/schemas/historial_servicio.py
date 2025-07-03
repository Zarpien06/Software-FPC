# app/schemas/historial_servicio.py
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from enum import Enum

# Importar enums del modelo
from app.models.historial_servicio import TipoMantenimiento, EstadoHistorial

# Schema para filtros de búsqueda
class HistorialServicioFilter(BaseModel):
    estado: Optional[EstadoHistorial] = None
    tipo_mantenimiento: Optional[TipoMantenimiento] = None
    automovil_id: Optional[int] = None
    tecnico_id: Optional[int] = None
    cliente_id: Optional[int] = None
    proceso_id: Optional[int] = None
    
    # Filtros de fecha
    fecha_servicio_desde: Optional[datetime] = None
    fecha_servicio_hasta: Optional[datetime] = None
    fecha_inicio_desde: Optional[datetime] = None
    fecha_inicio_hasta: Optional[datetime] = None
    fecha_fin_desde: Optional[datetime] = None
    fecha_fin_hasta: Optional[datetime] = None
    
    # Filtros de costo
    costo_minimo: Optional[Decimal] = Field(None, ge=0)
    costo_maximo: Optional[Decimal] = Field(None, ge=0)
    
    # Filtros de kilometraje
    kilometraje_minimo: Optional[int] = Field(None, ge=0)
    kilometraje_maximo: Optional[int] = Field(None, ge=0)
    
    # Filtros de garantía
    en_garantia: Optional[bool] = None
    
    # Filtros de calificación
    calificacion_minima: Optional[int] = Field(None, ge=1, le=5)
    
    # Búsqueda por texto
    codigo_servicio: Optional[str] = Field(None, description="Buscar por código de servicio")
    descripcion: Optional[str] = Field(None, description="Buscar en descripción (contiene)")
    
    # Filtros generales
    activo: Optional[bool] = True
    
    # Paginación
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=100, ge=1, le=1000)

# Schema base
class HistorialServicioBase(BaseModel):
    codigo_servicio: str = Field(..., min_length=3, max_length=50, description="Código único del servicio")
    fecha_servicio: datetime = Field(..., description="Fecha y hora del servicio")
    tipo_mantenimiento: TipoMantenimiento = Field(..., description="Tipo de mantenimiento")
    descripcion: str = Field(..., min_length=10, description="Descripción detallada del servicio")
    observaciones: Optional[str] = Field(None, description="Observaciones adicionales")
    
    # Información técnica
    kilometraje_actual: Optional[int] = Field(None, ge=0, description="Kilometraje actual del vehículo")
    kilometraje_proximo_servicio: Optional[int] = Field(None, ge=0, description="Kilometraje para próximo servicio")
    
    # Información económica
    costo_mano_obra: Optional[Decimal] = Field(default=0.00, ge=0, description="Costo de mano de obra")
    costo_repuestos: Optional[Decimal] = Field(default=0.00, ge=0, description="Costo de repuestos")
    costo_total: Decimal = Field(..., ge=0, description="Costo total del servicio")
    
    # Fechas de programación
    fecha_inicio: Optional[datetime] = Field(None, description="Fecha de inicio del trabajo")
    fecha_fin: Optional[datetime] = Field(None, description="Fecha de finalización del trabajo")
    fecha_proximo_servicio: Optional[datetime] = Field(None, description="Fecha programada para próximo servicio")
    
    # Garantía
    garantia_dias: Optional[int] = Field(default=0, ge=0, description="Días de garantía")
    
    # Relaciones
    automovil_id: int = Field(..., description="ID del automóvil")
    tecnico_id: Optional[int] = Field(None, description="ID del técnico responsable")
    cliente_id: Optional[int] = Field(None, description="ID del cliente")
    proceso_id: Optional[int] = Field(None, description="ID del proceso relacionado")

    @validator('fecha_fin')
    def validar_fecha_fin(cls, v, values):
        if v and 'fecha_inicio' in values and values['fecha_inicio'] and v <= values['fecha_inicio']:
            raise ValueError('La fecha de fin debe ser posterior a la fecha de inicio')
        return v

    @validator('kilometraje_proximo_servicio')
    def validar_kilometraje_proximo(cls, v, values):
        if v and 'kilometraje_actual' in values and values['kilometraje_actual'] and v <= values['kilometraje_actual']:
            raise ValueError('El kilometraje del próximo servicio debe ser mayor al actual')
        return v

# Schema para crear historial de servicio
class HistorialServicioCreate(HistorialServicioBase):
    pass

# Schema para actualizar historial de servicio
class HistorialServicioUpdate(BaseModel):
    codigo_servicio: Optional[str] = Field(None, min_length=3, max_length=50)
    fecha_servicio: Optional[datetime] = None
    tipo_mantenimiento: Optional[TipoMantenimiento] = None
    estado: Optional[EstadoHistorial] = None
    descripcion: Optional[str] = Field(None, min_length=10)
    observaciones: Optional[str] = None
    trabajo_realizado: Optional[str] = None
    repuestos_utilizados: Optional[str] = None
    
    # Información técnica
    kilometraje_actual: Optional[int] = Field(None, ge=0)
    kilometraje_proximo_servicio: Optional[int] = Field(None, ge=0)
    
    # Información económica
    costo_mano_obra: Optional[Decimal] = Field(None, ge=0)
    costo_repuestos: Optional[Decimal] = Field(None, ge=0)
    costo_total: Optional[Decimal] = Field(None, ge=0)
    
    # Fechas
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    fecha_proximo_servicio: Optional[datetime] = None
    
    # Garantía
    garantia_dias: Optional[int] = Field(None, ge=0)
    fecha_vencimiento_garantia: Optional[datetime] = None
    
    # Calificación del cliente
    calificacion_servicio: Optional[int] = Field(None, ge=1, le=5)
    comentarios_cliente: Optional[str] = None
    
    # Relaciones
    tecnico_id: Optional[int] = None
    cliente_id: Optional[int] = None
    proceso_id: Optional[int] = None

# Schema para iniciar servicio
class HistorialServicioIniciar(BaseModel):
    observaciones: Optional[str] = None
    kilometraje_actual: Optional[int] = Field(None, ge=0)

# Schema para completar servicio
class HistorialServicioCompletar(BaseModel):
    trabajo_realizado: str = Field(..., min_length=10, description="Descripción del trabajo realizado")
    repuestos_utilizados: Optional[str] = None
    costo_mano_obra: Optional[Decimal] = Field(None, ge=0)
    costo_repuestos: Optional[Decimal] = Field(None, ge=0)
    costo_total: Decimal = Field(..., ge=0, description="Costo total final")
    observaciones: Optional[str] = None
    kilometraje_proximo_servicio: Optional[int] = Field(None, ge=0)
    fecha_proximo_servicio: Optional[datetime] = None

# Schema para calificación del cliente
class HistorialServicioCalificacion(BaseModel):
    calificacion_servicio: int = Field(..., ge=1, le=5, description="Calificación del 1 al 5")
    comentarios_cliente: Optional[str] = Field(None, description="Comentarios del cliente")

# Schema para respuesta con información completa
class HistorialServicioResponse(HistorialServicioBase):
    id: int
    estado: EstadoHistorial
    trabajo_realizado: Optional[str]
    repuestos_utilizados: Optional[str]
    fecha_vencimiento_garantia: Optional[datetime]
    calificacion_servicio: Optional[int]
    comentarios_cliente: Optional[str]
    activo: bool
    creado_en: datetime
    actualizado_en: datetime
    
    # Propiedades calculadas
    esta_en_garantia: Optional[bool] = None
    duracion_servicio: Optional[float] = None

    class Config:
        from_attributes = True

# Schema para listado con información resumida
class HistorialServicioResumen(BaseModel):
    id: int
    codigo_servicio: str
    fecha_servicio: datetime
    tipo_mantenimiento: TipoMantenimiento
    estado: EstadoHistorial
    descripcion: str
    costo_total: Decimal
    automovil_id: int
    tecnico_id: Optional[int]
    cliente_id: Optional[int]
    calificacion_servicio: Optional[int]

    class Config:
        from_attributes = True

# Schemas para estadísticas
class HistorialServicioEstadisticas(BaseModel):
    total_servicios: int
    servicios_completados: int
    servicios_en_proceso: int
    servicios_cancelados: int
    costo_total_servicios: Decimal
    promedio_calificacion: Optional[float]
    servicios_en_garantia: int

# Schema para reporte de servicios
class HistorialServicioReporte(BaseModel):
    periodo_inicio: datetime
    periodo_fin: datetime
    total_servicios: int
    ingresos_totales: Decimal
    servicios_por_tipo: dict
    servicios_por_tecnico: dict
    promedio_calificacion: Optional[float]
    servicios_en_garantia: int