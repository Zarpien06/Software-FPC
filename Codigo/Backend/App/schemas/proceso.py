# 📁 app/schemas/proceso.py
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from enum import Enum

# Enums para validación
class EstadoProcesoEnum(str, Enum):
    PENDIENTE = "PENDIENTE"
    EN_PROGRESO = "EN_PROGRESO"
    COMPLETADO = "COMPLETADO"
    CANCELADO = "CANCELADO"
    PAUSADO = "PAUSADO"

# Alias para compatibilidad
EstadoEnum = EstadoProcesoEnum

class TipoProcesoEnum(str, Enum):
    MANTENIMIENTO = "MANTENIMIENTO"
    REPARACION = "REPARACION"
    DIAGNOSTICO = "DIAGNOSTICO"
    PINTURA = "PINTURA"
    MECANICA = "MECANICA"
    ELECTRICA = "ELECTRICA"
    CARROCERIA = "CARROCERIA"
    INSPECCION = "INSPECCION"

# Alias para compatibilidad
TipoEnum = TipoProcesoEnum

class PrioridadProcesoEnum(str, Enum):
    BAJA = "BAJA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"
    URGENTE = "URGENTE"

# Alias para compatibilidad con imports existentes
PrioridadEnum = PrioridadProcesoEnum

# Schema para filtros de búsqueda
class ProcesoFilter(BaseModel):
    estado: Optional[EstadoProcesoEnum] = None
    tipo_proceso: Optional[TipoProcesoEnum] = None
    prioridad: Optional[PrioridadProcesoEnum] = None
    automovil_id: Optional[int] = None
    tecnico_responsable_id: Optional[int] = None
    cliente_id: Optional[int] = None
    fecha_inicio_desde: Optional[datetime] = None
    fecha_inicio_hasta: Optional[datetime] = None
    fecha_fin_desde: Optional[datetime] = None
    fecha_fin_hasta: Optional[datetime] = None
    activo: Optional[bool] = True
    requiere_inspeccion: Optional[bool] = None
    inspeccion_realizada: Optional[bool] = None
    
    # Filtros de búsqueda por texto
    nombre: Optional[str] = Field(None, description="Buscar por nombre (contiene)")
    codigo_proceso: Optional[str] = Field(None, description="Buscar por código de proceso")
    
    # Paginación
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=100, ge=1, le=1000)

# Schema base
class ProcesoBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=200, description="Nombre descriptivo del proceso")
    descripcion: Optional[str] = Field(None, description="Descripción detallada del proceso")
    tipo_proceso: TipoProcesoEnum = Field(default=TipoProcesoEnum.MANTENIMIENTO)
    prioridad: PrioridadProcesoEnum = Field(default=PrioridadProcesoEnum.MEDIA)
    
    # Fechas programadas
    fecha_inicio_programada: datetime = Field(..., description="Fecha y hora programada de inicio")
    fecha_fin_programada: Optional[datetime] = Field(None, description="Fecha y hora programada de finalización")
    duracion_estimada_horas: Optional[Decimal] = Field(None, ge=0, description="Duración estimada en horas")
    
    # Información económica
    costo_estimado: Optional[Decimal] = Field(None, ge=0, description="Costo estimado del proceso")
    costo_mano_obra: Optional[Decimal] = Field(None, ge=0, description="Costo estimado de mano de obra")
    costo_repuestos: Optional[Decimal] = Field(None, ge=0, description="Costo estimado de repuestos")
    
    # Información técnica
    kilometraje_actual: Optional[int] = Field(None, ge=0, description="Kilometraje actual del vehículo")
    observaciones_iniciales: Optional[str] = Field(None, description="Observaciones iniciales del proceso")
    
    # Garantía
    garantia_dias: Optional[int] = Field(default=0, ge=0, description="Días de garantía")
    
    # Control de calidad
    requiere_inspeccion: bool = Field(default=False, description="Si requiere inspección de calidad")
    
    # Relaciones
    automovil_id: int = Field(..., description="ID del automóvil")
    tecnico_responsable_id: Optional[int] = Field(None, description="ID del técnico responsable")
    cliente_id: Optional[int] = Field(None, description="ID del cliente")

    @validator('fecha_fin_programada')
    def validar_fecha_fin(cls, v, values):
        if v and 'fecha_inicio_programada' in values and v <= values['fecha_inicio_programada']:
            raise ValueError('La fecha de fin debe ser posterior a la fecha de inicio')
        return v

# Schema para crear proceso
class ProcesoCreate(ProcesoBase):
    pass

# Schema para actualizar proceso
class ProcesoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=200)
    descripcion: Optional[str] = None
    tipo_proceso: Optional[TipoProcesoEnum] = None
    estado: Optional[EstadoProcesoEnum] = None
    prioridad: Optional[PrioridadProcesoEnum] = None
    
    # Fechas
    fecha_inicio_programada: Optional[datetime] = None
    fecha_fin_programada: Optional[datetime] = None
    fecha_inicio_real: Optional[datetime] = None
    fecha_fin_real: Optional[datetime] = None
    duracion_estimada_horas: Optional[Decimal] = Field(None, ge=0)
    duracion_real_horas: Optional[Decimal] = Field(None, ge=0)
    
    # Costos
    costo_estimado: Optional[Decimal] = Field(None, ge=0)
    costo_real: Optional[Decimal] = Field(None, ge=0)
    costo_mano_obra: Optional[Decimal] = Field(None, ge=0)
    costo_repuestos: Optional[Decimal] = Field(None, ge=0)
    
    # Información técnica
    kilometraje_actual: Optional[int] = Field(None, ge=0)
    observaciones_iniciales: Optional[str] = None
    observaciones_finales: Optional[str] = None
    trabajo_realizado: Optional[str] = None
    repuestos_utilizados: Optional[str] = None
    
    # Garantía y calidad
    garantia_dias: Optional[int] = Field(None, ge=0)
    calificacion_cliente: Optional[int] = Field(None, ge=1, le=5)
    comentarios_cliente: Optional[str] = None
    
    # Control de calidad
    requiere_inspeccion: Optional[bool] = None
    inspeccion_realizada: Optional[bool] = None
    fecha_inspeccion: Optional[datetime] = None
    resultado_inspeccion: Optional[str] = None
    
    # Relaciones
    tecnico_responsable_id: Optional[int] = None
    inspector_id: Optional[int] = None
    cliente_id: Optional[int] = None

# Schema para iniciar proceso
class ProcesoIniciar(BaseModel):
    observaciones_iniciales: Optional[str] = None
    kilometraje_actual: Optional[int] = Field(None, ge=0)
    
# Schema para completar proceso
class ProcesoCompletar(BaseModel):
    observaciones_finales: str = Field(..., min_length=10, description="Observaciones finales obligatorias")
    trabajo_realizado: str = Field(..., min_length=10, description="Descripción del trabajo realizado")
    costo_real: Optional[Decimal] = Field(None, ge=0)
    costo_mano_obra: Optional[Decimal] = Field(None, ge=0)
    costo_repuestos: Optional[Decimal] = Field(None, ge=0)
    repuestos_utilizados: Optional[str] = None
    duracion_real_horas: Optional[Decimal] = Field(None, ge=0)

# Schema para inspección
class ProcesoInspeccion(BaseModel):
    resultado_inspeccion: str = Field(..., min_length=5, description="Resultado de la inspección")
    inspector_id: int = Field(..., description="ID del inspector")

# Schema para respuesta con información completa
class ProcesoResponse(ProcesoBase):
    id: int
    codigo_proceso: str
    estado: EstadoProcesoEnum
    fecha_inicio_real: Optional[datetime]
    fecha_fin_real: Optional[datetime]
    duracion_real_horas: Optional[Decimal]
    costo_real: Optional[Decimal]
    observaciones_finales: Optional[str]
    trabajo_realizado: Optional[str]
    repuestos_utilizados: Optional[str]
    fecha_vencimiento_garantia: Optional[datetime]
    calificacion_cliente: Optional[int]
    comentarios_cliente: Optional[str]
    inspeccion_realizada: bool
    fecha_inspeccion: Optional[datetime]
    resultado_inspeccion: Optional[str]
    activo: bool
    creado_en: datetime
    actualizado_en: datetime
    
    # Propiedades calculadas
    porcentaje_progreso: Optional[int] = None
    esta_en_garantia: Optional[bool] = None
    duracion_real_calculada: Optional[float] = None

    class Config:
        from_attributes = True

# Schema para listado con información resumida
class ProcesoResumen(BaseModel):
    id: int
    codigo_proceso: str
    nombre: str
    tipo_proceso: TipoProcesoEnum
    estado: EstadoProcesoEnum
    prioridad: PrioridadProcesoEnum
    fecha_inicio_programada: datetime
    fecha_fin_programada: Optional[datetime]
    costo_estimado: Optional[Decimal]
    costo_real: Optional[Decimal]
    automovil_id: int
    tecnico_responsable_id: Optional[int]
    cliente_id: Optional[int]

    class Config:
        from_attributes = True