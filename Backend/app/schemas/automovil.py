# app/schemas/automovil.py

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class EstadoAutomovilEnum(str, Enum):
    ACTIVO = "activo"
    EN_SERVICIO = "en_servicio"
    INACTIVO = "inactivo"
    FUERA_DE_SERVICIO = "fuera_de_servicio"

class TipoCombustibleEnum(str, Enum):
    GASOLINA = "gasolina"
    DIESEL = "diesel"
    GAS = "gas"
    ELECTRICO = "electrico"
    HIBRIDO = "hibrido"

class TipoTransmisionEnum(str, Enum):
    MANUAL = "manual"
    AUTOMATICA = "automatica"
    SEMIAUTOMATICA = "semiautomatica"

# Esquema base para automóvil
class AutomovilBase(BaseModel):
    placa: str = Field(..., min_length=6, max_length=10, description="Placa del vehículo")
    vin: Optional[str] = Field(None, min_length=17, max_length=17, description="Número de identificación del vehículo")
    marca: str = Field(..., min_length=2, max_length=50, description="Marca del vehículo")
    modelo: str = Field(..., min_length=1, max_length=50, description="Modelo del vehículo")
    año: int = Field(..., ge=1900, le=2030, description="Año de fabricación")
    color: str = Field(..., min_length=3, max_length=30, description="Color del vehículo")
    cilindraje: Optional[float] = Field(None, ge=0.1, le=10.0, description="Cilindraje en litros")
    numero_motor: Optional[str] = Field(None, max_length=50, description="Número del motor")
    tipo_combustible: TipoCombustibleEnum = Field(default=TipoCombustibleEnum.GASOLINA)
    tipo_transmision: TipoTransmisionEnum = Field(default=TipoTransmisionEnum.MANUAL)
    kilometraje_actual: int = Field(default=0, ge=0, description="Kilometraje actual")
    kilometraje_ingreso: Optional[int] = Field(None, ge=0, description="Kilometraje al ingreso")
    estado: EstadoAutomovilEnum = Field(default=EstadoAutomovilEnum.ACTIVO)
    observaciones: Optional[str] = Field(None, max_length=1000, description="Observaciones generales")
    numero_puertas: Optional[int] = Field(None, ge=2, le=6, description="Número de puertas")
    capacidad_pasajeros: Optional[int] = Field(None, ge=1, le=50, description="Capacidad de pasajeros")
    fecha_matricula: Optional[datetime] = Field(None, description="Fecha de matrícula")
    fecha_soat: Optional[datetime] = Field(None, description="Fecha vencimiento SOAT")
    fecha_tecnomecanica: Optional[datetime] = Field(None, description="Fecha vencimiento tecnomecánica")
    
    @validator('placa')
    def validar_placa(cls, v):
        if v:
            v = v.upper().strip()
            # Validación básica de formato de placa colombiana
            if len(v) < 6:
                raise ValueError('La placa debe tener al menos 6 caracteres')
        return v
    
    @validator('vin')
    def validar_vin(cls, v):
        if v:
            v = v.upper().strip()
            if len(v) != 17:
                raise ValueError('El VIN debe tener exactamente 17 caracteres')
        return v
    
    @validator('kilometraje_ingreso')
    def validar_kilometraje_ingreso(cls, v, values):
        if v is not None and 'kilometraje_actual' in values:
            if v > values['kilometraje_actual']:
                raise ValueError('El kilometraje de ingreso no puede ser mayor al actual')
        return v

# Esquema para crear automóvil
class AutomovilCreate(AutomovilBase):
    propietario_id: int = Field(..., gt=0, description="ID del propietario")

