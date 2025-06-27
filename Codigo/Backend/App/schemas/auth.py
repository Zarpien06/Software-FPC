from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from enum import Enum

class TipoIdentificacionEnum(str, Enum):
    CC = "cc"
    TI = "ti"
    CE = "ce"
    PP = "pp"

class LoginRequest(BaseModel):
    correo: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(..., min_length=1, description="Contraseña del usuario")
    
    class Config:
        json_schema_extra = {
            "example": {
                "correo": "admin@fullpaint.com",
                "password": "Admin123!"
            }
        }

class RegisterRequest(BaseModel):
    nombre_completo: str = Field(..., min_length=2, max_length=100, description="Nombre completo del usuario")
    correo: EmailStr = Field(..., description="Email único del usuario")
    password: str = Field(..., min_length=8, max_length=128, description="Contraseña del usuario")
    telefono: Optional[str] = Field(None, max_length=15, description="Teléfono del usuario")
    tipo_identificacion: TipoIdentificacionEnum = Field(..., description="Tipo de identificación")
    numero_identificacion: str = Field(..., min_length=5, max_length=20, description="Número de identificación")
    
    @validator('password')
    def validate_password(cls, v):
        from app.auth.password_handler import password_handler
        is_valid, message = password_handler.validate_password_strength(v)
        if not is_valid:
            raise ValueError(message)
        return v
    
    @validator('telefono')
    def validate_telefono(cls, v):
        if v and not v.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise ValueError('El teléfono debe contener solo números, espacios, guiones y el símbolo +')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "nombre_completo": "Juan Pérez García",
                "correo": "juan.perez@example.com",
                "password": "MiPassword123!",
                "telefono": "3001234567",
                "tipo_identificacion": "cc",
                "numero_identificacion": "1234567890"
            }
        }

class TokenResponse(BaseModel):
    access_token: str = Field(..., description="Token JWT de acceso")
    token_type: str = Field(default="bearer", description="Tipo de token")
    expires_in: int = Field(..., description="Tiempo de expiración en segundos")
    user_info: dict = Field(..., description="Información básica del usuario")
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 1800,
                "user_info": {
                    "usuario_id": 1,
                    "nombre_completo": "Juan Pérez",
                    "correo": "juan@example.com",
                    "role": {"id": 1, "nombre": "admin"}
                }
            }
        }

class UserInfo(BaseModel):
    usuario_id: int
    nombre_completo: str
    correo: EmailStr
    telefono: Optional[str]
    tipo_identificacion: str
    numero_identificacion: str
    estado: str
    rol_id: Optional[int]
    foto_perfil: str
    fecha_registro: str
    role: Optional[dict]
    tipo_identificacion_info: Optional[dict]
    
    class Config:
        from_orm = True
