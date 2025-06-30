# app/models/automovil.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class EstadoAutomovil(str, enum.Enum):
    ACTIVO = "activo"
    EN_SERVICIO = "en_servicio" 
    INACTIVO = "inactivo"
    FUERA_DE_SERVICIO = "fuera_de_servicio"

class TipoCombustible(str, enum.Enum):
    GASOLINA = "gasolina"
    DIESEL = "diesel"
    GAS = "gas"
    ELECTRICO = "electrico"
    HIBRIDO = "hibrido"

class TipoTransmision(str, enum.Enum):
    MANUAL = "manual"
    AUTOMATICA = "automatica"
    SEMIAUTOMATICA = "semiautomatica"

class Automovil(Base):
    __tablename__ = "automoviles"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    placa = Column(String(10), unique=True, index=True, nullable=False)
    vin = Column(String(17), unique=True, index=True, nullable=True)
    
    marca = Column(String(50), nullable=False)
    modelo = Column(String(50), nullable=False)
    año = Column(Integer, nullable=False)
    color = Column(String(30), nullable=False)
    
    cilindraje = Column(Numeric(4, 1), nullable=True)
    numero_motor = Column(String(50), nullable=True)
    tipo_combustible = Column(Enum(TipoCombustible), nullable=False, default=TipoCombustible.GASOLINA)
    tipo_transmision = Column(Enum(TipoTransmision), nullable=False, default=TipoTransmision.MANUAL)
    
    kilometraje_actual = Column(Integer, nullable=False, default=0)
    kilometraje_ingreso = Column(Integer, nullable=True)
    
    estado = Column(Enum(EstadoAutomovil), nullable=False, default=EstadoAutomovil.ACTIVO)
    observaciones = Column(Text, nullable=True)
    
    propietario_id = Column(Integer, ForeignKey("usuarios.usuario_id"), nullable=False)
    propietario = relationship("Usuario", back_populates="automoviles")  # corregido aquí

    numero_puertas = Column(Integer, nullable=True)
    capacidad_pasajeros = Column(Integer, nullable=True)
    
    fecha_matricula = Column(DateTime(timezone=True), nullable=True)
    fecha_soat = Column(DateTime(timezone=True), nullable=True)
    fecha_tecnomecanica = Column(DateTime(timezone=True), nullable=True)
    
    procesos = relationship("Proceso", back_populates="automovil", cascade="all, delete-orphan")
    historial_servicios = relationship("HistorialServicio", back_populates="automovil", cascade="all, delete-orphan")
    cotizaciones = relationship("Cotizacion", back_populates="automovil")

    def __repr__(self):
        return f"<Automovil(id={self.id}, placa='{self.placa}', marca='{self.marca}', modelo='{self.modelo}')>"
    
    @property
    def nombre_completo(self):
        return f"{self.marca} {self.modelo} {self.año} - {self.placa}"
    
    @property
    def esta_activo(self):
        return self.estado == EstadoAutomovil.ACTIVO
    
    @property
    def esta_en_servicio(self):
        return self.estado == EstadoAutomovil.EN_SERVICIO
