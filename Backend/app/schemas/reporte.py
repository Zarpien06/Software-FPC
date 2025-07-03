from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from app.models.reporte import TipoReporte, EstadoReporte

# Esquemas base
class ReporteBase(BaseModel):
    titulo: str = Field(..., min_length=3, max_length=200, description="Título del reporte")
    tipo_reporte: TipoReporte = Field(default=TipoReporte.SERVICIO_PRINCIPAL, description="Tipo de reporte")
    automovil_id: int = Field(..., gt=0, description="ID del automóvil")
    proceso_id: Optional[int] = Field(None, gt=0, description="ID del proceso relacionado")
    tecnico_responsable_id: Optional[int] = Field(None, gt=0, description="ID del técnico responsable")
    
    descripcion_trabajo: str = Field(..., min_length=10, description="Descripción detallada del trabajo")
    observaciones_tecnicas: Optional[str] = Field(None, description="Observaciones técnicas")
    recomendaciones: Optional[str] = Field(None, description="Recomendaciones")
    trabajo_realizado: Optional[str] = Field(None, description="Trabajo específico realizado")
    materiales_utilizados: Optional[str] = Field(None, description="Materiales utilizados")
    tiempo_empleado: Optional[int] = Field(None, ge=0, description="Tiempo empleado en minutos")
    
    kilometraje_inicial: Optional[int] = Field(None, ge=0, description="Kilometraje inicial")
    kilometraje_final: Optional[int] = Field(None, ge=0, description="Kilometraje final")
    diagnostico_inicial: Optional[str] = Field(None, description="Diagnóstico inicial")
    problemas_encontrados: Optional[str] = Field(None, description="Problemas encontrados")
    solucion_aplicada: Optional[str] = Field(None, description="Solución aplicada")
    
    costo_mano_obra: Optional[Decimal] = Field(default=Decimal('0.00'), ge=0, description="Costo mano de obra")
    costo_materiales: Optional[Decimal] = Field(default=Decimal('0.00'), ge=0, description="Costo materiales")
    
    nivel_satisfaccion: Optional[int] = Field(None, ge=1, le=5, description="Nivel satisfacción (1-5)")
    garantia_dias: Optional[int] = Field(default=0, ge=0, description="Días de garantía")
    requiere_seguimiento: Optional[bool] = Field(default=False, description="Requiere seguimiento")
    fecha_seguimiento: Optional[datetime] = Field(None, description="Fecha de seguimiento")
    
    fotos_antes: Optional[str] = Field(None, description="URLs de fotos antes (separadas por comas)")
    fotos_despues: Optional[str] = Field(None, description="URLs de fotos después (separadas por comas)")
    documentos_adjuntos: Optional[str] = Field(None, description="URLs de documentos (separadas por comas)")

    @validator('kilometraje_final')
    def validar_kilometraje_final(cls, v, values):
        if v is not None and 'kilometraje_inicial' in values and values['kilometraje_inicial'] is not None:
            if v < values['kilometraje_inicial']:
                raise ValueError('El kilometraje final no puede ser menor al inicial')
        return v

    @validator('fecha_seguimiento')
    def validar_fecha_seguimiento(cls, v, values):
        if v is not None and v <= datetime.now():
            raise ValueError('La fecha de seguimiento debe ser futura')
        return v

# Crear reporte
class ReporteCreate(ReporteBase):
    """Esquema para crear un nuevo reporte"""
    pass

# Actualizar reporte
class ReporteUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=3, max_length=200)
    tipo_reporte: Optional[TipoReporte] = None
    tecnico_responsable_id: Optional[int] = Field(None, gt=0)
    
    descripcion_trabajo: Optional[str] = Field(None, min_length=10)
    observaciones_tecnicas: Optional[str] = None
    recomendaciones: Optional[str] = None
    trabajo_realizado: Optional[str] = None
    materiales_utilizados: Optional[str] = None
    tiempo_empleado: Optional[int] = Field(None, ge=0)
    
    kilometraje_inicial: Optional[int] = Field(None, ge=0)
    kilometraje_final: Optional[int] = Field(None, ge=0)
    diagnostico_inicial: Optional[str] = None
    problemas_encontrados: Optional[str] = None
    solucion_aplicada: Optional[str] = None
    
    costo_mano_obra: Optional[Decimal] = Field(None, ge=0)
    costo_materiales: Optional[Decimal] = Field(None, ge=0)
    
    nivel_satisfaccion: Optional[int] = Field(None, ge=1, le=5)
    garantia_dias: Optional[int] = Field(None, ge=0)
    requiere_seguimiento: Optional[bool] = None
    fecha_seguimiento: Optional[datetime] = None
    
    fotos_antes: Optional[str] = None
    fotos_despues: Optional[str] = None
    documentos_adjuntos: Optional[str] = None

