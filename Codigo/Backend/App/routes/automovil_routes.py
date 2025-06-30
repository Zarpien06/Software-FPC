# app/routes/automovil_routes.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.user import User
from app.schemas.automovil import (
    AutomovilCreate, AutomovilUpdate, AutomovilResponse, 
    AutomovilFiltros, CambioEstadoAutomovil, ActualizarKilometraje,
    AutomovilPaginado, AutomovilHistorialResponse, AutomovilEstadisticasResponse
)
from app.controllers.automovil_controller import AutomovilController
from app.auth.auth_handler import get_current_user
import logging

logger = logging.getLogger(__name__)

# Crear router para automóviles
router = APIRouter(
    prefix="/automoviles",
    tags=["Automóviles"],
    responses={
        404: {"description": "Automóvil no encontrado"},
        403: {"description": "Sin permisos suficientes"},
        400: {"description": "Datos inválidos"}
    }
)

@router.post(
    "/",
    response_model=AutomovilResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo automóvil",
    description="Registra un nuevo automóvil en el sistema. Solo admins pueden asignar automóviles a otros usuarios."
)
async def crear_automovil(
    automovil_data: AutomovilCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Crear un nuevo automóvil:
    
    - **placa**: Placa del vehículo (único, se convierte a mayúsculas)
    - **marca**: Marca del automóvil
    - **modelo**: Modelo del automóvil
    - **año**: Año del vehículo
    - **propietario_id**: ID del propietario (si no se especifica, se asigna al usuario actual)
    - **vin**: VIN del vehículo (opcional, único)
    - **color**: Color del automóvil
    - **tipo_combustible**: Tipo de combustible
    - **tipo_transmision**: Tipo de transmisión
    - **cilindrada**: Cilindrada del motor
    - **kilometraje_actual**: Kilometraje actual del vehículo
    
    Permisos:
    - Clientes: Solo pueden registrar automóviles para sí mismos
    - Empleados/Admins: Pueden registrar automóviles para cualquier usuario
    """
    try:
        # Si no se especifica propietario, asignar al usuario actual
        if not automovil_data.propietario_id:
            automovil_data.propietario_id = current_user.id
            
        automovil = AutomovilController.crear_automovil(db, automovil_data, current_user)
        
        logger.info(f"Automóvil creado exitosamente: {automovil.placa} por usuario {current_user.id}")
        return automovil
        
    except Exception as e:
        logger.error(f"Error en endpoint crear_automovil: {str(e)}")
        raise

@router.get(
    "/",
    response_model=AutomovilPaginado,
    summary="Listar automóviles",
    description="Obtiene la lista de automóviles con filtros opcionales y paginación."
)
async def listar_automoviles(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=500, description="Límite de registros por página"),
    placa: Optional[str] = Query(None, description="Filtrar por placa (búsqueda parcial)"),
    marca: Optional[str] = Query(None, description="Filtrar por marca"),
    modelo: Optional[str] = Query(None, description="Filtrar por modelo"),
    año_min: Optional[int] = Query(None, ge=1900, description="Año mínimo"),
    año_max: Optional[int] = Query(None, le=2030, description="Año máximo"),
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    propietario_id: Optional[int] = Query(None, description="Filtrar por ID del propietario"),
    tipo_combustible: Optional[str] = Query(None, description="Filtrar por tipo de combustible"),
    tipo_transmision: Optional[str] = Query(None, description="Filtrar por tipo de transmisión"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Listar automóviles con filtros:
    
    Filtros disponibles:
    - **placa**: Búsqueda parcial por placa
    - **marca**: Filtrar por marca exacta
    - **modelo**: Filtrar por modelo exacto
    - **año_min/año_max**: Rango de años
    - **estado**: Filtrar por estado del automóvil
    - **propietario_id**: Filtrar por propietario
    - **tipo_combustible**: Filtrar por tipo de combustible
    - **tipo_transmision**: Filtrar por tipo de transmisión
    
    Permisos:
    - Clientes: Solo ven sus propios automóviles
    - Empleados: Ven todos los automóviles activos
    - Admins: Ven todos los automóviles
    """
    try:
        # Crear objeto de filtros
        filtros = AutomovilFiltros(
            placa=placa,
            marca=marca,
            modelo=modelo,
            año_min=año_min,
            año_max=año_max,
            estado=estado,
            propietario_id=propietario_id,
            tipo_combustible=tipo_combustible,
            tipo_transmision=tipo_transmision
        )
        
        automoviles, total = AutomovilController.obtener_automoviles(
            db, current_user, filtros, skip, limit
        )
        
        return AutomovilPaginado(  
       items=automoviles,  
       total=total,
       page=skip // limit + 1,  
       per_page=limit,         
       total_pages=(total + limit - 1) // limit, 
       has_next=skip + limit < total,
       has_prev=skip > 0
   )
        
    except Exception as e:
        logger.error(f"Error en endpoint listar_automoviles: {str(e)}")
        raise

@router.get(
    "/{automovil_id}",
    response_model=AutomovilResponse,
    summary="Obtener automóvil por ID",
    description="Obtiene la información detallada de un automóvil específico."
)
async def obtener_automovil(
    automovil_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener información detallada de un automóvil:
    
    - Devuelve todos los datos del automóvil
    - Incluye información del propietario
    - Muestra historial de cambios en observaciones
    
    Permisos:
    - Clientes: Solo pueden ver sus propios automóviles
    - Empleados/Admins: Pueden ver cualquier automóvil
    """
    try:
        automovil = AutomovilController.obtener_automovil_por_id(db, automovil_id, current_user)
        
        if not automovil:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Automóvil no encontrado"
            )
        
        return automovil
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en endpoint obtener_automovil: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.put(
    "/{automovil_id}",
    response_model=AutomovilResponse,
    summary="Actualizar automóvil",
    description="Actualiza la información de un automóvil existente."
)
async def actualizar_automovil(
    automovil_id: int,
    automovil_data: AutomovilUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Actualizar información de un automóvil:
    
    - Se pueden actualizar todos los campos excepto la placa (contactar admin)
    - Solo se actualizan los campos proporcionados
    - Mantiene historial de cambios en observaciones
    
    Permisos:
    - Clientes: Solo pueden actualizar sus propios automóviles
    - Empleados/Admins: Pueden actualizar cualquier automóvil
    """
    try:
        automovil = AutomovilController.actualizar_automovil(db, automovil_id, automovil_data, current_user)
        
        if not automovil:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Automóvil no encontrado"
            )
        
        logger.info(f"Automóvil {automovil.placa} actualizado por usuario {current_user.id}")
        return automovil
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en endpoint actualizar_automovil: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.delete(
    "/{automovil_id}",
    summary="Eliminar automóvil",
    description="Elimina un automóvil del sistema (eliminación lógica)."
)
async def eliminar_automovil(
    automovil_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Eliminar un automóvil:
    
    - Eliminación lógica (marca como inactivo)
    - Solo admins pueden eliminar automóviles
    - Se mantiene el historial para auditoría
    
    Permisos:
    - Solo Administradores pueden eliminar automóviles
    """
    try:
        success = AutomovilController.eliminar_automovil(db, automovil_id, current_user)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Automóvil no encontrado"
            )
        
        logger.info(f"Automóvil ID {automovil_id} eliminado por usuario {current_user.id}")
        return {"message": "Automóvil eliminado exitosamente"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en endpoint eliminar_automovil: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.patch(
    "/{automovil_id}/estado",
    response_model=AutomovilResponse,
    summary="Cambiar estado del automóvil",
    description="Cambia el estado de un automóvil (activo, en servicio, etc.)."
)
async def cambiar_estado_automovil(
    automovil_id: int,
    cambio_estado: CambioEstadoAutomovil,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cambiar estado de un automóvil:
    
    Estados disponibles:
    - **activo**: Vehículo disponible
    - **en_servicio**: Vehículo en reparación/mantenimiento
    - **inactivo**: Vehículo temporalmente fuera de servicio
    - **vendido**: Vehículo vendido
    - **siniestrado**: Vehículo accidentado
    
    Permisos:
    - Empleados/Admins: Pueden cambiar cualquier estado
    - Clientes: Solo pueden marcar como "en_servicio" sus propios vehículos
    """
    try:
        automovil = AutomovilController.cambiar_estado_automovil(
            db, automovil_id, cambio_estado, current_user
        )
        
        if not automovil:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Automóvil no encontrado"
            )
        
        logger.info(f"Estado del automóvil {automovil.placa} cambiado a {cambio_estado.nuevo_estado} por usuario {current_user.id}")
        return automovil
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en endpoint cambiar_estado_automovil: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.patch(
    "/{automovil_id}/kilometraje",
    response_model=AutomovilResponse,
    summary="Actualizar kilometraje",
    description="Actualiza el kilometraje actual del automóvil."
)
async def actualizar_kilometraje(
    automovil_id: int,
    kilometraje_data: ActualizarKilometraje,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Actualizar kilometraje del automóvil:
    
    - El nuevo kilometraje debe ser mayor al actual
    - Se registra la fecha de actualización
    - Útil para registros de mantenimiento
    
    Permisos:
    - Propietarios: Pueden actualizar el kilometraje de sus vehículos
    - Empleados/Admins: Pueden actualizar cualquier vehículo
    """
    try:
        automovil = AutomovilController.actualizar_kilometraje(
            db, automovil_id, kilometraje_data, current_user
        )
        
        if not automovil:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Automóvil no encontrado"
            )
        
        logger.info(f"Kilometraje del automóvil {automovil.placa} actualizado a {kilometraje_data.nuevo_kilometraje} por usuario {current_user.id}")
        return automovil
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en endpoint actualizar_kilometraje: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get(
    "/{automovil_id}/historial",
    response_model=AutomovilHistorialResponse,
    summary="Obtener historial del automóvil",
    description="Obtiene el historial completo de servicios y cambios del automóvil."
)
async def obtener_historial_automovil(
    automovil_id: int,
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(50, ge=1, le=200, description="Límite de registros por página"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener historial completo del automóvil:
    
    - Historial de servicios y mantenimientos
    - Cambios de estado
    - Actualizaciones de kilometraje
    - Observaciones y notas
    
    Permisos:
    - Propietarios: Pueden ver el historial de sus vehículos
    - Empleados/Admins: Pueden ver cualquier historial
    """
    try:
        historial = AutomovilController.obtener_historial_automovil(
            db, automovil_id, current_user, skip, limit
        )
        
        if not historial:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Automóvil no encontrado o sin historial"
            )
        
        return historial
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en endpoint obtener_historial_automovil: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get(
    "/estadisticas/general",
    response_model=AutomovilEstadisticasResponse,
    summary="Obtener estadísticas de automóviles",
    description="Obtiene estadísticas generales sobre los automóviles en el sistema."
)
async def obtener_estadisticas_automoviles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener estadísticas generales:
    
    - Total de automóviles por estado
    - Distribución por marca y modelo
    - Estadísticas de kilometraje
    - Automóviles por año
    
    Permisos:
    - Empleados/Admins: Ven estadísticas completas
    - Clientes: Solo ven estadísticas de sus vehículos
    """
    try:
        estadisticas = AutomovilController.obtener_estadisticas(db, current_user)
        return estadisticas
        
    except Exception as e:
        logger.error(f"Error en endpoint obtener_estadisticas_automoviles: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get(
    "/buscar/{termino}",
    response_model=List[AutomovilResponse],
    summary="Buscar automóviles",
    description="Búsqueda rápida de automóviles por placa, marca, modelo o VIN."
)
async def buscar_automoviles(
    termino: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Búsqueda rápida de automóviles:
    
    - Busca en placa, marca, modelo y VIN
    - Búsqueda parcial no sensible a mayúsculas
    - Resultados limitados a 20 por rendimiento
    
    Permisos:
    - Empleados/Admins: Buscan en todos los automóviles
    - Clientes: Solo buscan en sus propios automóviles
    """
    try:
        if len(termino.strip()) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El término de búsqueda debe tener al menos 2 caracteres"
            )
        
        automoviles = AutomovilController.buscar_automoviles(db, termino, current_user)
        return automoviles
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en endpoint buscar_automoviles: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )