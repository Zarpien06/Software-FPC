# app/models/tipo_identificacion.py
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.database import Base

class TipoIdentificacion(Base):
    __tablename__ = "tipos_identificacion"
    
    tipo_id = Column(String(2), primary_key=True, index=True)
    descripcion = Column(String(50), nullable=False)
    
    # Relación con usuarios, usando el atributo relationship del User
    usuarios = relationship(
        "Usuario",
        back_populates="tipo_identificacion_rel"
    )
    
    def __repr__(self):
        return f"<TipoIdentificacion(tipo_id={self.tipo_id}, descripcion={self.descripcion})>"
    
    def to_dict(self):
        return {
            "tipo_id": self.tipo_id,
            "descripcion": self.descripcion
        }
