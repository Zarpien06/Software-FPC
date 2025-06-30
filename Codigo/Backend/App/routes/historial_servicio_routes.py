# 📁 app/routes/historial_servicio_routes.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.auth.auth_handler import get_current_user
from app.models.user import Usuario
from app.controllers.historial_servicio_controller import HistorialServicioController
from app.schemas.historial_servicio import (
    HistorialServicioCreate,
    HistorialServicioUpdate,
    HistorialServicioResponse,
    HistorialServicioFilter,
    TipoMantenimiento,
    EstadoHistorial
)

# Crear router
router = APIRouter(
    prefix="/api/v1/historial-servicios",
    tags=["Historial de Servicios"],
    responses={404: {"description": "No encontrado"}}
)

@router.post("/", response_model=HistorialServicioResponse, status_code=status.HTTP_201_CREATED)
async def crear_historial_servicio(
    historial_data: HistorialServicioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Crear un nuevo registro de historial de servicio
    
    **RF004 - Gestión de Procesos**
    
    - **automovil_id**: ID del automóvil (requerido)
    - **fecha_servicio**: Fecha del servicio realizado
    - **tipo_mantenimiento**: Tipo de mantenimiento (PREVENTIVO, CORRECTIVO, etc.)
    - **descripcion**: Descripción detallada del servicio
    - **kilometraje**: Kilometraje del vehículo al momento del servicio
    - **costo**: Costo del servicio
    - **tecnico_id**: ID del técnico que realizó el servicio (opcional)
    - **proveedor**: Proveedor del servicio (opcional)
    """
    controller = HistorialServicioController(db)
    return controller.crear_historial(historial_data, current_user.id)

@router.get("/{historial_id}", response_model=HistorialServicioResponse)
async def obtener_historial_servicio(
    historial_id: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtener un historial de servicio específico por ID
    
    **RF004 - Gestión de Procesos**
    """
    controller = HistorialServicioController(db)
    return controller.obtener_historial_por_id(historial_id)

@router.get("/", response_model=List[HistorialServicioResponse])
async def listar_historiales_servicio(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    automovil_id: Optional[str] = Query(None, description="Filtrar por ID de automóvil"),
    tipo_mantenimiento: Optional[TipoMantenimiento] = Query(None, description="Filtrar por tipo de mantenimiento"),
    estado: Optional[EstadoHistorial] = Query(None, description="Filtrar por estado"),
    fecha_desde: Optional[datetime] = Query(None, description="Fecha desde (YYYY-MM-DD)"),
    fecha_hasta: Optional[datetime] = Query(None, description="Fecha hasta (YYYY-MM-DD)"),
    tecnico_id: Optional[str] = Query(None, description="Filtrar por ID de técnico"),
    costo_minimo: Optional[float] = Query(None, ge=0, description="Costo mínimo"),
    costo_maximo: Optional[float] = Query(None, ge=0, description="Costo máximo"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Listar todos los historiales de servicio con filtros opcionales
    
    **RF004 - Gestión de Procesos**
    
    Permite filtrar por:
    - Automóvil específico
    - Tipo de mantenimiento
    - Estado del historial
    - Rango de fechas
    - Técnico responsable
    - Rango de costos
    """
    controller = HistorialServicioController(db)
    
    # Crear objeto de filtros
    filtros = HistorialServicioFilter(
        automovil_id=automovil_id,
        tipo_mantenimiento=tipo_mantenimiento,
        estado=estado,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        tecnico_id=tecnico_id,
        costo_minimo=costo_minimo,
        costo_maximo=costo_maximo
    )
    
    return controller.obtener_todos_historiales(skip, limit, filtros)

@router.get("/automovil/{automovil_id}", response_model=List[HistorialServicioResponse])
async def obtener_historial_por_automovil(
    automovil_id: str,
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    tipo_mantenimiento: Optional[TipoMantenimiento] = Query(None, description="Filtrar por tipo de mantenimiento"),
    estado: Optional[EstadoHistorial] = Query(None, description="Filtrar por estado"),
    fecha_desde: Optional[datetime] = Query(None, description="Fecha desde (YYYY-MM-DD)"),
    fecha_hasta: Optional[datetime] = Query(None, description="Fecha hasta (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtener historial completo de servicios de un automóvil específico
    
    **RF04 - Gestión de Procesos**
    
    Retorna todos los servicios realizados a un vehículo ordenados por fecha
    """
    controller = HistorialServicioController(db)
    
    # Crear objeto de filtros
    filtros = HistorialServicioFilter(
        tipo_mantenimiento=tipo_mantenimiento,
        estado=estado,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta
    )
    
    return controller.obtener_historial_por_automovil(automovil_id, skip, limit, filtros)

@router.get("/tecnico/{tecnico_id}", response_model=List[HistorialServicioResponse])
async def obtener_historial_por_tecnico(
    tecnico_id: str,
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtener historiales de servicio realizados por un técnico específico
    
    **RF004 - Gestión de Procesos**
    """
    controller = HistorialServicioController(db)
    return controller.obtener_historial_por_tecnico(tecnico_id, skip, limit)

@router.put("/{historial_id}", response_model=HistorialServicioResponse)
async def actualizar_historial_servicio(
    historial_id: str,
    historial_data: HistorialServicioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Actualizar un registro de historial de servicio existente
    
    **RF004 - Gestión de Procesos**
    
    Permite actualizar cualquier campo del historial de servicio
    """
    controller = HistorialServicioController(db)
    return controller.actualizar_historial(historial_id, historial_data, current_user.id)

@router.delete("/{historial_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_historial_servicio(
    historial_id: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Eliminar (desactivar) un registro de historial de servicio
    
    **RF004 - Gestión de Procesos**
    
    Nota: El registro se marca como inactivo pero no se elimina físicamente
    """
    controller = HistorialServicioController(db)
    controller.eliminar_historial(historial_id, current_user.id)
    return {"message": "Historial de servicio eliminado correctamente"}

@router.get("/mantenimientos/proximos", response_model=List[HistorialServicioResponse])
async def obtener_proximos_mantenimientos(
    dias_adelanto: int = Query(30, ge=1, le=365, description="Días de adelanto para mostrar próximos mantenimientos"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtener vehículos que necesitan mantenimiento próximamente
    
    **RF004 - Gestión de Procesos**
    
    Retorna los vehículos que tienen mantenimientos programados en los próximos N días
    """
    controller = HistorialServicioController(db)
    return controller.obtener_proximos_mantenimientos(dias_adelanto)

@router.get("/estadisticas/mantenimiento")
async def obtener_estadisticas_mantenimiento(
    automovil_id: Optional[str] = Query(None, description="ID de automóvil específico (opcional)"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtener estadísticas de mantenimiento
    
    **RF004 - Gestión de Procesos**
    
    Retorna:
    - Total de servicios realizados
    - Costo total y promedio
    - Distribución por tipo de mantenimiento
    - Distribución por estado
    """
    controller = HistorialServicioController(db)
    return controller.obtener_estadisticas_mantenimiento(automovil_id)

# ===== ENDPOINTS ADICIONALES PARA REPORTES =====

@router.get("/reportes/costos-por-periodo")
async def reporte_costos_por_periodo(
    fecha_desde: datetime = Query(..., description="Fecha inicio del período"),
    fecha_hasta: datetime = Query(..., description="Fecha fin del período"),
    automovil_id: Optional[str] = Query(None, description="ID de automóvil específico"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Generar reporte de costos de mantenimiento por período
    
    **RF004 - Gestión de Procesos**
    """
    controller = HistorialServicioController(db)
    
    filtros = HistorialServicioFilter(
        automovil_id=automovil_id,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta
    )
    
    historiales = controller.obtener_todos_historiales(0, 9999, filtros)
    
    # Calcular estadísticas del período
    total_servicios = len(historiales)
    costo_total = sum(h.costo for h in historiales if h.costo)
    costo_promedio = costo_total / total_servicios if total_servicios > 0 else 0
    
    # Agrupar por tipo de mantenimiento
    costos_por_tipo = {}
    for historial in historiales:
        tipo = historial.tipo_mantenimiento.value
        if tipo not in costos_por_tipo:
            costos_por_tipo[tipo] = {"count": 0, "total": 0}
        costos_por_tipo[tipo]["count"] += 1
        costos_por_tipo[tipo]["total"] += historial.costo if historial.costo else 0
    
    return {
        "periodo": {
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta
        },
        "resumen": {
            "total_servicios": total_servicios,
            "costo_total": costo_total,
            "costo_promedio": costo_promedio
        },
        "costos_por_tipo": costos_por_tipo,
        "historiales": [
            {
                "id": h.id,
                "fecha_servicio": h.fecha_servicio,
                "tipo_mantenimiento": h.tipo_mantenimiento.value,
                "descripcion": h.descripcion,
                "costo": h.costo,
                "automovil_id": h.automovil_id
            } for h in historiales
        ]
    }

@router.get("/reportes/eficiencia-tecnico/{tecnico_id}")
async def reporte_eficiencia_tecnico(
    tecnico_id: str,
    fecha_desde: Optional[datetime] = Query(None, description="Fecha inicio del período"),
    fecha_hasta: Optional[datetime] = Query(None, description="Fecha fin del período"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Generar reporte de eficiencia de un técnico específico
    
    **RF004 - Gestión de Procesos**
    """
    controller = HistorialServicioController(db)
    
    filtros = HistorialServicioFilter(
        tecnico_id=tecnico_id,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta
    )
    
    historiales = controller.obtener_todos_historiales(0, 9999, filtros)
    
    # Calcular métricas de eficiencia
    total_servicios = len(historiales)
    servicios_completados = len([h for h in historiales if h.estado.value == "COMPLETADO"])
    tasa_completacion = (servicios_completados / total_servicios * 100) if total_servicios > 0 else 0
    
    # Servicios por tipo
    servicios_por_tipo = {}
    for historial in historiales:
        tipo = historial.tipo_mantenimiento.value
        servicios_por_tipo[tipo] = servicios_por_tipo.get(tipo, 0) + 1
    
    return {
        "tecnico_id": tecnico_id,
        "periodo": {
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta
        },
        "metricas": {
            "total_servicios": total_servicios,
            "servicios_completados": servicios_completados,
            "tasa_completacion": round(tasa_completacion, 2),
            "servicios_por_tipo": servicios_por_tipo
        },
        "historiales": [
            {
                "id": h.id,
                "fecha_servicio": h.fecha_servicio,
                "tipo_mantenimiento": h.tipo_mantenimiento.value,
                "estado": h.estado.value,
                "descripcion": h.descripcion,
                "automovil_id": h.automovil_id
            } for h in historiales
        ]
    }