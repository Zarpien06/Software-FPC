from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from app.models.proceso import TipoProceso, EstadoProceso, PrioridadProceso

# Esquemas base
class ProcesoBase(BaseModel):
    titulo: str = Field(..., min_length=5, max_length=100, description="Título del proceso")
    descripcion: str = Field(..., min_length=10, description="Descripción detallada del proceso")
    tipo_proceso: TipoProceso = Field(default=TipoProceso.MANTENIMIENTO, description="Tipo de proceso")
    prioridad: PrioridadProceso = Field(default=PrioridadProceso.MEDIA, description="Prioridad del proceso")
    fecha_programada: datetime = Field(..., description="Fecha programada para el proceso")
    fecha_estimada_finalizacion: Optional[datetime] = Field(None, description="Fecha estimada de finalización")
    costo_estimado: Optional[Decimal] = Field(None, ge=0, description="Costo estimado del proceso")
    tecnico_asignado_id: Optional[int] = Field(None, gt=0, description="ID del técnico asignado")
    observaciones_iniciales: Optional[str] = Field(None, description="Observaciones iniciales")
    kilometraje_actual: Optional[int] = Field(None, ge=0, description="Kilometraje al momento del proceso")
    proximo_mantenimiento_km: Optional[int] = Field(None, ge=0, description="Kilometraje del próximo mantenimiento")
    proximo_mantenimiento_fecha: Optional[datetime] = Field(None, description="Fecha del próximo mantenimiento")
    
    @validator('fecha_programada', 'fecha_estimada_finalizacion', 'proximo_mantenimiento_fecha')
    def validar_fechas_futuras(cls, v):
        if v and v < datetime.now():
            raise ValueError('Las fechas deben ser futuras')
        return v
    
    @validator('titulo', 'descripcion')
    def validar_strings(cls, v):
        return v.strip() if v else v

# Esquema para crear proceso
class ProcesoCreate(ProcesoBase):
    automovil_id: int = Field(..., gt=0, description="ID del automóvil")

# Esquema para actualizar proceso
class ProcesoUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=5, max_length=100)
    descripcion: Optional[str] = Field(None, min_length=10)
    tipo_proceso: Optional[TipoProceso] = None
    prioridad: Optional[PrioridadProceso] = None
    fecha_programada: Optional[datetime] = None
    fecha_estimada_finalizacion: Optional[datetime] = None
    costo_estimado: Optional[Decimal] = Field(None, ge=0)
    costo_real: Optional[Decimal] = Field(None, ge=0)
    tecnico_asignado_id: Optional[int] = Field(None, gt=0)
    observaciones_iniciales: Optional[str] = None
    observaciones_finales: Optional[str] = None
    notas_tecnico: Optional[str] = None
    kilometraje_actual: Optional[int] = Field(None, ge=0)
    proximo_mantenimiento_km: Optional[int] = Field(None, ge=0)
    proximo_mantenimiento_fecha: Optional[datetime] = None
    
    @validator('titulo', 'descripcion', 'observaciones_iniciales', 'observaciones_finales', 'notas_tecnico')
    def validar_strings(cls, v):
        return v.strip() if v else v

# Esquema para cambiar estado del proceso
class ProcesoCambiarEstado(BaseModel):
    nuevo_estado: EstadoProceso = Field(..., description="Nuevo estado del proceso")
    observaciones: Optional[str] = Field(None, description="Observaciones del cambio de estado")
    progreso: Optional[int] = Field(None, ge=0, le=100, description="Porcentaje de progreso")
    fecha_inicio: Optional[datetime] = Field(None, description="Fecha de inicio (solo si cambia a EN_PROCESO)")
    fecha_finalizacion: Optional[datetime] = Field(None, description="Fecha de finalización (solo si cambia a COMPLETADO)")

# Esquema para actualizar progreso
class ProcesoActualizarProgreso(BaseModel):
    progreso: int = Field(..., ge=0, le=100, description="Porcentaje de progreso")
    notas_tecnico: Optional[str] = Field(None, description="Notas del técnico sobre el progreso")