# Esquema para actualizar automóvil
class AutomovilUpdate(BaseModel):
    placa: Optional[str] = Field(None, min_length=6, max_length=10)
    vin: Optional[str] = Field(None, min_length=17, max_length=17)
    marca: Optional[str] = Field(None, min_length=2, max_length=50)
    modelo: Optional[str] = Field(None, min_length=1, max_length=50)
    año: Optional[int] = Field(None, ge=1900, le=2030)
    color: Optional[str] = Field(None, min_length=3, max_length=30)
    cilindraje: Optional[float] = Field(None, ge=0.1, le=10.0)
    numero_motor: Optional[str] = Field(None, max_length=50)
    tipo_combustible: Optional[TipoCombustibleEnum] = None
    tipo_transmision: Optional[TipoTransmisionEnum] = None
    kilometraje_actual: Optional[int] = Field(None, ge=0)
    kilometraje_ingreso: Optional[int] = Field(None, ge=0)
    estado: Optional[EstadoAutomovilEnum] = None
    observaciones: Optional[str] = Field(None, max_length=1000)
    numero_puertas: Optional[int] = Field(None, ge=2, le=6)
    capacidad_pasajeros: Optional[int] = Field(None, ge=1, le=50)
    fecha_matricula: Optional[datetime] = None
    fecha_soat: Optional[datetime] = None
    fecha_tecnomecanica: Optional[datetime] = None
    propietario_id: Optional[int] = Field(None, gt=0)

# Información básica del propietario para incluir in responses
class PropietarioBasico(BaseModel):
    id: int
    nombre_completo: str
    correo: str
    telefono: Optional[str]
    
    class Config:
        from_attributes = True

# Esquema de respuesta para automóvil
class AutomovilResponse(AutomovilBase):
    id: int
    created_at: datetime
    updated_at: datetime
    propietario_id: int
    propietario: Optional[PropietarioBasico] = None
    
    class Config:
        from_attributes = True

# Esquema para respuesta con información adicional
class AutomovilDetallado(AutomovilResponse):
    nombre_completo: str
    esta_activo: bool
    esta_en_servicio: bool
    total_procesos: Optional[int] = 0
    ultimo_servicio: Optional[datetime] = None
    proximo_mantenimiento: Optional[str] = None

# Esquema para listado de automóviles
class AutomovilListItem(BaseModel):
    id: int
    placa: str
    marca: str
    modelo: str
    año: int
    color: str
    estado: EstadoAutomovilEnum
    kilometraje_actual: int
    propietario_nombre: str
    propietario_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Esquema para búsqueda y filtros
class AutomovilFiltros(BaseModel):
    placa: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    año_min: Optional[int] = Field(None, ge=1900)
    año_max: Optional[int] = Field(None, le=2030)
    estado: Optional[EstadoAutomovilEnum] = None
    propietario_id: Optional[int] = None
    tipo_combustible: Optional[TipoCombustibleEnum] = None
    tipo_transmision: Optional[TipoTransmisionEnum] = None

# Esquema para estadísticas
class AutomovilEstadisticas(BaseModel):
    total_automoviles: int
    por_estado: dict
    por_marca: dict
    por_año: dict
    por_combustible: dict
    promedio_kilometraje: float
    
# Esquema para cambio de estado
class CambioEstadoAutomovil(BaseModel):
    estado: EstadoAutomovilEnum
    observaciones: Optional[str] = Field(None, max_length=500, description="Motivo del cambio de estado")

# Esquema para actualizar kilometraje
class ActualizarKilometraje(BaseModel):
    kilometraje_actual: int = Field(..., ge=0, description="Nuevo kilometraje")
    observaciones: Optional[str] = Field(None, max_length=500, description="Observaciones del cambio")

# Respuesta paginada
class AutomovilPaginado(BaseModel):
    items: List[AutomovilListItem]
    total: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_prev: bool

class AutomovilListResponse(BaseModel):
    automoviles: List[AutomovilListItem]
    total: int
    skip: int
    limit: int
    has_next: bool
    has_prev: bool

# Esquema para historial del automóvil
class AutomovilHistorialItem(BaseModel):
    id: int
    fecha: datetime
    tipo: str  # 'servicio', 'cambio_estado', 'kilometraje', etc.
    descripcion: str
    kilometraje: Optional[int] = None
    usuario: str
    observaciones: Optional[str] = None
    
    class Config:
        from_attributes = True

class AutomovilHistorialResponse(BaseModel):
    automovil_id: int
    automovil_placa: str
    historial: List[AutomovilHistorialItem]
    total: int
    skip: int
    limit: int
    has_next: bool
    has_prev: bool

# Esquema para estadísticas (mejorando el existente)
class AutomovilEstadisticasResponse(BaseModel):
    total_automoviles: int
    por_estado: dict
    por_marca: dict
    por_año: dict
    por_combustible: dict
    por_transmision: dict
    promedio_kilometraje: float
    automoviles_proximos_mantenimiento: int
    automoviles_documentos_vencidos: int