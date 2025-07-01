from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, desc, asc, func, extract
from fastapi import HTTPException, status
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from decimal import Decimal

from app.models.reporte import Reporte, TipoReporte, EstadoReporte
from app.models.automovil import Automovil
from app.models.proceso import Proceso
from app.models.user import User
from app.schemas.reporte import (
    ReporteCreate, ReporteUpdate, ReporteResponse, ReporteSimple,
    CambiarEstadoReporte, AprobacionCliente, FirmaReporte,
    EstadisticasReportes, FiltrosReporte, ReportesPaginados,
    TemplateReporte
)

class ReporteController:
    
    @staticmethod
    def crear_reporte(db: Session, reporte_data: ReporteCreate, usuario_id: int) -> ReporteResponse:
        """Crea un nuevo reporte"""
        try:
            # Verificar que el automóvil existe
            automovil = db.query(Automovil).filter(Automovil.id == reporte_data.automovil_id).first()
            if not automovil:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Automóvil no encontrado"
                )
            
            # Verificar que el proceso existe (si se proporciona)
            if reporte_data.proceso_id:
                proceso = db.query(Proceso).filter(Proceso.id == reporte_data.proceso_id).first()
                if not proceso:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Proceso no encontrado"
                    )
            
            # Verificar que el técnico existe (si se proporciona)
            if reporte_data.tecnico_responsable_id:
                tecnico = db.query(User).filter(User.id == reporte_data.tecnico_responsable_id).first()
                if not tecnico:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Técnico no encontrado"
                    )
            
            # Crear el reporte
            db_reporte = Reporte(
                **reporte_data.dict(exclude_unset=True),
                usuario_creador_id=usuario_id
            )
            
            # Calcular costo total
            db_reporte.calcular_costo_total()
            
            db.add(db_reporte)
            db.flush()  # Para obtener el ID
            
            # Generar código de reporte único
            db_reporte.codigo_reporte = db_reporte.generar_codigo_reporte()
            
            db.commit()
            db.refresh(db_reporte)
            
            return ReporteResponse.from_orm(db_reporte)
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear reporte: {str(e)}"
            )
    
    @staticmethod
    def obtener_reportes(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        filtros: Optional[FiltrosReporte] = None,
        usuario_id: Optional[int] = None,
        es_admin: bool = False
    ) -> ReportesPaginados:
        """Obtiene reportes con filtros y paginación"""
        try:
            query = db.query(Reporte).options(
                joinedload(Reporte.automovil),
                joinedload(Reporte.usuario_creador),
                joinedload(Reporte.tecnico_responsable)
            )
            
            # Aplicar filtros de seguridad (no admin solo ve sus reportes)
            if not es_admin and usuario_id:
                query = query.filter(
                    or_(
                        Reporte.usuario_creador_id == usuario_id,
                        Reporte.tecnico_responsable_id == usuario_id
                    )
                )
            
            # Aplicar filtros adicionales
            if filtros:
                if filtros.tipo_reporte:
                    query = query.filter(Reporte.tipo_reporte == filtros.tipo_reporte)
                
                if filtros.estado:
                    query = query.filter(Reporte.estado == filtros.estado)
                
                if filtros.automovil_id:
                    query = query.filter(Reporte.automovil_id == filtros.automovil_id)
                
                if filtros.proceso_id:
                    query = query.filter(Reporte.proceso_id == filtros.proceso_id)
                
                if filtros.tecnico_responsable_id:
                    query = query.filter(Reporte.tecnico_responsable_id == filtros.tecnico_responsable_id)
                
                if filtros.fecha_inicio:
                    query = query.filter(Reporte.created_at >= filtros.fecha_inicio)
                
                if filtros.fecha_fin:
                    query = query.filter(Reporte.created_at <= filtros.fecha_fin)
                
                if filtros.requiere_seguimiento is not None:
                    query = query.filter(Reporte.requiere_seguimiento == filtros.requiere_seguimiento)
                
                if filtros.nivel_satisfaccion_min:
                    query = query.filter(Reporte.nivel_satisfaccion >= filtros.nivel_satisfaccion_min)
                
                if filtros.busqueda_texto:
                    texto = f"%{filtros.busqueda_texto}%"
                    query = query.filter(
                        or_(
                            Reporte.titulo.ilike(texto),
                            Reporte.descripcion_trabajo.ilike(texto),
                            Reporte.codigo_reporte.ilike(texto)
                        )
                    )
            
            # Ordenar por fecha de creación descendente
            query = query.order_by(desc(Reporte.created_at))
            
            # Contar total
            total = query.count()
            
            # Aplicar paginación
            reportes = query.offset(skip).limit(limit).all()
            
            return ReportesPaginados(
                reportes=[ReporteSimple.from_orm(r) for r in reportes],
                total=total,
                pagina=(skip // limit) + 1,
                tamano_pagina=limit,
                total_paginas=(total + limit - 1) // limit
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener reportes: {str(e)}"
            )
    
    @staticmethod
    def obtener_reporte_por_id(db: Session, reporte_id: int, usuario_id: Optional[int] = None, es_admin: bool = False) -> ReporteResponse:
        """Obtiene un reporte por ID"""
        try:
            query = db.query(Reporte).options(
                joinedload(Reporte.automovil),
                joinedload(Reporte.proceso),
                joinedload(Reporte.usuario_creador),
                joinedload(Reporte.tecnico_responsable)
            )
            
            reporte = query.filter(Reporte.id == reporte_id).first()
            
            if not reporte:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Reporte no encontrado"
                )
            
            # Verificar permisos
            if not es_admin and usuario_id:
                if reporte.usuario_creador_id != usuario_id and reporte.tecnico_responsable_id != usuario_id:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="No tiene permisos para ver este reporte"
                    )
            
            return ReporteResponse.from_orm(reporte)
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener reporte: {str(e)}"
            )
    
    @staticmethod
    def actualizar_reporte(db: Session, reporte_id: int, reporte_data: ReporteUpdate, usuario_id: int, es_admin: bool = False) -> ReporteResponse:
        """Actualiza un reporte existente"""
        try:
            reporte = db.query(Reporte).filter(Reporte.id == reporte_id).first()
            
            if not reporte:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Reporte no encontrado"
                )
            
            # Verificar permisos
            if not es_admin:
                if reporte.usuario_creador_id != usuario_id and reporte.tecnico_responsable_id != usuario_id:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="No tiene permisos para editar este reporte"
                    )
            
            # Verificar si puede ser editado
            if not reporte.puede_ser_editado() and not es_admin:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"No se puede editar un reporte en estado {reporte.estado.value}"
                )
            
            # Validar técnico responsable si se proporciona
            if reporte_data.tecnico_responsable_id:
                tecnico = db.query(User).filter(User.id == reporte_data.tecnico_responsable_id).first()
                if not tecnico:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Técnico no encontrado"
                    )
            
            # Actualizar campos
            update_data = reporte_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(reporte, field, value)
            
            # Incrementar versión
            reporte.version += 1
            
            # Recalcular costo total
            reporte.calcular_costo_total()
            
            db.commit()
            db.refresh(reporte)
            
            return ReporteResponse.from_orm(reporte)
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar reporte: {str(e)}"
            )
    
    @staticmethod
    def eliminar_reporte(db: Session, reporte_id: int, usuario_id: int, es_admin: bool = False) -> dict:
        """Elimina un reporte"""
        try:
            reporte = db.query(Reporte).filter(Reporte.id == reporte_id).first()
            
            if not reporte:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Reporte no encontrado"
                )
            
            # Verificar permisos - solo admin o creador pueden eliminar
            if not es_admin and reporte.usuario_creador_id != usuario_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tiene permisos para eliminar este reporte"
                )
            
            # Verificar si puede ser eliminado
            if reporte.estado in [EstadoReporte.APROBADO, EstadoReporte.ARCHIVADO] and not es_admin:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"No se puede eliminar un reporte en estado {reporte.estado.value}"
                )
            
            db.delete(reporte)
            db.commit()
            
            return {"message": "Reporte eliminado exitosamente"}
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al eliminar reporte: {str(e)}"
            )
    
    @staticmethod
    def cambiar_estado_reporte(db: Session, reporte_id: int, cambio_estado: CambiarEstadoReporte, usuario_id: int, es_admin: bool = False) -> ReporteResponse:
        """Cambia el estado de un reporte"""
        try:
            reporte = db.query(Reporte).filter(Reporte.id == reporte_id).first()
            
            if not reporte:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Reporte no encontrado"
                )
            
            # Verificar permisos
            if not es_admin:
                if reporte.usuario_creador_id != usuario_id and reporte.tecnico_responsable_id != usuario_id:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="No tiene permisos para cambiar el estado de este reporte"
                    )
            
            # Verificar transición de estado válida
            if not reporte.puede_cambiar_estado(cambio_estado.nuevo_estado):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"No se puede cambiar de {reporte.estado.value} a {cambio_estado.nuevo_estado.value}"
                )
            
            # Actualizar estado
            reporte.estado = cambio_estado.nuevo_estado
            
            # Agregar comentario si se proporciona
            if cambio_estado.comentario:
                reporte.comentarios_internos = f"{reporte.comentarios_internos}\n\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {cambio_estado.comentario}" if reporte.comentarios_internos else f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {cambio_estado.comentario}"
            
            # Si se está aprobando, registrar fecha
            if cambio_estado.nuevo_estado == EstadoReporte.APROBADO:
                reporte.fecha_aprobacion = datetime.now()
            
            # Si se está completando, registrar fecha
            if cambio_estado.nuevo_estado == EstadoReporte.COMPLETADO:
                reporte.fecha_finalizacion = datetime.now()
            
            db.commit()
            db.refresh(reporte)
            
            return ReporteResponse.from_orm(reporte)
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al cambiar estado del reporte: {str(e)}"
            )
    
    @staticmethod
    def registrar_aprobacion_cliente(db: Session, reporte_id: int, aprobacion: AprobacionCliente, usuario_id: int) -> ReporteResponse:
        """Registra la aprobación del cliente"""
        try:
            reporte = db.query(Reporte).filter(Reporte.id == reporte_id).first()
            
            if not reporte:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Reporte no encontrado"
                )
            
            # Verificar que el usuario sea el propietario del automóvil o admin
            if reporte.automovil.usuario_id != usuario_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Solo el propietario del vehículo puede aprobar el reporte"
                )
            
            # Verificar que el reporte esté en estado que permita aprobación
            if reporte.estado not in [EstadoReporte.PENDIENTE, EstadoReporte.EN_REVISION]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"No se puede aprobar un reporte en estado {reporte.estado.value}"
                )
            
            # Registrar aprobación
            reporte.aprobado_cliente = aprobacion.aprobado
            reporte.fecha_aprobacion_cliente = datetime.now()
            reporte.comentarios_cliente = aprobacion.comentarios
            reporte.nivel_satisfaccion = aprobacion.nivel_satisfaccion
            
            # Si se aprueba, cambiar estado
            if aprobacion.aprobado:
                reporte.estado = EstadoReporte.APROBADO
                reporte.fecha_aprobacion = datetime.now()
            else:
                reporte.estado = EstadoReporte.RECHAZADO
            
            db.commit()
            db.refresh(reporte)
            
            return ReporteResponse.from_orm(reporte)
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al registrar aprobación del cliente: {str(e)}"
            )
    
    @staticmethod
    def firmar_reporte(db: Session, reporte_id: int, firma: FirmaReporte, usuario_id: int) -> ReporteResponse:
        """Registra la firma digital del reporte"""
        try:
            reporte = db.query(Reporte).filter(Reporte.id == reporte_id).first()
            
            if not reporte:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Reporte no encontrado"
                )
            
            # Verificar permisos (técnico responsable o admin)
            if reporte.tecnico_responsable_id != usuario_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Solo el técnico responsable puede firmar el reporte"
                )
            
            # Verificar que el reporte esté completado
            if reporte.estado != EstadoReporte.COMPLETADO:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Solo se pueden firmar reportes completados"
                )
            
            # Registrar firma
            reporte.firma_tecnico = firma.firma_digital
            reporte.fecha_firma = datetime.now()
            
            db.commit()
            db.refresh(reporte)
            
            return ReporteResponse.from_orm(reporte)
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al firmar reporte: {str(e)}"
            )
    
    @staticmethod
    def obtener_estadisticas_reportes(db: Session, fecha_inicio: Optional[datetime] = None, fecha_fin: Optional[datetime] = None) -> EstadisticasReportes:
        """Obtiene estadísticas de reportes"""
        try:
            # Filtro de fechas por defecto (último mes)
            if not fecha_inicio:
                fecha_inicio = datetime.now() - timedelta(days=30)
            if not fecha_fin:
                fecha_fin = datetime.now()
            
            query_base = db.query(Reporte).filter(
                Reporte.created_at >= fecha_inicio,
                Reporte.created_at <= fecha_fin
            )
            
            # Conteos por estado
            total_reportes = query_base.count()
            reportes_pendientes = query_base.filter(Reporte.estado == EstadoReporte.PENDIENTE).count()
            reportes_en_proceso = query_base.filter(Reporte.estado == EstadoReporte.EN_PROCESO).count()
            reportes_completados = query_base.filter(Reporte.estado == EstadoReporte.COMPLETADO).count()
            reportes_aprobados = query_base.filter(Reporte.estado == EstadoReporte.APROBADO).count()
            
            # Conteos por tipo
            reportes_servicio = query_base.filter(Reporte.tipo_reporte == TipoReporte.SERVICIO).count()
            reportes_mantenimiento = query_base.filter(Reporte.tipo_reporte == TipoReporte.MANTENIMIENTO).count()
            reportes_reparacion = query_base.filter(Reporte.tipo_reporte == TipoReporte.REPARACION).count()
            reportes_inspeccion = query_base.filter(Reporte.tipo_reporte == TipoReporte.INSPECCION).count()
            
            # Satisfacción promedio
            satisfaccion_promedio = db.query(func.avg(Reporte.nivel_satisfaccion)).filter(
                Reporte.created_at >= fecha_inicio,
                Reporte.created_at <= fecha_fin,
                Reporte.nivel_satisfaccion.isnot(None)
            ).scalar() or 0
            
            # Costo promedio
            costo_promedio = db.query(func.avg(Reporte.costo_total)).filter(
                Reporte.created_at >= fecha_inicio,
                Reporte.created_at <= fecha_fin,
                Reporte.costo_total.isnot(None)
            ).scalar() or 0
            
            # Tiempo promedio de resolución (en días)
            reportes_con_tiempo = db.query(Reporte).filter(
                Reporte.created_at >= fecha_inicio,
                Reporte.created_at <= fecha_fin,
                Reporte.fecha_finalizacion.isnot(None)
            ).all()
            
            tiempo_promedio_resolucion = 0
            if reportes_con_tiempo:
                tiempos = [(r.fecha_finalizacion - r.created_at).days for r in reportes_con_tiempo]
                tiempo_promedio_resolucion = sum(tiempos) / len(tiempos)
            
            return EstadisticasReportes(
                total_reportes=total_reportes,
                reportes_pendientes=reportes_pendientes,
                reportes_en_proceso=reportes_en_proceso,
                reportes_completados=reportes_completados,
                reportes_aprobados=reportes_aprobados,
                reportes_servicio=reportes_servicio,
                reportes_mantenimiento=reportes_mantenimiento,
                reportes_reparacion=reportes_reparacion,
                reportes_inspeccion=reportes_inspeccion,
                satisfaccion_promedio=round(float(satisfaccion_promedio), 2),
                costo_promedio=round(float(costo_promedio), 2),
                tiempo_promedio_resolucion=round(tiempo_promedio_resolucion, 1),
                periodo_inicio=fecha_inicio,
                periodo_fin=fecha_fin
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener estadísticas: {str(e)}"
            )
    
    @staticmethod
    def obtener_reportes_por_automovil(db: Session, automovil_id: int, usuario_id: Optional[int] = None, es_admin: bool = False) -> List[ReporteSimple]:
        """Obtiene todos los reportes de un automóvil específico"""
        try:
            # Verificar que el automóvil existe
            automovil = db.query(Automovil).filter(Automovil.id == automovil_id).first()
            if not automovil:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Automóvil no encontrado"
                )
            
            # Verificar permisos
            if not es_admin and usuario_id:
                if automovil.usuario_id != usuario_id:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="No tiene permisos para ver los reportes de este automóvil"
                    )
            
            reportes = db.query(Reporte).options(
                joinedload(Reporte.usuario_creador),
                joinedload(Reporte.tecnico_responsable)
            ).filter(
                Reporte.automovil_id == automovil_id
            ).order_by(desc(Reporte.created_at)).all()
            
            return [ReporteSimple.from_orm(r) for r in reportes]
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener reportes del automóvil: {str(e)}"
            )
    
    @staticmethod
    def obtener_template_reporte(db: Session, tipo_reporte: TipoReporte) -> TemplateReporte:
        """Obtiene un template base para crear reportes según el tipo"""
        try:
            templates = {
                TipoReporte.SERVICIO: TemplateReporte(
                    tipo_reporte=TipoReporte.SERVICIO,
                    titulo_sugerido="Servicio de Mantenimiento",
                    descripcion_template="Descripción del servicio realizado:\n\n1. Diagnóstico inicial\n2. Trabajos realizados\n3. Observaciones\n4. Recomendaciones",
                    campos_requeridos=["descripcion_trabajo", "tecnico_responsable_id"],
                    checklist_sugerido=[
                        "Revisión de fluidos",
                        "Inspección visual",
                        "Pruebas funcionales",
                        "Limpieza de componentes"
                    ]
                ),
                TipoReporte.MANTENIMIENTO: TemplateReporte(
                    tipo_reporte=TipoReporte.MANTENIMIENTO,
                    titulo_sugerido="Mantenimiento Preventivo",
                    descripcion_template="Mantenimiento realizado:\n\n1. Componentes revisados\n2. Cambios realizados\n3. Estado general del vehículo\n4. Próximo mantenimiento",
                    campos_requeridos=["descripcion_trabajo", "tecnico_responsable_id", "costo_mano_obra"],
                    checklist_sugerido=[
                        "Cambio de aceite",
                        "Filtros",
                        "Frenos",
                        "Suspensión",
                        "Sistema eléctrico"
                    ]
                ),
                TipoReporte.REPARACION: TemplateReporte(
                    tipo_reporte=TipoReporte.REPARACION,
                    titulo_sugerido="Reparación de Componente",
                    descripcion_template="Reparación realizada:\n\n1. Problema identificado\n2. Diagnóstico\n3. Reparación ejecutada\n4. Pruebas realizadas\n5. Garantía",
                    campos_requeridos=["descripcion_trabajo", "tecnico_responsable_id", "costo_mano_obra", "costo_repuestos"],
                    checklist_sugerido=[
                        "Diagnóstico del problema",
                        "Desmontaje de componentes",
                        "Reparación/Reemplazo",
                        "Montaje y ajuste",
                        "Pruebas de funcionamiento"
                    ]
                ),
                TipoReporte.INSPECCION: TemplateReporte(
                    tipo_reporte=TipoReporte.INSPECCION,
                    titulo_sugerido="Inspección Técnica",
                    descripcion_template="Inspección realizada:\n\n1. Componentes inspeccionados\n2. Estado encontrado\n3. Observaciones\n4. Recomendaciones de acción",
                    campos_requeridos=["descripcion_trabajo", "tecnico_responsable_id"],
                    checklist_sugerido=[
                        "Inspección exterior",
                        "Inspección interior",
                        "Sistema de frenos",
                        "Sistema de dirección",
                        "Motor y transmisión",
                        "Sistema eléctrico"
                    ]
                )
            }
            
            return templates.get(tipo_reporte, templates[TipoReporte.SERVICIO])
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener template: {str(e)}"
            )