# Cambiar estado del reporte
class CambiarEstadoReporte(BaseModel):
    estado: EstadoReporte = Field(..., description="Nuevo estado del reporte")
    observaciones: Optional[str] = Field(None, description="Observaciones del cambio de estado")

# Aprobación del cliente
class AprobacionCliente(BaseModel):
    aprobado: bool = Field(..., description="Si el cliente aprueba el reporte")
    firma_cliente: Optional[str] = Field(None, description="Firma digital del cliente")
    comentarios_cliente: Optional[str] = Field(None, description="Comentarios del cliente")
    nivel_satisfaccion: Optional[int] = Field(None, ge=1, le=5, description="Nivel de satisfacción")

# Firmas
class FirmaReporte(BaseModel):
    tipo_firma: str = Field(..., pattern="^(tecnico|supervisor|cliente)$", description="Tipo de firma")
    firma: str = Field(..., description="Firma digital en base64")
    comentarios: Optional[str] = Field(None, description="Comentarios adicionales")

# Respuesta de reporte
class ReporteResponse(BaseModel):
    id: int
    codigo_reporte: str
    titulo: str
    tipo_reporte: TipoReporte
    estado: EstadoReporte
    automovil_id: int
    proceso_id: Optional[int]
    usuario_creador_id: int
    tecnico_responsable_id: Optional[int]
    
    descripcion_trabajo: str
    observaciones_tecnicas: Optional[str]
    recomendaciones: Optional[str]
    trabajo_realizado: Optional[str]
    materiales_utilizados: Optional[str]
    tiempo_empleado: Optional[int]
    
    kilometraje_inicial: Optional[int]
    kilometraje_final: Optional[int]
    diagnostico_inicial: Optional[str]
    problemas_encontrados: Optional[str]
    solucion_aplicada: Optional[str]
    
    costo_mano_obra: Optional[Decimal]
    costo_materiales: Optional[Decimal]
    costo_total: Optional[Decimal]
    
    nivel_satisfaccion: Optional[int]
    garantia_dias: Optional[int]
    requiere_seguimiento: Optional[bool]
    fecha_seguimiento: Optional[datetime]
    
    fotos_antes: Optional[str]
    fotos_despues: Optional[str]
    documentos_adjuntos: Optional[str]
    
    firma_tecnico: Optional[str]
    firma_supervisor: Optional[str]
    firma_cliente: Optional[str]
    fecha_aprobacion_cliente: Optional[datetime]
    
    created_at: datetime
    updated_at: Optional[datetime]
    fecha_finalizacion: Optional[datetime]
    version: int

    class Config:
        from_attributes = True

# Respuesta simplificada para listas
class ReporteSimple(BaseModel):
    id: int
    codigo_reporte: str
    titulo: str
    tipo_reporte: TipoReporte
    estado: EstadoReporte
    automovil_id: int
    usuario_creador_id: int
    tecnico_responsable_id: Optional[int]
    costo_total: Optional[Decimal]
    created_at: datetime
    fecha_finalizacion: Optional[datetime]

    class Config:
        from_attributes = True

# Estadísticas de reportes
class EstadisticasReportes(BaseModel):
    total_reportes: int
    reportes_por_estado: dict[str, int]
    reportes_por_tipo: dict[str, int]
    reportes_mes_actual: int
    reportes_mes_anterior: int
    costo_total_reportes: Decimal
    tiempo_promedio_resolucion: Optional[float]  # En días
    satisfaccion_promedio: Optional[float]
    reportes_con_seguimiento: int

# Filtros de búsqueda
class FiltrosReporte(BaseModel):
    tipo_reporte: Optional[TipoReporte] = None
    estado: Optional[EstadoReporte] = None
    automovil_id: Optional[int] = None
    proceso_id: Optional[int] = None
    tecnico_responsable_id: Optional[int] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    requiere_seguimiento: Optional[bool] = None
    nivel_satisfaccion_min: Optional[int] = Field(None, ge=1, le=5)
    busqueda_texto: Optional[str] = Field(None, min_length=3, description="Búsqueda en título y descripciones")

# Respuesta paginada
class ReportesPaginados(BaseModel):
    reportes: List[ReporteSimple]
    total: int
    pagina: int
    tamano_pagina: int
    total_paginas: int

    @validator('total_paginas', always=True)
    def calcular_total_paginas(cls, v, values):
        if 'total' in values and 'tamano_pagina' in values and values['tamano_pagina'] > 0:
            return (values['total'] + values['tamano_pagina'] - 1) // values['tamano_pagina']
        return 0

# Template de reporte
class TemplateReporte(BaseModel):
    tipo_reporte: TipoReporte
    titulo_sugerido: str
    campos_requeridos: List[str]
    descripcion_template: str
    observaciones_template: Optional[str]
    recomendaciones_template: Optional[str]