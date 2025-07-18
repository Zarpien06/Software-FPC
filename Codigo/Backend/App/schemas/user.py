from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from enum import Enum
from datetime import datetime


# Enums
class EstadoUsuarioEnum(str, Enum):
    ACTIVO = 'ACTIVO'
    INACTIVO = 'INACTIVO'


class TipoIdentificacionEnum(str, Enum):
    cc = "cc"
    ti = "ti"
    ce = "ce"
    pp = "pp"


class UserBase(BaseModel):
    nombre_completo: str = Field(..., min_length=2, max_length=100)
    correo: EmailStr
    telefono: Optional[str] = Field(None, max_length=15)
    tipo_identificacion: TipoIdentificacionEnum
    numero_identificacion: str = Field(..., min_length=5, max_length=20)
    estado: EstadoUsuarioEnum = EstadoUsuarioEnum.ACTIVO
    rol_id: Optional[int] = None
    foto_perfil: Optional[str] = "static/img/default-profile.png"

    @validator('telefono')
    def validate_telefono(cls, v):
        if v and not v.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise ValueError('El teléfono debe contener solo números, espacios, guiones y el símbolo +')
        return v

    @validator('tipo_identificacion', pre=True)
    def normalize_tipo_identificacion(cls, v):
        if isinstance(v, str):
            return v.lower()
        return v

# Esquema para crear usuarios
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)

    @validator('password')
    def validate_password(cls, v):
        from app.auth.password_handler import password_handler
        is_valid, message = password_handler.validate_password_strength(v)
        if not is_valid:
            raise ValueError(message)
        return v


# Esquema para actualizar usuarios
class UserUpdate(BaseModel):
    nombre_completo: Optional[str] = Field(None, min_length=2, max_length=100)
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, max_length=15)
    tipo_identificacion: Optional[TipoIdentificacionEnum] = None
    numero_identificacion: Optional[str] = Field(None, min_length=5, max_length=20)
    estado: Optional[EstadoUsuarioEnum] = None
    rol_id: Optional[int] = None
    foto_perfil: Optional[str] = None

    @validator('telefono')
    def validate_telefono(cls, v):
        if v and not v.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise ValueError('El teléfono debe contener solo números, espacios, guiones y el símbolo +')
        return v


# Esquema del rol (usado en respuesta)
class RoleOut(BaseModel):
    id: int
    nombre: str

    model_config = {
        "from_attributes": True
    }


# Esquema de respuesta completa de un usuario
class UserResponse(UserBase):
    usuario_id: int
    fecha_registro: datetime
    role: Optional[RoleOut] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "usuario_id": 1,
                "nombre_completo": "Juan Pérez García",
                "correo": "juan@example.com",
                "telefono": "3001234567",
                "tipo_identificacion": "cc",
                "numero_identificacion": "1234567890",
                "estado": "ACTIVO",
                "rol_id": 2,
                "foto_perfil": "static/img/default-profile.png",
                "fecha_registro": "2024-01-15T10:30:00",
                "role": {"id": 2, "nombre": "empleado"},
            }
        }
    }


# Esquema de respuesta para listas de usuarios
class UserListResponse(BaseModel):
    users: List[UserResponse]
    total: int
    page: int
    size: int
    total_pages: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "users": [],
                "total": 50,
                "page": 1,
                "size": 10,
                "total_pages": 5
            }
        }
    }


# Cambio de contraseña
class PasswordChangeRequest(BaseModel):
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8, max_length=128)

    @validator('new_password')
    def validate_password(cls, v):
        from app.auth.password_handler import password_handler
        is_valid, message = password_handler.validate_password_strength(v)
        if not is_valid:
            raise ValueError(message)
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "current_password": "MiPasswordActual123!",
                "new_password": "MiNuevoPassword456!"
            }
        }
    }


# Usuario actual autenticado
class UserCurrent(BaseModel):
    usuario_id: int
    nombre_completo: str
    correo: EmailStr
    rol_id: Optional[int] = None
    foto_perfil: Optional[str] = None

    model_config = {
        "from_attributes": True
    }
