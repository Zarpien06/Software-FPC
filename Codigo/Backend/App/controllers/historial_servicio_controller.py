# 📁 app/controllers/historial_servicio_controller.py
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_, func
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import datetime, timedelta
import uuid

from app.models.historial_servicio import HistorialServicio, TipoMantenimiento, EstadoHistorial
from app.models.automovil import Automovil
from app.models.user import Usuario
from app.schemas.historial_servicio import (
    HistorialServicioCreate, 
    HistorialServicioUpdate, 
    HistorialServicioResponse,
    HistorialServicioFilter
)

class HistorialServicioController:
    """
    Controlador para gestionar operaciones CRUD del historial de servicios
    RF004 - Gestión de Procesos
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def crear_historial(self, historial_data: HistorialServicioCreate, usuario_id: str) -> HistorialServicio:
        """
        Crear un nuevo registro de historial de servicio
        """
        try:
            # Verificar que el automóvil existe
            automovil = self.db.query(Automovil).filter(Automovil.id == historial_data.automovil_id).first()
            if not automovil:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Automóvil no encontrado"
                )
            
            # Verificar que el técnico existe (si se proporciona)
            if historial_data.tecnico_id:
                tecnico = self.db.query(Usuario).filter(Usuario.id == historial_data.tecnico_id).first()
                if not tecnico:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Técnico no encontrado"
                    )
            
            # Crear nuevo historial
            nuevo_historial = HistorialServicio(
                id=str(uuid.uuid4()),
                automovil_id=historial_data.automovil_id,
                fecha_servicio=historial_data.fecha_servicio,
                tipo_mantenimiento=historial_data.tipo_mantenimiento,
                descripcion=historial_data.descripcion,
                kilometraje=historial_data.kilometraje,
                costo=historial_data.costo,
                tecnico_id=historial_data.tecnico_id,
                proveedor=historial_data.proveedor,
                repuestos_utilizados=historial_data.repuestos_utilizados,
                observaciones=historial_data.observaciones,
                proximo_mantenimiento_km=historial_data.proximo_mantenimiento_km,
                proximo_mantenimiento_fecha=historial_data.proximo_mantenimiento_fecha,
                estado=historial_data.estado or EstadoHistorial.COMPLETADO,
                created_by=usuario_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            self.db.add(nuevo_historial)
            self.db.commit()
            self.db.refresh(nuevo_historial)
            
            return nuevo_historial
            
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear historial de servicio: {str(e)}"
            )
    
    def obtener_historial_por_id(self, historial_id: str) -> HistorialServicio:
        """
        Obtener un historial específico por ID
        """
        historial = self.db.query(HistorialServicio).filter(
            HistorialServicio.id == historial_id,
            HistorialServicio.is_active == True
        ).first()
        
        if not historial:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Historial de servicio no encontrado"
            )
        
        return historial
    
    def obtener_historial_por_automovil(
        self, 
        automovil_id: str,
        skip: int = 0,
        limit: int = 100,
        filtros: Optional[HistorialServicioFilter] = None
    ) -> List[HistorialServicio]:
        """
        Obtener historial de servicios de un automóvil específico
        """
        query = self.db.query(HistorialServicio).filter(
            HistorialServicio.automovil_id == automovil_id,
            HistorialServicio.is_active == True
        )
        
        # Aplicar filtros si se proporcionan
        if filtros:
            if filtros.tipo_mantenimiento:
                query = query.filter(HistorialServicio.tipo_mantenimiento == filtros.tipo_mantenimiento)
            
            if filtros.estado:
                query = query.filter(HistorialServicio.estado == filtros.estado)
            
            if filtros.fecha_desde:
                query = query.filter(HistorialServicio.fecha_servicio >= filtros.fecha_desde)
            
            if filtros.fecha_hasta:
                query = query.filter(HistorialServicio.fecha_servicio <= filtros.fecha_hasta)
            
            if filtros.tecnico_id:
                query = query.filter(HistorialServicio.tecnico_id == filtros.tecnico_id)
            
            if filtros.costo_minimo:
                query = query.filter(HistorialServicio.costo >= filtros.costo_minimo)
            
            if filtros.costo_maximo:
                query = query.filter(HistorialServicio.costo <= filtros.costo_maximo)
        
        return query.order_by(desc(HistorialServicio.fecha_servicio)).offset(skip).limit(limit).all()
    
    def obtener_todos_historiales(
        self, 
        skip: int = 0, 
        limit: int = 100,
        filtros: Optional[HistorialServicioFilter] = None
    ) -> List[HistorialServicio]:
        """
        Obtener todos los historiales de servicio con filtros opcionales
        """
        query = self.db.query(HistorialServicio).filter(HistorialServicio.is_active == True)
        
        # Aplicar filtros si se proporcionan
        if filtros:
            if filtros.automovil_id:
                query = query.filter(HistorialServicio.automovil_id == filtros.automovil_id)
            
            if filtros.tipo_mantenimiento:
                query = query.filter(HistorialServicio.tipo_mantenimiento == filtros.tipo_mantenimiento)
            
            if filtros.estado:
                query = query.filter(HistorialServicio.estado == filtros.estado)
            
            if filtros.fecha_desde:
                query = query.filter(HistorialServicio.fecha_servicio >= filtros.fecha_desde)
            
            if filtros.fecha_hasta:
                query = query.filter(HistorialServicio.fecha_servicio <= filtros.fecha_hasta)
            
            if filtros.tecnico_id:
                query = query.filter(HistorialServicio.tecnico_id == filtros.tecnico_id)
            
            if filtros.costo_minimo:
                query = query.filter(HistorialServicio.costo >= filtros.costo_minimo)
            
            if filtros.costo_maximo:
                query = query.filter(HistorialServicio.costo <= filtros.costo_maximo)
        
        return query.order_by(desc(HistorialServicio.fecha_servicio)).offset(skip).limit(limit).all()
    
    def actualizar_historial(self, historial_id: str, historial_data: HistorialServicioUpdate, usuario_id: str) -> HistorialServicio:
        """
        Actualizar un registro de historial existente
        """
        try:
            historial = self.obtener_historial_por_id(historial_id)
            
            # Verificar automóvil si se está cambiando
            if historial_data.automovil_id and historial_data.automovil_id != historial.automovil_id:
                automovil = self.db.query(Automovil).filter(Automovil.id == historial_data.automovil_id).first()
                if not automovil:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Automóvil no encontrado"
                    )
            
            # Verificar técnico si se está cambiando
            if historial_data.tecnico_id:
                tecnico = self.db.query(Usuario).filter(Usuario.id == historial_data.tecnico_id).first()
                if not tecnico:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Técnico no encontrado"
                    )
            
            # Actualizar campos proporcionados
            update_data = historial_data.dict(exclude_unset=True)
            
            for field, value in update_data.items():
                if hasattr(historial, field):
                    setattr(historial, field, value)
            
            historial.updated_by = usuario_id
            historial.updated_at = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(historial)
            
            return historial
            
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar historial: {str(e)}"
            )
    
    def eliminar_historial(self, historial_id: str, usuario_id: str) -> bool:
        """
        Eliminar (desactivar) un registro de historial
        """
        try:
            historial = self.obtener_historial_por_id(historial_id)
            
            historial.is_active = False
            historial.updated_by = usuario_id
            historial.updated_at = datetime.utcnow()
            
            self.db.commit()
            return True
            
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al eliminar historial: {str(e)}"
            )
    
    def obtener_historial_por_tecnico(self, tecnico_id: str, skip: int = 0, limit: int = 100) -> List[HistorialServicio]:
        """
        Obtener historiales de servicio realizados por un técnico específico
        """
        return self.db.query(HistorialServicio).filter(
            HistorialServicio.tecnico_id == tecnico_id,
            HistorialServicio.is_active == True
        ).order_by(desc(HistorialServicio.fecha_servicio)).offset(skip).limit(limit).all()
    
    def obtener_proximos_mantenimientos(self, dias_adelanto: int = 30) -> List[HistorialServicio]:
        """
        Obtener vehículos que necesitan mantenimiento próximamente
        """
        fecha_limite = datetime.utcnow() + timedelta(days=dias_adelanto)
        
        return self.db.query(HistorialServicio).filter(
            HistorialServicio.is_active == True,
            HistorialServicio.proximo_mantenimiento_fecha <= fecha_limite,
            HistorialServicio.proximo_mantenimiento_fecha >= datetime.utcnow()
        ).order_by(HistorialServicio.proximo_mantenimiento_fecha).all()
    
    def obtener_estadisticas_mantenimiento(self, automovil_id: Optional[str] = None) -> dict:
        """
        Obtener estadísticas de mantenimiento
        """
        try:
            query = self.db.query(HistorialServicio).filter(HistorialServicio.is_active == True)
            
            if automovil_id:
                query = query.filter(HistorialServicio.automovil_id == automovil_id)
            
            # Estadísticas básicas
            total_servicios = query.count()
            costo_total = query.with_entities(func.sum(HistorialServicio.costo)).scalar() or 0
            costo_promedio = query.with_entities(func.avg(HistorialServicio.costo)).scalar() or 0
            
            # Servicios por tipo
            servicios_por_tipo = {}
            for tipo in TipoMantenimiento:
                count = query.filter(HistorialServicio.tipo_mantenimiento == tipo).count()
                servicios_por_tipo[tipo.value] = count
            
            # Servicios por estado
            servicios_por_estado = {}
            for estado in EstadoHistorial:
                count = query.filter(HistorialServicio.estado == estado).count()
                servicios_por_estado[estado.value] = count
            
            return {
                "total_servicios": total_servicios,
                "costo_total": float(costo_total),
                "costo_promedio": float(costo_promedio),
                "servicios_por_tipo": servicios_por_tipo,
                "servicios_por_estado": servicios_por_estado
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener estadísticas: {str(e)}"
            )