# app/models/user.py
from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.database import Base

class EstadoUsuario(PyEnum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"

class Usuario(Base):
    __tablename__ = "usuarios"

    usuario_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_completo = Column(String(100), nullable=False)
    telefono = Column(String(15), nullable=True)
    correo = Column(String(100), unique=True, nullable=False, index=True)
    tipo_identificacion = Column(String(2), ForeignKey("tipos_identificacion.tipo_id"), nullable=False)
    numero_identificacion = Column(String(20), nullable=False)
    password_hash = Column(String(255), nullable=False)

    estado = Column(
        Enum(EstadoUsuario, name="estadousuario"),
        default=EstadoUsuario.ACTIVO,
        nullable=False
    )

    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    foto_perfil = Column(String(255), default="static/img/default-profile.png")
    fecha_registro = Column(TIMESTAMP, server_default=func.current_timestamp())

    # Relaciones básicas
    role = relationship("Role", back_populates="usuarios")
    tipo_identificacion_rel = relationship("TipoIdentificacion", back_populates="usuarios")
    automoviles = relationship("Automovil", back_populates="propietario", cascade="all, delete-orphan")
    cotizaciones = relationship("Cotizacion", back_populates="cliente", foreign_keys="Cotizacion.cliente_id")
    
    # Relaciones con Proceso
    procesos_como_tecnico = relationship(
        "Proceso",
        foreign_keys="Proceso.tecnico_responsable_id",
        back_populates="tecnico_responsable"
    )
    
    procesos_como_inspector = relationship(
        "Proceso",
        foreign_keys="Proceso.inspector_id",
        back_populates="inspector"
    )
    
    procesos_como_cliente = relationship(
        "Proceso",
        foreign_keys="Proceso.cliente_id",
        back_populates="cliente"
    )
    
    # *** RELACIONES FALTANTES AGREGADAS ***
    # Relaciones con HistorialServicio
    servicios_como_tecnico = relationship(
        "HistorialServicio",
        foreign_keys="HistorialServicio.tecnico_id",
        back_populates="tecnico"
    )
    
    servicios_como_cliente = relationship(
        "HistorialServicio",
        foreign_keys="HistorialServicio.cliente_id",
        back_populates="cliente"
    )
    
    # Relaciones adicionales para auditoría (sin back_populates para evitar conflictos)
    procesos_creados = relationship(
        "Proceso",
        foreign_keys="Proceso.creado_por",
        viewonly=True  # Solo lectura para evitar conflictos
    )
    
    procesos_actualizados = relationship(
        "Proceso",
        foreign_keys="Proceso.actualizado_por",
        viewonly=True  # Solo lectura para evitar conflictos
    )

    def __repr__(self):
        rol_nombre = self.role.nombre if self.role else 'None'
        return f"<Usuario(id={self.usuario_id}, email={self.correo}, role={rol_nombre})>"

    def to_dict(self, include_password=False):
        user_dict = {
            "usuario_id": self.usuario_id,
            "nombre_completo": self.nombre_completo,
            "telefono": self.telefono,
            "correo": self.correo,
            "tipo_identificacion": self.tipo_identificacion,
            "numero_identificacion": self.numero_identificacion,
            "estado": self.estado.value,
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
        return self.role and self.role.nombre.lower() == "admin"

    def is_active(self) -> bool:
        return self.estado == EstadoUsuario.ACTIVO

    # Métodos de utilidad para trabajar con procesos
    def get_procesos_activos_como_tecnico(self):
        """Obtiene los procesos activos donde este usuario es técnico responsable"""
        return [p for p in self.procesos_como_tecnico if p.activo and p.estado.name != 'COMPLETADO']
    
    def get_procesos_pendientes_inspeccion(self):
        """Obtiene los procesos pendientes de inspección donde este usuario es inspector"""
        return [p for p in self.procesos_como_inspector if p.requiere_inspeccion and not p.inspeccion_realizada]
    
    def get_historial_procesos_como_cliente(self):
        """Obtiene el historial de procesos donde este usuario es cliente"""
        return self.procesos_como_cliente

    # *** MÉTODOS ADICIONALES PARA HISTORIAL DE SERVICIOS ***
    def get_servicios_como_tecnico(self):
        """Obtiene todos los servicios donde este usuario es técnico"""
        return self.servicios_como_tecnico
    
    def get_servicios_como_cliente(self):
        """Obtiene todos los servicios donde este usuario es cliente"""
        return self.servicios_como_cliente

# Alias para compatibilidad
User = Usuario