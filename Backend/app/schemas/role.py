from pydantic import BaseModel, Field, validator
from typing import List, Optional

class RoleBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=50, description="Nombre del rol")
    
    @validator('nombre')
    def validate_nombre(cls, v):
        # Convertir a minúsculas y validar caracteres permitidos
        v = v.lower().strip()
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('El nombre del rol solo puede contener letras, números, guiones y guiones bajos')
        return v

class RoleCreate(RoleBase):
    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "supervisor"
            }
        }

class RoleUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=50)
    
    @validator('nombre')
    def validate_nombre(cls, v):
        if v is not None:
            v = v.lower().strip()
            if not v.replace('_', '').replace('-', '').isalnum():
                raise ValueError('El nombre del rol solo puede contener letras, números, guiones y guiones bajos')
        return v

class RoleResponse(RoleBase):
    id: int = Field(..., description="ID único del rol")
    
    class Config:
        from_orm = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "nombre": "admin"
            }
        }

class RoleListResponse(BaseModel):
    roles: List[RoleResponse]
    total: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "roles": [
                    {"id": 1, "nombre": "admin"},
                    {"id": 2, "nombre": "empleado"},
                    {"id": 3, "nombre": "cliente"}
                ],
                "total": 3
            }
        }

class RoleAssignRequest(BaseModel):
    user_id: int = Field(..., description="ID del usuario")
    role_id: int = Field(..., description="ID del rol a asignar")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 5,
                "role_id": 2
            }
        }