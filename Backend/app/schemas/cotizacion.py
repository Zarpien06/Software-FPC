from pydantic import BaseModel, validator, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from enum import Enum

class EstadoCotizacion(str, Enum):
    BORRADOR = "BORRADOR"
    ENVIADA = "ENVIADA"
    ACEPTADA = "ACEPTADA"
    RECHAZADA = "RECHAZADA"
    VENCIDA = "VENCIDA"
    CONVERTIDA = "CONVERTIDA"

class TipoServicio(str, Enum):
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

# Esquemas para Items
class ItemCotizacionBase(BaseModel):
    tipo_servicio: TipoServicio
    descripcion: str = Field(..., min_length=5, max_length=255)
    detalle: Optional[str] = None
    cantidad: int = Field(default=1, ge=1)
    precio_unitario: Decimal = Field(..., ge=0)
    tiempo_estimado_horas: Decimal = Field(..., ge=0.1)

class ItemCotizacionCreate(ItemCotizacionBase):
    pass

class ItemCotizacionUpdate(BaseModel):
    tipo_servicio: Optional[TipoServicio] = None
    descripcion: Optional[str] = Field(None, min_length=5, max_length=255)
    detalle: Optional[str] = None
    cantidad: Optional[int] = Field(None, ge=1)
    precio_unitario: Optional[Decimal] = Field(None, ge=0)
    tiempo_estimado_horas: Optional[Decimal] = Field(None, ge=0.1)

class ItemCotizacionResponse(ItemCotizacionBase):
    id: int
    cotizacion_id: int
    precio_total: Decimal
    created_at: datetime
    
    class Config:
        from_attributes = True

# Esquemas para Cotizaciones
class CotizacionBase(BaseModel):
    descripcion_general: str = Field(..., min_length=10, max_length=1000)
    observaciones: Optional[str] = None
    tiempo_estimado_horas: int = Field(..., ge=1)
    kilometraje_actual: Optional[int] = Field(None, ge=0)

class CotizacionCreate(CotizacionBase):
    cliente_id: int
    automovil_id: int
    fecha_vencimiento: datetime
    items: List[ItemCotizacionCreate] = Field(..., min_items=1)
    
    @validator('fecha_vencimiento')
    def validar_fecha_vencimiento(cls, v):
        if v <= datetime.now():
            raise ValueError('La fecha de vencimiento debe ser futura')
        return v

class CotizacionUpdate(BaseModel):
    descripcion_general: Optional[str] = Field(None, min_length=10, max_length=1000)
    observaciones: Optional[str] = None
    tiempo_estimado_horas: Optional[int] = Field(None, ge=1)
    kilometraje_actual: Optional[int] = Field(None, ge=0)
    fecha_vencimiento: Optional[datetime] = None
    items: Optional[List[ItemCotizacionCreate]] = None
    
    @validator('fecha_vencimiento')
    def validar_fecha_vencimiento(cls, v):
        if v and v <= datetime.now():
            raise ValueError('La fecha de vencimiento debe ser futura')
        return v

class CambiarEstadoRequest(BaseModel):
    nuevo_estado: EstadoCotizacion

class CotizacionResponse(CotizacionBase):
    id: int
    numero_cotizacion: str
    cliente_id: int
    automovil_id: int
    empleado_id: int
    estado: EstadoCotizacion
    fecha_creacion: datetime
    fecha_vencimiento: datetime
    fecha_aceptacion: Optional[datetime]
    subtotal: Decimal
    impuestos: Decimal
    descuento: Decimal
    total: Decimal
    created_at: datetime
    updated_at: Optional[datetime]
    
    # Información relacionada
    cliente_nombre: Optional[str] = None
    automovil_info: Optional[str] = None
    empleado_nombre: Optional[str] = None
    items: List[ItemCotizacionResponse] = []
    
    class Config:
        from_attributes = True

class EstadisticasCotizaciones(BaseModel):
    total_cotizaciones: int
    cotizaciones_por_estado: dict
    valor_total_cotizaciones: Decimal
    cotizaciones_vencidas: int
    promedio_valor_cotizacion: Decimal
    servicios_mas_solicitados: List[dict]