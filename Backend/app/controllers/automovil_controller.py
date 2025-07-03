# app/controllers/automovil_controller.py

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from app.models.automovil import Automovil, EstadoAutomovil
from app.models.user import User
from app.schemas.automovil import (
    AutomovilCreate, AutomovilUpdate, AutomovilFiltros, 
    CambioEstadoAutomovil, ActualizarKilometraje
)
from fastapi import HTTPException, status
from typing import List, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class AutomovilController:
    
    @staticmethod
    def crear_automovil(db: Session, automovil_data: AutomovilCreate, current_user: User) -> Automovil:
        """Crear un nuevo automóvil"""
        try:
            # Verificar que la placa no exista
            automovil_existente = db.query(Automovil).filter(
                Automovil.placa == automovil_data.placa.upper().strip()
            ).first()
            
            if automovil_existente:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe un automóvil con la placa {automovil_data.placa}"
                )
            
            # Verificar VIN si se proporciona
            if automovil_data.vin:
                vin_existente = db.query(Automovil).filter(
                    Automovil.vin == automovil_data.vin.upper().strip()
                ).first()
                
                if vin_existente:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Ya existe un automóvil con el VIN {automovil_data.vin}"
                    )
            
            # Verificar que el propietario existe y está activo
            propietario = db.query(User).filter(
                and_(User.id == automovil_data.propietario_id, User.activo == True)
            ).first()
            
            if not propietario:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Propietario no encontrado o inactivo"
                )
            
            # Solo admin puede asignar automóviles a otros usuarios
            if current_user.rol.nombre != "Administrador" and automovil_data.propietario_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tiene permisos para asignar automóviles a otros usuarios"
                )
            
            # Crear el automóvil
            nuevo_automovil = Automovil(**automovil_data.dict())
            nuevo_automovil.placa = nuevo_automovil.placa.upper().strip()
            if nuevo_automovil.vin:
                nuevo_automovil.vin = nuevo_automovil.vin.upper().strip()
            
            db.add(nuevo_automovil)
            db.commit()
            db.refresh(nuevo_automovil)
            
            logger.info(f"Automóvil creado: {nuevo_automovil.placa} por usuario {current_user.id}")
            return nuevo_automovil
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error al crear automóvil: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor al crear el automóvil"
            )
    
    @staticmethod
    def obtener_automoviles(
        db: Session, 
        current_user: User,
        filtros: Optional[AutomovilFiltros] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> tuple[List[Automovil], int]:
        """Obtener lista de automóviles con filtros y paginación"""
        try:
            query = db.query(Automovil).join(User)
            
            # Filtrar por rol del usuario
            if current_user.rol.nombre == "Cliente":
                query = query.filter(Automovil.propietario_id == current_user.id)
            elif current_user.rol.nombre == "Empleado":
                # Los empleados pueden ver todos los automóviles activos
                query = query.filter(Automovil.estado != EstadoAutomovil.INACTIVO)
            
            # Aplicar filtros
            if filtros:
                if filtros.placa:
                    query = query.filter(Automovil.placa.ilike(f"%{filtros.placa}%"))
                if filtros.marca:
                    query = query.filter(Automovil.marca.ilike(f"%{filtros.marca}%"))
                if filtros.modelo:
                    query = query.filter(Automovil.modelo.ilike(f"%{filtros.modelo}%"))
                if filtros.año_min:
                    query = query.filter(Automovil.año >= filtros.año_min)
                if filtros.año_max:
                    query = query.filter(Automovil.año <= filtros.año_max)
                if filtros.estado:
                    query = query.filter(Automovil.estado == filtros.estado)
                if filtros.propietario_id:
                    query = query.filter(Automovil.propietario_id == filtros.propietario_id)
                if filtros.tipo_combustible:
                    query = query.filter(Automovil.tipo_combustible == filtros.tipo_combustible)
                if filtros.tipo_transmision:
                    query = query.filter(Automovil.tipo_transmision == filtros.tipo_transmision)
            
            # Contar total
            total = query.count()
            
            # Aplicar paginación y ordenamiento
            automoviles = query.order_by(desc(Automovil.created_at)).offset(skip).limit(limit).all()
            
            return automoviles, total
            
        except Exception as e:
            logger.error(f"Error al obtener automóviles: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor al obtener automóviles"
            )
    
    @staticmethod
    def obtener_automovil_por_id(db: Session, automovil_id: int, current_user: User) -> Automovil:
        """Obtener un automóvil específico por ID"""
        try:
            query = db.query(Automovil).filter(Automovil.id == automovil_id)
            
            # Filtrar por rol del usuario
            if current_user.rol.nombre == "Cliente":
                query = query.filter(Automovil.propietario_id == current_user.id)
            
            automovil = query.first()
            
            if not automovil:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Automóvil no encontrado"
                )
            
            return automovil
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error al obtener automóvil por ID: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor al obtener el automóvil"
            )
    
    @staticmethod
    def obtener_automovil_por_placa(db: Session, placa: str, current_user: User) -> Automovil:
        """Obtener un automóvil por placa"""
        try:
            query = db.query(Automovil).filter(Automovil.placa == placa.upper().strip())
            
            # Filtrar por rol del usuario
            if current_user.rol.nombre == "Cliente":
                query = query.filter(Automovil.propietario_id == current_user.id)
            
            automovil = query.first()
            
            if not automovil:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Automóvil con placa {placa} no encontrado"
                )
            
            return automovil
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error al obtener automóvil por placa: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor al obtener el automóvil"
            )
    
    @staticmethod
    def actualizar_automovil(
        db: Session, 
        automovil_id: int, 
        automovil_data: AutomovilUpdate, 
        current_user: User
    ) -> Automovil:
        """Actualizar un automóvil"""
        try:
            automovil = AutomovilController.obtener_automovil_por_id(db, automovil_id, current_user)
            
            # Solo admin o el propietario pueden actualizar
            if (current_user.rol.nombre not in ["Administrador", "Empleado"] and 
                automovil.propietario_id != current_user.id):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tiene permisos para actualizar este automóvil"
                )
            
            # Verificar placa única si se está actualizando
            if automovil_data.placa and automovil_data.placa != automovil.placa:
                placa_existente = db.query(Automovil).filter(
                    and_(
                        Automovil.placa == automovil_data.placa.upper().strip(),
                        Automovil.id != automovil_id
                    )
                ).first()
                
                if placa_existente:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Ya existe un automóvil con la placa {automovil_data.placa}"
                    )
            
            # Verificar VIN único si se está actualizando
            if automovil_data.vin and automovil_data.vin != automovil.vin:
                vin_existente = db.query(Automovil).filter(
                    and_(
                        Automovil.vin == automovil_data.vin.upper().strip(),
                        Automovil.id != automovil_id
                    )
                ).first()
                
                if vin_existente:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Ya existe un automóvil con el VIN {automovil_data.vin}"
                    )
            
            # Actualizar campos
            update_data = automovil_data.dict(exclude_unset=True)
            
            for field, value in update_data.items():
                if field == "placa" and value:
                    setattr(automovil, field, value.upper().strip())
                elif field == "vin" and value:
                    setattr(automovil, field, value.upper().strip())
                else:
                    setattr(automovil, field, value)
            
            automovil.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(automovil)
            
            logger.info(f"Automóvil actualizado: {automovil.placa} por usuario {current_user.id}")
            return automovil
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error al actualizar automóvil: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor al actualizar el automóvil"
            )
    
    @staticmethod
    def cambiar_estado_automovil(
        db: Session, 
        automovil_id: int, 
        cambio_estado: CambioEstadoAutomovil, 
        current_user: User
    ) -> Automovil:
        """Cambiar el estado de un automóvil"""
        try:
            # Solo admin y empleados pueden cambiar estados
            if current_user.rol.nombre not in ["Administrador", "Empleado"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tiene permisos para cambiar el estado del automóvil"
                )
            
            automovil = AutomovilController.obtener_automovil_por_id(db, automovil_id, current_user)
            
            estado_anterior = automovil.estado
            automovil.estado = cambio_estado.estado
            
            if cambio_estado.observaciones:
                observaciones_actuales = automovil.observaciones or ""
                nueva_observacion = f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Estado cambiado de {estado_anterior} a {cambio_estado.estado}: {cambio_estado.observaciones}"
                automovil.observaciones = f"{observaciones_actuales}\n{nueva_observacion}".strip()
            
            automovil.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(automovil)
            
            logger.info(f"Estado del automóvil {automovil.placa} cambiado de {estado_anterior} a {cambio_estado.estado} por usuario {current_user.id}")
            return automovil
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error al cambiar estado del automóvil: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor al cambiar el estado"
            )
    
    @staticmethod
    def actualizar_kilometraje(
        db: Session, 
        automovil_id: int, 
        datos_kilometraje: ActualizarKilometraje, 
        current_user: User
    ) -> Automovil:
        """Actualizar el kilometraje de un automóvil"""
        try:
            automovil = AutomovilController.obtener_automovil_por_id(db, automovil_id, current_user)
            
            # Verificar que el nuevo kilometraje sea mayor al actual
            if datos_kilometraje.kilometraje_actual < automovil.kilometraje_actual:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El nuevo kilometraje no puede ser menor al actual"
                )
            
            kilometraje_anterior = automovil.kilometraje_actual
            automovil.kilometraje_actual = datos_kilometraje.kilometraje_actual
            
            # Agregar observación del cambio de kilometraje
            if datos_kilometraje.observaciones:
                observaciones_actuales = automovil.observaciones or ""
                nueva_observacion = f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Kilometraje actualizado de {kilometraje_anterior} a {datos_kilometraje.kilometraje_actual} km: {datos_kilometraje.observaciones}"
                automovil.observaciones = f"{observaciones_actuales}\n{nueva_observacion}".strip()
            
            automovil.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(automovil)
            
            logger.info(f"Kilometraje actualizado para automóvil {automovil.placa}: {kilometraje_anterior} -> {datos_kilometraje.kilometraje_actual} km por usuario {current_user.id}")
            return automovil
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error al actualizar kilometraje: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor al actualizar el kilometraje"
            )
    
    @staticmethod
    def eliminar_automovil(db: Session, automovil_id: int, current_user: User) -> bool:
        """Eliminar un automóvil (eliminación lógica)"""
        try:
            # Solo admin puede eliminar automóviles
            if current_user.rol.nombre != "Administrador":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tiene permisos para eliminar automóviles"
                )
            
            automovil = AutomovilController.obtener_automovil_por_id(db, automovil_id, current_user)
            
            # Eliminación lógica: cambiar estado a INACTIVO
            automovil.estado = EstadoAutomovil.INACTIVO
            automovil.updated_at = datetime.utcnow()
            
            # Agregar observación de eliminación
            observaciones_actuales = automovil.observaciones or ""
            nueva_observacion = f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Automóvil eliminado por usuario {current_user.nombre_completo}"
            automovil.observaciones = f"{observaciones_actuales}\n{nueva_observacion}".strip()
            
            db.commit()
            
            logger.info(f"Automóvil eliminado (lógicamente): {automovil.placa} por usuario {current_user.id}")
            return True
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error al eliminar automóvil: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor al eliminar el automóvil"
            )
    
    @staticmethod
    def obtener_historial_automovil(db: Session, automovil_id: int, current_user: User) -> dict:
        """Obtener el historial completo de un automóvil"""
        try:
            automovil = AutomovilController.obtener_automovil_por_id(db, automovil_id, current_user)
            
            # Crear historial desde las observaciones
            historial = []
            if automovil.observaciones:
                observaciones_list = automovil.observaciones.split('\n')
                for obs in observaciones_list:
                    if obs.strip():
                        historial.append({
                            "fecha": obs[:19] if obs.startswith('[') else datetime.now().strftime('%Y-%m-%d %H:%M'),
                            "descripcion": obs.strip()
                        })
            
            return {
                "automovil_id": automovil.id,
                "placa": automovil.placa,
                "marca": automovil.marca,
                "modelo": automovil.modelo,
                "año": automovil.año,
                "propietario": automovil.propietario.nombre_completo,
                "estado_actual": automovil.estado.value,
                "kilometraje_actual": automovil.kilometraje_actual,
                "fecha_registro": automovil.created_at,
                "ultima_actualizacion": automovil.updated_at,
                "historial": historial
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error al obtener historial del automóvil: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor al obtener el historial"
            )
    
    @staticmethod
    def obtener_estadisticas_automoviles(db: Session, current_user: User) -> dict:
        """Obtener estadísticas de los automóviles"""
        try:
            # Solo admin y empleados pueden ver estadísticas completas
            if current_user.rol.nombre == "Cliente":
                query = db.query(Automovil).filter(Automovil.propietario_id == current_user.id)
            else:
                query = db.query(Automovil)
            
            # Contar por estado
            total_automoviles = query.count()
            activos = query.filter(Automovil.estado == EstadoAutomovil.ACTIVO).count()
            en_servicio = query.filter(Automovil.estado == EstadoAutomovil.EN_SERVICIO).count()
            en_reparacion = query.filter(Automovil.estado == EstadoAutomovil.EN_REPARACION).count()
            inactivos = query.filter(Automovil.estado == EstadoAutomovil.INACTIVO).count()
            
            # Estadísticas por marca
            marcas = db.query(
                Automovil.marca, 
                func.count(Automovil.id).label('cantidad')
            ).group_by(Automovil.marca).all()
            
            # Estadísticas por año
            años = db.query(
                Automovil.año, 
                func.count(Automovil.id).label('cantidad')
            ).group_by(Automovil.año).order_by(desc(Automovil.año)).limit(10).all()
            
            return {
                "total_automoviles": total_automoviles,
                "estados": {
                    "activos": activos,
                    "en_servicio": en_servicio,
                    "en_reparacion": en_reparacion,
                    "inactivos": inactivos
                },
                "por_marca": [{"marca": marca, "cantidad": cantidad} for marca, cantidad in marcas],
                "por_año": [{"año": año, "cantidad": cantidad} for año, cantidad in años],
                "fecha_consulta": datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"Error al obtener estadísticas de automóviles: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor al obtener estadísticas"
            )