from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.auth.auth_handler import get_current_user
from app.models.user import User
from app.schemas.cotizacion import *
from app.controllers.cotizacion_controller import CotizacionController

router = APIRouter(prefix="/api/v1/cotizaciones", tags=["Cotizaciones"])

@router.post("/", response_model=CotizacionResponse, status_code=status.HTTP_201_CREATED)
async def crear_cotizacion(
    cotizacion_data: CotizacionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Crear una nueva cotización
    
    - **cliente_id**: ID del cliente
    - **automovil_id**: ID del automóvil
    - **descripcion_general**: Descripción general del servicio
    - **items**: Lista de servicios incluidos en la cotización
    """
    cotizacion = CotizacionController.crear_cotizacion(db, cotizacion_data, current_user.id)
    
    # Enriquecer respuesta con información relacionada
    response = CotizacionResponse.from_orm(cotizacion)
    if cotizacion.cliente:
        response.cliente_nombre = f"{cotizacion.cliente.nombre} {cotizacion.cliente.apellido}"
    if cotizacion.automovil:
        response.automovil_info = f"{cotizacion.automovil.marca} {cotizacion.automovil.modelo} - {cotizacion.automovil.placa}"
    if cotizacion.empleado:
        response.empleado_nombre = f"{cotizacion.empleado.nombre} {cotizacion.empleado.apellido}"
    
    return response

@router.get("/", response_model=List[CotizacionResponse])
async def listar_cotizaciones(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(50, ge=1, le=100, description="Límite de registros a devolver"),
    estado: Optional[EstadoCotizacion] = Query(None, description="Filtrar por estado"),
    cliente_id: Optional[int] = Query(None, description="Filtrar por cliente"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Listar cotizaciones con filtros opcionales
    """
    cotizaciones = CotizacionController.obtener_cotizaciones(db, skip, limit, estado, cliente_id)
    
    # Enriquecer respuestas
    response_list = []
    for cotizacion in cotizaciones:
        response = CotizacionResponse.from_orm(cotizacion)
        if cotizacion.cliente:
            response.cliente_nombre = f"{cotizacion.cliente.nombre} {cotizacion.cliente.apellido}"
        if cotizacion.automovil:
            response.automovil_info = f"{cotizacion.automovil.marca} {cotizacion.automovil.modelo} - {cotizacion.automovil.placa}"
        if cotizacion.empleado:
            response.empleado_nombre = f"{cotizacion.empleado.nombre} {cotizacion.empleado.apellido}"
        response_list.append(response)
    
    return response_list

@router.get("/{cotizacion_id}", response_model=CotizacionResponse)
async def obtener_cotizacion(
    cotizacion_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener una cotización específica por ID
    """
    cotizacion = CotizacionController.obtener_cotizacion_por_id(db, cotizacion_id)
    
    # Enriquecer respuesta
    response = CotizacionResponse.from_orm(cotizacion)
    if cotizacion.cliente:
        response.cliente_nombre = f"{cotizacion.cliente.nombre} {cotizacion.cliente.apellido}"
    if cotizacion.automovil:
        response.automovil_info = f"{cotizacion.automovil.marca} {cotizacion.automovil.modelo} - {cotizacion.automovil.placa}"
    if cotizacion.empleado:
        response.empleado_nombre = f"{cotizacion.empleado.nombre} {cotizacion.empleado.apellido}"
    
    return response

@router.put("/{cotizacion_id}", response_model=CotizacionResponse)
async def actualizar_cotizacion(
    cotizacion_id: int,
    cotizacion_data: CotizacionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Actualizar una cotización existente (solo en estado BORRADOR)
    """
    cotizacion = CotizacionController.actualizar_cotizacion(db, cotizacion_id, cotizacion_data)
    
    # Enriquecer respuesta
    response = CotizacionResponse.from_orm(cotizacion)
    if cotizacion.cliente:
        response.cliente_nombre = f"{cotizacion.cliente.nombre} {cotizacion.cliente.apellido}"
    if cotizacion.automovil:
        response.automovil_info = f"{cotizacion.automovil.marca} {cotizacion.automovil.modelo} - {cotizacion.automovil.placa}"
    if cotizacion.empleado:
        response.empleado_nombre = f"{cotizacion.empleado.nombre} {cotizacion.empleado.apellido}"
    
    return response

@router.patch("/{cotizacion_id}/estado", response_model=CotizacionResponse)
async def cambiar_estado_cotizacion(
    cotizacion_id: int,
    estado_data: CambiarEstadoRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cambiar el estado de una cotización
    
    Estados disponibles:
    - BORRADOR → ENVIADA
    - ENVIADA → ACEPTADA, RECHAZADA, VENCIDA
    - ACEPTADA → CONVERTIDA
    """
    cotizacion = CotizacionController.cambiar_estado_cotizacion(
        db, cotizacion_id, estado_data.nuevo_estado
    )
    
    # Enriquecer respuesta
    response = CotizacionResponse.from_orm(cotizacion)
    if cotizacion.cliente:
        response.cliente_nombre = f"{cotizacion.cliente.nombre} {cotizacion.cliente.apellido}"
    if cotizacion.automovil:
        response.automovil_info = f"{cotizacion.automovil.marca} {cotizacion.automovil.modelo} - {cotizacion.automovil.placa}"
    if cotizacion.empleado:
        response.empleado_nombre = f"{cotizacion.empleado.nombre} {cotizacion.empleado.apellido}"
    
    return response

@router.delete("/{cotizacion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_cotizacion(
    cotizacion_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Eliminar una cotización (solo en estado BORRADOR)
    """
    CotizacionController.eliminar_cotizacion(db, cotizacion_id)

@router.get("/cliente/{cliente_id}", response_model=List[CotizacionResponse])
async def obtener_cotizaciones_por_cliente(
    cliente_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener todas las cotizaciones de un cliente específico
    """
    cotizaciones = CotizacionController.obtener_cotizaciones(db, skip, limit, cliente_id=cliente_id)
    
    # Enriquecer respuestas
    response_list = []
    for cotizacion in cotizaciones:
        response = CotizacionResponse.from_orm(cotizacion)
        if cotizacion.cliente:
            response.cliente_nombre = f"{cotizacion.cliente.nombre} {cotizacion.cliente.apellido}"
        if cotizacion.automovil:
            response.automovil_info = f"{cotizacion.automovil.marca} {cotizacion.automovil.modelo} - {cotizacion.automovil.placa}"
        if cotizacion.empleado:
            response.empleado_nombre = f"{cotizacion.empleado.nombre} {cotizacion.empleado.apellido}"
        response_list.append(response)
    
    return response_list

@router.get("/estadisticas/dashboard", response_model=EstadisticasCotizaciones)
async def obtener_estadisticas_cotizaciones(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener estadísticas generales de cotizaciones para el dashboard
    """
    return CotizacionController.obtener_estadisticas(db)