# Esquema para asignar técnico
class ProcesoAsignarTecnico(BaseModel):
    tecnico_id: int = Field(..., gt=0, description="ID del técnico a asignar")
    observaciones: Optional[str] = Field(None, description="Observaciones de la asignación")

# Esquema de respuesta básico
class ProcesoResponse(ProcesoBase):
    id: int
    codigo: str
    automovil_id: int
    estado: EstadoProceso
    progreso: int
    fecha_inicio: Optional[datetime]
    fecha_finalizacion: Optional[datetime]
    costo_real: Optional[Decimal]
    observaciones_finales: Optional[str]
    notas_tecnico: Optional[str]
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime]
    creado_por: int
    activo: bool
    
    # Propiedades calculadas
    duracion_total: Optional[int]
    dias_restantes: Optional[int]
    esta_vencido: bool
    diferencia_costo: Optional[float]
    
    class Config:
        from_attributes = True

# Esquema de respuesta con información del automóvil
class ProcesoResponseConAutomovil(ProcesoResponse):
    automovil: Optional[dict] = None  # Información básica del automóvil
    tecnico_asignado: Optional[dict] = None  # Información del técnico
    creado_por_usuario: Optional[dict] = None  # Información del usuario que creó
    
    class Config:
        from_attributes = True

# Esquema para búsqueda y filtros
class ProcesoFiltros(BaseModel):
    codigo: Optional[str] = None
    titulo: Optional[str] = None
    tipo_proceso: Optional[TipoProceso] = None
    estado: Optional[EstadoProceso] = None
    prioridad: Optional[PrioridadProceso] = None
    automovil_id: Optional[int] = None
    tecnico_asignado_id: Optional[int] = None
    creado_por: Optional[int] = None
    activo: Optional[bool] = True
    
    # Filtros de fecha
    fecha_programada_desde: Optional[datetime] = None
    fecha_programada_hasta: Optional[datetime] = None
    fecha_creacion_desde: Optional[datetime] = None
    fecha_creacion_hasta: Optional[datetime] = None
    
    # Filtros de costo
    costo_estimado_desde: Optional[Decimal] = Field(None, ge=0)
    costo_estimado_hasta: Optional[Decimal] = Field(None, ge=0)
    
    # Filtros especiales
    vencidos: Optional[bool] = None  # Solo procesos vencidos
    sin_tecnico: Optional[bool] = None  # Solo procesos sin técnico asignado
    progreso_desde: Optional[int] = Field(None, ge=0, le=100)
    progreso_hasta: Optional[int] = Field(None, ge=0, le=100)
    
    # Ordenamiento
    ordenar_por: Optional[str] = Field(default="fecha_creacion", description="Campo por el cual ordenar")
    orden_desc: Optional[bool] = Field(default=True, description="Orden descendente")
    
    # Paginación
    pagina: Optional[int] = Field(default=1, ge=1, description="Número de página")
    por_pagina: Optional[int] = Field(default=10, ge=1, le=100, description="Elementos por página")

# Esquema de respuesta paginada
class ProcesoResponsePaginado(BaseModel):
    procesos: List[ProcesoResponseConAutomovil]
    total: int
    pagina: int
    por_pagina: int
    total_paginas: int
    
    class Config:
        from_attributes = True

# Esquema para estadísticas
class ProcesoEstadisticas(BaseModel):
    total_procesos: int
    por_estado: dict
    por_tipo_proceso: dict
    por_prioridad: dict
    procesos_vencidos: int
    procesos_sin_tecnico: int
    progreso_promedio: Optional[float]
    costo_total_estimado: Optional[Decimal]
    costo_total_real: Optional[Decimal]
    duracion_promedio: Optional[float]
    
    class Config:
        from_attributes = True

# Esquema para reportes
class ProcesoReporte(BaseModel):
    proceso_id: int
    codigo: str
    titulo: str
    automovil_placa: str
    automovil_info: str
    estado: EstadoProceso
    progreso: int
    fecha_programada: datetime
    fecha_inicio: Optional[datetime]
    fecha_finalizacion: Optional[datetime]
    tecnico_asignado: Optional[str]
    costo_estimado: Optional[Decimal]
    costo_real: Optional[Decimal]
    observaciones: str