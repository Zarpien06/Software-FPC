from sqlalchemy import Column, Integer, String, ForeignKey, Enum, TIMESTAMP, func
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.database import Base

class EstadoUsuario(PyEnum):
    ACTIVO = "activo"
    INACTIVO = "inactivo"

class User(Base):
    __tablename__ = "usuarios"
    
    usuario_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_completo = Column(String(100), nullable=False)
    telefono = Column(String(15), nullable=True)
    correo = Column(String(100), unique=True, nullable=False, index=True)
    tipo_identificacion = Column(String(2), ForeignKey("tipos_identificacion.tipo_id"), nullable=False)
    numero_identificacion = Column(String(20), nullable=False)
    password_hash = Column(String(255), nullable=False)
    estado = Column(String(10), default="activo", nullable=False)
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    foto_perfil = Column(String(255), default="static/img/default-profile.png")
    fecha_registro = Column(TIMESTAMP, default=func.current_timestamp())
    
    # Relaciones
    role = relationship("Role", back_populates="usuarios")
    tipo_identificacion_rel = relationship("TipoIdentificacion", back_populates="usuarios")
    
    def __repr__(self):
        return f"<User(id={self.usuario_id}, email={self.correo}, role={self.role.nombre if self.role else 'None'})>"
    
    def to_dict(self, include_password=False):
        user_dict = {
            "usuario_id": self.usuario_id,
            "nombre_completo": self.nombre_completo,
            "telefono": self.telefono,
            "correo": self.correo,
            "tipo_identificacion": self.tipo_identificacion,
            "numero_identificacion": self.numero_identificacion,
            "estado": self.estado.value if self.estado else None,
            "rol_id": self.rol_id,
            "foto_perfil": self.foto_perfil,
            "fecha_registro": self.fecha_registro.isoformat() if self.fecha_registro else None,
            "role": self.role.to_dict() if self.role else None,
            "tipo_identificacion_info": self.tipo_identificacion_rel.to_dict() if self.tipo_identificacion_rel else None
        }
        
        if include_password:
            user_dict["password_hash"] = self.password_hash
            
        return user_dict
    
    def is_admin(self) -> bool:
        """Verifica si el usuario es administrador"""
        return self.role and self.role.nombre == "admin"
    
    def is_active(self) -> bool:
      """Verifica si el usuario está activo"""
      return self.estado == "activo" 