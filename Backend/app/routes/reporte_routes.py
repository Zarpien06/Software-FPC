from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from fastapi.security import HTTPBearer
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date
from app.database import get_db
from app.auth.auth_handler import JWTBearer, get_current_user
from app.controllers.reporte_controller import ReporteController
from app.schemas.reporte import (
    ReporteCreate, ReporteUpdate, ReporteResponse, ReporteSimple,
    CambiarEstadoReporte, AprobacionCliente, FirmaReporte,
    EstadisticasReportes, FiltrosReporte, ReportesPaginados,
    TemplateReporte, TipoReporte
)
from app.schemas.user import UserCurrent

router = APIRouter(
    prefix="/api/v1/reportes",
    tags=["Reportes"],
    dependencies=[Depends(HTTPBearer())]
)

# 📝 CREAR REPORTE
@router.post("/", response_model=ReporteResponse, status_code=status.HTTP_201_CREATED)
async def crear_reporte(
    reporte_data: ReporteCreate,
    db: Session = Depends(get_db),
    current_user: UserCurrent = Depends(get_current_user)
):
    """
    Crear un nuevo reporte de servicio.
    
    - **automovil_id**: ID del automóvil al que se asocia el reporte
    - **proceso_id**: ID del proceso/servicio realizado (opcional)
    - **tipo**: Tipo de reporte (INICIAL, FINAL, DIAGNOSTICO, etc.)
    - **titulo**: Título descriptivo del reporte
    - **descripcion**: Descripción detallada del trabajo realizado
    - **observaciones**: Observaciones adicionales del técnico
    - **repuestos_utilizados**: Lista de repuestos utilizados
    - **estado**: Estado del reporte (BORRADOR, EN_REVISION, APROBADO, etc.)
    """
    try:
        controller = ReporteController()
        return await controller.crear_reporte(db, reporte_data, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno: {str(e)}")

# 📋 LISTAR REPORTES CON FILTROS Y PAGINACIÓN
@router.get("/", response_model=ReportesPaginados)
async def listar_reportes(
    page: int = Query(1, ge=1, description="Número de página"),
    limit: int = Query(10, ge=1, le=100, description="Elementos por página"),
    automovil_id: Optional[int] = Query(None, description="Filtrar por automóvil"),
    proceso_id: Optional[int] = Query(None, description="Filtrar por proceso"),
    tipo: Optional[TipoReporte] = Query(None, description="Filtrar por tipo de reporte"),
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    fecha_inicio: Optional[date] = Query(None, description="Fecha inicio (YYYY-MM-DD)"),
    fecha_fin: Optional[date] = Query(None, description="Fecha fin (YYYY-MM-DD)"),
    tecnico_id: Optional[int] = Query(None, description="Filtrar por técnico"),
    cliente_id: Optional[int] = Query(None, description="Filtrar por cliente"),
    search: Optional[str] = Query(None, description="Búsqueda en título y descripción"),
    db: Session = Depends(get_db),
    current_user: UserCurrent = Depends(get_current_user)
):
    """
    Listar reportes con filtros avanzados y paginación.
    
    Filtros disponibles:
    - Por automóvil, proceso, tipo, estado
    - Por rango de fechas
    - Por técnico o cliente
    - Búsqueda de texto en título y descripción
    """
    try:
        controller = ReporteController()
        filtros = FiltrosReporte(
            automovil_id=automovil_id,
            proceso_id=proceso_id,
            tipo=tipo,
            estado=estado,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            tecnico_id=tecnico_id,
            cliente_id=cliente_id,
            search=search
        )
        return await controller.listar_reportes(db, filtros, page, limit, current_user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno: {str(e)}")

# 🔍 OBTENER REPORTE POR ID
@router.get("/{reporte_id}", response_model=ReporteResponse)
async def obtener_reporte(
    reporte_id: int,
    db: Session = Depends(get_db),
    current_user: UserCurrent = Depends(get_current_user)
):
    """
    Obtener detalles completos de un reporte específico.
    """
    try:
        controller = ReporteController()
        return await controller.obtener_reporte(db, reporte_id, current_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno: {str(e)}")

# ✏️ ACTUALIZAR REPORTE
@router.put("/{reporte_id}", response_model=ReporteResponse)
async def actualizar_reporte(
    reporte_id: int,
    reporte_data: ReporteUpdate,
    db: Session = Depends(get_db),
    current_user: UserCurrent = Depends(get_current_user)
):
    """
    Actualizar un reporte existente.
    Solo se pueden actualizar reportes en estado BORRADOR o EN_REVISION.
    """
    try:
        controller = ReporteController()
        return await controller.actualizar_reporte(db, reporte_id, reporte_data, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno: {str(e)}")

# 🗑️ ELIMINAR REPORTE
@router.delete("/{reporte_id}")
async def eliminar_reporte(
    reporte_id: int,
    db: Session = Depends(get_db),
    current_user: UserCurrent = Depends(get_current_user)
):
    """
    Eliminar un reporte.
    Solo administradores pueden eliminar reportes, y solo en estado BORRADOR.
    """
    try:
        controller = ReporteController()
        await controller.eliminar_reporte(db, reporte_id, current_user.id)
        return {"message": "Reporte eliminado exitosamente"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno: {str(e)}")

# 🔄 CAMBIAR ESTADO DEL REPORTE
@router.patch("/{reporte_id}/estado", response_model=ReporteResponse)
async def cambiar_estado_reporte(
    reporte_id: int,
    estado_data: CambiarEstadoReporte,
    db: Session = Depends(get_db),
    current_user: UserCurrent = Depends(get_current_user)
):
    """
    Cambiar el estado de un reporte.
    
    Estados disponibles:
    - BORRADOR: En creación
    - EN_REVISION: Enviado para revisión
    - APROBADO: Aprobado por supervisor
    - RECHAZADO: Rechazado, requiere correcciones
    - FINALIZADO: Proceso completado
    - CLIENTE_APROBADO: Cliente ha visto y aprobado
    """
    try:
        controller = ReporteController()
        return await controller.cambiar_estado_reporte(db, reporte_id, estado_data, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno: {str(e)}")

# ✅ APROBACIÓN DEL CLIENTE
@router.post("/{reporte_id}/aprobacion-cliente", response_model=ReporteResponse)
async def aprobacion_cliente(
    reporte_id: int,
    aprobacion_data: AprobacionCliente,
    db: Session = Depends(get_db),
    current_user: UserCurrent = Depends(get_current_user)
):
    """
    Registrar la aprobación del cliente para un reporte.
    Solo el cliente propietario del vehículo puede aprobar.
    """
    try:
        controller = ReporteController()
        return await controller.aprobacion_cliente(db, reporte_id, aprobacion_data, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno: {str(e)}")

# ✍️ FIRMAR REPORTE
@router.post("/{reporte_id}/firmar")
async def firmar_reporte(
    reporte_id: int,
    firma_data: FirmaReporte,
    db: Session = Depends(get_db),
    current_user: UserCurrent = Depends(get_current_user)
):
    """
    Aplicar firma digital al reporte.
    Puede ser firmado por técnico, supervisor o cliente.
    """
    try:
        controller = ReporteController()
        return await controller.firmar_reporte(db, reporte_id, firma_data, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno: {str(e)}")

# 📊 ESTADÍSTICAS DE REPORTES
@router.get("/estadisticas/resumen", response_model=EstadisticasReportes)
async def obtener_estadisticas_reportes(
    fecha_inicio: Optional[date] = Query(None, description="Fecha inicio para estadísticas"),
    fecha_fin: Optional[date] = Query(None, description="Fecha fin para estadísticas"),
    tecnico_id: Optional[int] = Query(None, description="Estadísticas por técnico"),
    db: Session = Depends(get_db),
    current_user: UserCurrent = Depends(get_current_user)
):
    """
    Obtener estadísticas generales de reportes.
    Incluye conteos por estado, tipo, técnico, etc.
    """
    try:
        controller = ReporteController()
        return await controller.obtener_estadisticas_reportes(db, fecha_inicio, fecha_fin, tecnico_id, current_user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno: {str(e)}")

# 🚗 REPORTES POR AUTOMÓVIL
@router.get("/automovil/{automovil_id}", response_model=List[ReporteSimple])
async def reportes_por_automovil(
    automovil_id: int,
    db: Session = Depends(get_db),
    current_user: UserCurrent = Depends(get_current_user)
):
    """
    Obtener todos los reportes asociados a un automóvil específico.
    Útil para el historial completo del vehículo.
    """
    try:
        controller = ReporteController()
        return await controller.reportes_por_automovil(db, automovil_id, current_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno: {str(e)}")

# 🏷️ PLANTILLAS DE REPORTES
@router.get("/plantillas/tipos", response_model=List[TemplateReporte])
async def obtener_plantillas_reportes(
    tipo: Optional[TipoReporte] = Query(None, description="Filtrar plantillas por tipo"),
    db: Session = Depends(get_db),
    current_user: UserCurrent = Depends(get_current_user)
):
    """
    Obtener plantillas predefinidas para diferentes tipos de reportes.
    Facilita la creación estandarizada de reportes.
    """
    try:
        controller = ReporteController()
        return await controller.obtener_plantillas_reportes(db, tipo, current_user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno: {str(e)}")

# 📎 SUBIR ADJUNTOS AL REPORTE
@router.post("/{reporte_id}/adjuntos")
async def subir_adjunto_reporte(
    reporte_id: int,
    file: UploadFile = File(...),
    descripcion: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: UserCurrent = Depends(get_current_user)
):
    """
    Subir archivos adjuntos a un reporte (imágenes, documentos, etc.).
    Tipos permitidos: jpg, png, pdf, doc, docx.
    """
    try:
        controller = ReporteController()
        return await controller.subir_adjunto_reporte(db, reporte_id, file, descripcion, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno: {str(e)}")

# 📥 EXPORTAR REPORTE
@router.get("/{reporte_id}/exportar")
async def exportar_reporte(
    reporte_id: int,
    formato: str = Query("pdf", regex="^(pdf|excel|word)$", description="Formato de exportación"),
    db: Session = Depends(get_db),
    current_user: UserCurrent = Depends(get_current_user)
):
    """
    Exportar reporte en diferentes formatos (PDF, Excel, Word).
    Genera documento profesional con toda la información del reporte.
    """
    try:
        controller = ReporteController()
        file_path = await controller.exportar_reporte(db, reporte_id, formato, current_user)
        
        # Configurar headers para descarga
        filename = f"reporte_{reporte_id}.{formato}"
        media_type = {
            "pdf": "application/pdf",
            "excel": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "word": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        }.get(formato, "application/octet-stream")
        
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno: {str(e)}")

# 📋 DUPLICAR REPORTE
@router.post("/{reporte_id}/duplicar", response_model=ReporteResponse, status_code=status.HTTP_201_CREATED)
async def duplicar_reporte(
    reporte_id: int,
    automovil_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: UserCurrent = Depends(get_current_user)
):
    """
    Crear una copia de un reporte existente.
    Útil para servicios similares o mantenimientos regulares.
    """
    try:
        controller = ReporteController()
        return await controller.duplicar_reporte(db, reporte_id, automovil_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno: {str(e)}")

# 📈 REPORTES PENDIENTES
@router.get("/pendientes/revision", response_model=List[ReporteSimple])
async def reportes_pendientes_revision(
    db: Session = Depends(get_db),
    current_user: UserCurrent = Depends(get_current_user)
):
    """
    Obtener reportes pendientes de revisión.
    Solo para supervisores y administradores.
    """
    try:
        controller = ReporteController()
        return await controller.reportes_pendientes_revision(db, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno: {str(e)}")

# 🔔 NOTIFICAR CLIENTE
@router.post("/{reporte_id}/notificar-cliente")
async def notificar_cliente_reporte(
    reporte_id: int,
    mensaje_personalizado: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: UserCurrent = Depends(get_current_user)
):
    """
    Enviar notificación al cliente sobre el reporte.
    Incluye enlace para visualizar y aprobar el reporte.
    """
    try:
        controller = ReporteController()
        return await controller.notificar_cliente_reporte(db, reporte_id, mensaje_personalizado, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno: {str(e)}")

# 📝 COMENTARIOS EN REPORTE
@router.post("/{reporte_id}/comentarios")
async def agregar_comentario_reporte(
    reporte_id: int,
    comentario: str,
    db: Session = Depends(get_db),
    current_user: UserCurrent = Depends(get_current_user)
):
    """
    Agregar comentario a un reporte.
    Permite comunicación entre técnicos, supervisores y clientes.
    """
    try:
        controller = ReporteController()
        return await controller.agregar_comentario_reporte(db, reporte_id, comentario, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno: {str(e)}")

# 🏷️ ETIQUETAS DE REPORTE
@router.post("/{reporte_id}/etiquetas")
async def gestionar_etiquetas_reporte(
    reporte_id: int,
    etiquetas: List[str],
    accion: str = Query("agregar", regex="^(agregar|quitar|reemplazar)$"),
    db: Session = Depends(get_db),
    current_user: UserCurrent = Depends(get_current_user)
):
    """
    Gestionar etiquetas de un reporte para mejor categorización.
    Acciones: agregar, quitar, reemplazar etiquetas.
    """
    try:
        controller = ReporteController()
        return await controller.gestionar_etiquetas_reporte(db, reporte_id, etiquetas, accion, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno: {str(e)}")