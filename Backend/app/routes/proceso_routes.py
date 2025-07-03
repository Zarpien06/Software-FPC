# 📁 app/routes/proceso_routes.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.auth.auth_handler import get_current_user
from app.models.user import User
from app.controllers.proceso_controller import ProcesoController
from app.schemas.proceso import (
    ProcesoCreate,
    ProcesoUpdate,
    ProcesoResponse,
    ProcesoFilter,
    EstadoProcesoEnum,
    TipoProcesoEnum,
    PrioridadEnum
)

# Crear router
router = APIRouter(
    prefix="/api/v1/procesos",
    tags=["Procesos "],
    responses={404: {"description": "No encontrado"}}
)

@router.post("/", response_model=ProcesoResponse, status_code=status.HTTP_201_CREATED)
async def crear_proceso(
    proceso_data: ProcesoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Crear un nuevo proceso de mantenimiento o reparación
    
    **RF004 - Gestión de Procesos**
    
    - **automovil_id**: ID del automóvil (requerido)
    - **titulo**: Título descriptivo del proceso
    - **descripcion**: Descripción detallada del proceso
    - **tipo_proceso**: Tipo de proceso (MANTENIMIENTO, REPARACION, etc.)
    - **estado**: Estado del proceso (PENDIENTE, EN_PROCESO, etc.)
    - **prioridad**: Prioridad del proceso (BAJA, MEDIA, ALTA, URGENTE)
    - **fecha_programada**: Fecha programada para realizar el proceso
    - **tecnico_asignado_id**: ID del técnico asignado (opcional)
    """
    controller = ProcesoController(db)
    return controller.crear_proceso(proceso_data, current_user.id)

@router.get("/{proceso_id}", response_model=ProcesoResponse)
async def obtener_proceso(
    proceso_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener un proceso específico por ID
    
    **RF004 - Gestión de Procesos**
    """
    controller = ProcesoController(db)
    return controller.obtener_proceso_por_id(proceso_id)

@router.get("/", response_model=List[ProcesoResponse])
async def listar_procesos(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    automovil_id: Optional[str] = Query(None, description="Filtrar por ID de automóvil"),
    estado: Optional[EstadoProcesoEnum] = Query(None, description="Filtrar por estado del proceso"),
    tipo_proceso: Optional[TipoProcesoEnum] = Query(None, description="Filtrar por tipo de proceso"),
    prioridad: Optional[PrioridadEnum] = Query(None, description="Filtrar por prioridad"),
    tecnico_asignado_id: Optional[str] = Query(None, description="Filtrar por técnico asignado"),
    fecha_desde: Optional[datetime] = Query(None, description="Fecha programada desde (YYYY-MM-DD)"),
    fecha_hasta: Optional[datetime] = Query(None, description="Fecha programada hasta (YYYY-MM-DD)"),
    solo_pendientes: bool = Query(False, description="Mostrar solo procesos pendientes"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Listar todos los procesos con filtros opcionales
    
    **RF004 - Gestión de Procesos**
    
    Permite filtrar por:
    - Automóvil específico
    - Estado del proceso
    - Tipo de proceso
    - Prioridad
    - Técnico asignado
    - Rango de fechas programadas
    - Solo procesos pendientes
    """
    controller = ProcesoController(db)
    
    # Crear objeto de filtros
    filtros = ProcesoFilter(
        automovil_id=automovil_id,
        estado=estado,
        tipo_proceso=tipo_proceso,
        prioridad=prioridad,
        tecnico_asignado_id=tecnico_asignado_id,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        solo_pendientes=solo_pendientes
    )
    
    return controller.obtener_todos_procesos(skip, limit, filtros)

@router.get("/automovil/{automovil_id}", response_model=List[ProcesoResponse])
async def obtener_procesos_por_automovil(
    automovil_id: str,
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    estado: Optional[EstadoProcesoEnum] = Query(None, description="Filtrar por estado"),
    tipo_proceso: Optional[TipoProcesoEnum] = Query(None, description="Filtrar por tipo"),
    solo_pendientes: bool = Query(False, description="Mostrar solo procesos pendientes"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener todos los procesos de un automóvil específico
    
    **RF004 - Gestión de Procesos**
    
    Retorna todos los procesos asociados a un vehículo ordenados por fecha de creación
    """
    controller = ProcesoController(db)
    
    # Crear objeto de filtros
    filtros = ProcesoFilter(
        estado=estado,
        tipo_proceso=tipo_proceso,
        solo_pendientes=solo_pendientes
    )
    
    return controller.obtener_procesos_por_automovil(automovil_id, skip, limit, filtros)

@router.get("/tecnico/{tecnico_id}", response_model=List[ProcesoResponse])
async def obtener_procesos_por_tecnico(
    tecnico_id: str,
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    estado: Optional[EstadoProcesoEnum] = Query(None, description="Filtrar por estado"),
    solo_pendientes: bool = Query(False, description="Mostrar solo procesos pendientes"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener procesos asignados a un técnico específico
    
    **RF004 - Gestión de Procesos**
    """
    controller = ProcesoController(db)
    
    filtros = ProcesoFilter(
        estado=estado,
        solo_pendientes=solo_pendientes
    )
    
    return controller.obtener_procesos_por_tecnico(tecnico_id, skip, limit, filtros)

@router.put("/{proceso_id}", response_model=ProcesoResponse)
async def actualizar_proceso(
    proceso_id: str,
    proceso_data: ProcesoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Actualizar un proceso existente
    
    **RF004 - Gestión de Procesos**
    
    Permite actualizar cualquier campo del proceso
    """
    controller = ProcesoController(db)
    return controller.actualizar_proceso(proceso_id, proceso_data, current_user.id)

@router.delete("/{proceso_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_proceso(
    proceso_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Eliminar (desactivar) un proceso
    
    **RF004 - Gestión de Procesos**
    
    Nota: El proceso se marca como inactivo pero no se elimina físicamente
    """
    controller = ProcesoController(db)
    controller.eliminar_proceso(proceso_id, current_user.id)
    return {"message": "Proceso eliminado correctamente"}

@router.patch("/{proceso_id}/estado", response_model=ProcesoResponse)
async def cambiar_estado_proceso(
    proceso_id: str,
    nuevo_estado: EstadoProcesoEnum,
    observaciones: Optional[str] = Query(None, description="Observaciones del cambio de estado"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cambiar el estado de un proceso específico
    
    **RF004 - Gestión de Procesos**
    
    Estados disponibles:
    - PENDIENTE: Proceso creado pero no iniciado
    - EN_PROCESO: Proceso en ejecución
    - COMPLETADO: Proceso terminado exitosamente
    - CANCELADO: Proceso cancelado
    - PAUSADO: Proceso temporalmente pausado
    """
    controller = ProcesoController(db)
    return controller.cambiar_estado_proceso(proceso_id, nuevo_estado, current_user.id, observaciones)

@router.patch("/{proceso_id}/asignar-tecnico", response_model=ProcesoResponse)
async def asignar_tecnico_proceso(
    proceso_id: str,
    tecnico_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Asignar un técnico a un proceso específico
    
    **RF004 - Gestión de Procesos**
    """
    controller = ProcesoController(db)
    return controller.asignar_tecnico(proceso_id, tecnico_id, current_user.id)

@router.patch("/{proceso_id}/cambiar-prioridad", response_model=ProcesoResponse)
async def cambiar_prioridad_proceso(
    proceso_id: str,
    nueva_prioridad: PrioridadEnum,
    justificacion: Optional[str] = Query(None, description="Justificación del cambio de prioridad"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cambiar la prioridad de un proceso
    
    **RF004 - Gestión de Procesos**
    
    Prioridades disponibles:
    - BAJA: Proceso de baja prioridad
    - MEDIA: Prioridad normal
    - ALTA: Alta prioridad
    - URGENTE: Máxima prioridad
    """
    controller = ProcesoController(db)
    return controller.cambiar_prioridad(proceso_id, nueva_prioridad, current_user.id, justificacion)

@router.get("/pendientes/resumen")
async def obtener_resumen_pendientes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener resumen de procesos pendientes
    
    **RF004 - Gestión de Procesos**
    
    Retorna estadísticas de procesos pendientes agrupados por:
    - Prioridad
    - Tipo de proceso
    - Técnico asignado
    """
    controller = ProcesoController(db)
    return controller.obtener_resumen_pendientes()

@router.get("/estadisticas/dashboard")
async def obtener_estadisticas_dashboard(
    automovil_id: Optional[str] = Query(None, description="ID de automóvil específico"),
    tecnico_id: Optional[str] = Query(None, description="ID de técnico específico"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener estadísticas para dashboard de procesos
    
    **RF004 - Gestión de Procesos**
    
    Retorna:
    - Total de procesos por estado
    - Procesos por tipo
    - Procesos por prioridad
    - Procesos programados para hoy
    - Procesos vencidos
    """
    controller = ProcesoController(db)
    return controller.obtener_estadisticas_dashboard(automovil_id, tecnico_id)

@router.get("/programados/hoy", response_model=List[ProcesoResponse])
async def obtener_procesos_programados_hoy(
    tecnico_id: Optional[str] = Query(None, description="Filtrar por técnico específico"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener procesos programados para hoy
    
    **RF004 - Gestión de Procesos**
    """
    controller = ProcesoController(db)
    return controller.obtener_procesos_programados_hoy(tecnico_id)

@router.get("/vencidos/lista", response_model=List[ProcesoResponse])
async def obtener_procesos_vencidos(
    dias_vencimiento: int = Query(0, ge=0, description="Días de vencimiento (0 = solo hoy)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener procesos vencidos (fecha programada pasada)
    
    **RF004 - Gestión de Procesos**
    """
    controller = ProcesoController(db)
    return controller.obtener_procesos_vencidos(dias_vencimiento)

@router.get("/reportes/productividad-tecnico/{tecnico_id}")
async def reporte_productividad_tecnico(
    tecnico_id: str,
    fecha_desde: Optional[datetime] = Query(None, description="Fecha inicio del período"),
    fecha_hasta: Optional[datetime] = Query(None, description="Fecha fin del período"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generar reporte de productividad de un técnico específico
    
    **RF004 - Gestión de Procesos**
    """
    controller = ProcesoController(db)
    
    filtros = ProcesoFilter(
        tecnico_asignado_id=tecnico_id,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta
    )
    
    procesos = controller.obtener_todos_procesos(0, 9999, filtros)
    
    # Calcular métricas de productividad
    total_procesos = len(procesos)
    completados = len([p for p in procesos if p.estado.value == "COMPLETADO"])
    en_proceso = len([p for p in procesos if p.estado.value == "EN_PROCESO"])
    pendientes = len([p for p in procesos if p.estado.value == "PENDIENTE"])
    
    tasa_completacion = (completados / total_procesos * 100) if total_procesos > 0 else 0
    
    # Procesos por tipo
    procesos_por_tipo = {}
    for proceso in procesos:
        tipo = proceso.tipo_proceso.value
        procesos_por_tipo[tipo] = procesos_por_tipo.get(tipo, 0) + 1
    
    # Procesos por prioridad
    procesos_por_prioridad = {}
    for proceso in procesos:
        prioridad = proceso.prioridad.value
        procesos_por_prioridad[prioridad] = procesos_por_prioridad.get(prioridad, 0) + 1
    
    return {
        "tecnico_id": tecnico_id,
        "periodo": {
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta
        },
        "metricas": {
            "total_procesos": total_procesos,
            "completados": completados,
            "en_proceso": en_proceso,
            "pendientes": pendientes,
            "tasa_completacion": round(tasa_completacion, 2)
        },
        "distribucion": {
            "por_tipo": procesos_por_tipo,
            "por_prioridad": procesos_por_prioridad
        },
        "procesos": [
            {
                "id": p.id,
                "titulo": p.titulo,
                "tipo_proceso": p.tipo_proceso.value,
                "estado": p.estado.value,
                "prioridad": p.prioridad.value,
                "fecha_programada": p.fecha_programada,
                "fecha_completado": p.fecha_completado,
                "automovil_id": p.automovil_id
            } for p in procesos
        ]
    }

@router.get("/reportes/eficiencia-general")
async def reporte_eficiencia_general(
    fecha_desde: Optional[datetime] = Query(None, description="Fecha inicio del período"),
    fecha_hasta: Optional[datetime] = Query(None, description="Fecha fin del período"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generar reporte de eficiencia general del taller
    
    **RF004 - Gestión de Procesos**
    """
    controller = ProcesoController(db)
    
    filtros = ProcesoFilter(
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta
    )
    
    procesos = controller.obtener_todos_procesos(0, 9999, filtros)
    
    # Métricas generales
    total_procesos = len(procesos)
    completados = len([p for p in procesos if p.estado.value == "COMPLETADO"])
    
    # Tiempo promedio de completación (solo para procesos completados)
    tiempos_completacion = []
    for proceso in procesos:
        if proceso.estado.value == "COMPLETADO" and proceso.fecha_completado and proceso.fecha_programada:
            tiempo = (proceso.fecha_completado - proceso.fecha_programada).days
            tiempos_completacion.append(tiempo)
    
    tiempo_promedio_completacion = sum(tiempos_completacion) / len(tiempos_completacion) if tiempos_completacion else 0
    
    # Distribuciones
    estados_distribucion = {}
    tipos_distribucion = {}
    prioridades_distribucion = {}
    
    for proceso in procesos:
        # Por estado
        estado = proceso.estado.value
        estados_distribucion[estado] = estados_distribucion.get(estado, 0) + 1
        
        # Por tipo
        tipo = proceso.tipo_proceso.value
        tipos_distribucion[tipo] = tipos_distribucion.get(tipo, 0) + 1
        
        # Por prioridad
        prioridad = proceso.prioridad.value
        prioridades_distribucion[prioridad] = prioridades_distribucion.get(prioridad, 0) + 1
    
    return {
        "periodo": {
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta
        },
        "metricas_generales": {
            "total_procesos": total_procesos,
            "procesos_completados": completados,
            "tasa_completacion": round((completados / total_procesos * 100) if total_procesos > 0 else 0, 2),
            "tiempo_promedio_completacion_dias": round(tiempo_promedio_completacion, 2)
        },
        "distribucion": {
            "por_estado": estados_distribucion,
            "por_tipo": tipos_distribucion,
            "por_prioridad": prioridades_distribucion
        }
    }