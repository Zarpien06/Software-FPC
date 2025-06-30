# 📁 app/controllers/proceso_controller.py
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc
from fastapi import HTTPException, status
from typing import Optional, List
from datetime import datetime, timedelta
import logging

from app.models.proceso import Proceso
from app.models.automovil import Automovil
from app.models.user import Usuario
from app.schemas.proceso import (
    ProcesoCreate, 
    ProcesoUpdate, 
    ProcesoIniciar, 
    ProcesoCompletar, 
    ProcesoInspeccion,
    ProcesoResponse,
    ProcesoResumen
)

logger = logging.getLogger(__name__)

class ProcesoController:
    
    @staticmethod
    def crear_proceso(db: Session, proceso_data: ProcesoCreate, usuario_id: int) -> Proceso:
        """Crear un nuevo proceso"""
        try:
            # Verificar que el automóvil existe
            automovil = db.query(Automovil).filter(
                and_(Automovil.id == proceso_data.automovil_id, Automovil.activo == True)
            ).first()
            
            if not automovil:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Automóvil con ID {proceso_data.automovil_id} no encontrado"
                )
            
            # Verificar técnico responsable si se proporciona
            if proceso_data.tecnico_responsable_id:
                tecnico = db.query(Usuario).filter(
                    and_(
                        Usuario.id == proceso_data.tecnico_responsable_id,
                        Usuario.activo == True,
                        or_(Usuario.rol.has(nombre="EMPLEADO"), Usuario.rol.has(nombre="ADMINISTRADOR"))
                    )
                ).first()
                
                if not tecnico:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Técnico con ID {proceso_data.tecnico_responsable_id} no encontrado"
                    )
            
            # Generar código único del proceso
            codigo_proceso = ProcesoController._generar_codigo_proceso(db)
            
            # Crear proceso
            nuevo_proceso = Proceso(
                codigo_proceso=codigo_proceso,
                **proceso_data.dict(),
                creado_por_id=usuario_id
            )
            
            db.add(nuevo_proceso)
            db.commit()
            db.refresh(nuevo_proceso)
            
            logger.info(f"✅ Proceso creado: {codigo_proceso} para automóvil ID {proceso_data.automovil_id}")
            return nuevo_proceso
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Error creando proceso: {str(e)}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno creando proceso: {str(e)}"
            )
    
    @staticmethod
    def obtener_proceso_por_id(db: Session, proceso_id: int) -> Optional[Proceso]:
        """Obtener proceso por ID"""
        return db.query(Proceso).filter(
            and_(Proceso.id == proceso_id, Proceso.activo == True)
        ).first()
    
    @staticmethod
    def obtener_proceso_por_codigo(db: Session, codigo_proceso: str) -> Optional[Proceso]:
        """Obtener proceso por código"""
        return db.query(Proceso).filter(
            and_(Proceso.codigo_proceso == codigo_proceso, Proceso.activo == True)
        ).first()
    
    @staticmethod
    def listar_procesos(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        automovil_id: Optional[int] = None,
        estado: Optional[str] = None,
        tipo_proceso: Optional[str] = None,
        prioridad: Optional[str] = None,
        tecnico_id: Optional[int] = None,
        fecha_inicio: Optional[datetime] = None,
        fecha_fin: Optional[datetime] = None
    ) -> List[Proceso]:
        """Listar procesos con filtros opcionales"""
        try:
            query = db.query(Proceso).filter(Proceso.activo == True)
            
            # Aplicar filtros
            if automovil_id:
                query = query.filter(Proceso.automovil_id == automovil_id)
            
            if estado:
                query = query.filter(Proceso.estado == estado)
            
            if tipo_proceso:
                query = query.filter(Proceso.tipo_proceso == tipo_proceso)
            
            if prioridad:
                query = query.filter(Proceso.prioridad == prioridad)
            
            if tecnico_id:
                query = query.filter(Proceso.tecnico_responsable_id == tecnico_id)
            
            if fecha_inicio:
                query = query.filter(Proceso.fecha_inicio_programada >= fecha_inicio)
            
            if fecha_fin:
                query = query.filter(Proceso.fecha_inicio_programada <= fecha_fin)
            
            # Ordenar por fecha de creación descendente
            query = query.order_by(desc(Proceso.creado_en))
            
            return query.offset(skip).limit(limit).all()
            
        except Exception as e:
            logger.error(f"❌ Error listando procesos: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno listando procesos: {str(e)}"
            )
    
    @staticmethod
    def actualizar_proceso(db: Session, proceso_id: int, proceso_data: ProcesoUpdate) -> Optional[Proceso]:
        """Actualizar proceso existente"""
        try:
            proceso = ProcesoController.obtener_proceso_por_id(db, proceso_id)
            
            if not proceso:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Proceso con ID {proceso_id} no encontrado"
                )
            
            # Verificar que no se pueda modificar un proceso completado
            if proceso.estado == "COMPLETADO" and proceso_data.estado != "COMPLETADO":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se puede modificar un proceso completado"
                )
            
            # Actualizar campos proporcionados
            update_data = proceso_data.dict(exclude_unset=True)
            
            for field, value in update_data.items():
                setattr(proceso, field, value)
            
            # Actualizar timestamp de modificación
            proceso.actualizado_en = datetime.utcnow()
            
            db.commit()
            db.refresh(proceso)
            
            logger.info(f"✅ Proceso actualizado: {proceso.codigo_proceso}")
            return proceso
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Error actualizando proceso {proceso_id}: {str(e)}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno actualizando proceso: {str(e)}"
            )
    
    @staticmethod
    def iniciar_proceso(db: Session, proceso_id: int, datos_inicio: ProcesoIniciar) -> Proceso:
        """Iniciar un proceso pendiente"""
        try:
            proceso = ProcesoController.obtener_proceso_por_id(db, proceso_id)
            
            if not proceso:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Proceso con ID {proceso_id} no encontrado"
                )
            
            if proceso.estado != "PENDIENTE":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El proceso debe estar en estado PENDIENTE para iniciarse. Estado actual: {proceso.estado}"
                )
            
            # Actualizar estado y datos de inicio
            proceso.estado = "EN_PROGRESO"
            proceso.fecha_inicio_real = datetime.utcnow()
            
            if datos_inicio.observaciones_iniciales:
                proceso.observaciones_iniciales = datos_inicio.observaciones_iniciales
            
            if datos_inicio.kilometraje_actual:
                proceso.kilometraje_actual = datos_inicio.kilometraje_actual
            
            proceso.actualizado_en = datetime.utcnow()
            
            db.commit()
            db.refresh(proceso)
            
            logger.info(f"✅ Proceso iniciado: {proceso.codigo_proceso}")
            return proceso
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Error iniciando proceso {proceso_id}: {str(e)}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno iniciando proceso: {str(e)}"
            )
    
    @staticmethod
    def completar_proceso(db: Session, proceso_id: int, datos_completion: ProcesoCompletar) -> Proceso:
        """Completar un proceso en progreso"""
        try:
            proceso = ProcesoController.obtener_proceso_por_id(db, proceso_id)
            
            if not proceso:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Proceso con ID {proceso_id} no encontrado"
                )
            
            if proceso.estado != "EN_PROGRESO":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El proceso debe estar EN_PROGRESO para completarse. Estado actual: {proceso.estado}"
                )
            
            # Actualizar estado y datos de finalización
            proceso.estado = "COMPLETADO"
            proceso.fecha_fin_real = datetime.utcnow()
            
            # Calcular duración real
            if proceso.fecha_inicio_real:
                duracion = proceso.fecha_fin_real - proceso.fecha_inicio_real
                proceso.duracion_real_horas = duracion.total_seconds() / 3600
            
            # Actualizar campos de finalización
            proceso.observaciones_finales = datos_completion.observaciones_finales
            proceso.trabajo_realizado = datos_completion.trabajo_realizado
            
            if datos_completion.costo_real:
                proceso.costo_real = datos_completion.costo_real
            if datos_completion.costo_mano_obra:
                proceso.costo_mano_obra = datos_completion.costo_mano_obra
            if datos_completion.costo_repuestos:
                proceso.costo_repuestos = datos_completion.costo_repuestos
            if datos_completion.repuestos_utilizados:
                proceso.repuestos_utilizados = datos_completion.repuestos_utilizados
            if datos_completion.duracion_real_horas:
                proceso.duracion_real_horas = datos_completion.duracion_real_horas
            
            # Calcular fecha de vencimiento de garantía
            if proceso.garantia_dias and proceso.garantia_dias > 0:
                proceso.fecha_vencimiento_garantia = proceso.fecha_fin_real + timedelta(days=proceso.garantia_dias)
            
            proceso.actualizado_en = datetime.utcnow()
            
            db.commit()
            db.refresh(proceso)
            
            logger.info(f"✅ Proceso completado: {proceso.codigo_proceso}")
            return proceso
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Error completando proceso {proceso_id}: {str(e)}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno completando proceso: {str(e)}"
            )
    
    @staticmethod
    def cancelar_proceso(db: Session, proceso_id: int, motivo: str) -> Proceso:
        """Cancelar un proceso"""
        try:
            proceso = ProcesoController.obtener_proceso_por_id(db, proceso_id)
            
            if not proceso:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Proceso con ID {proceso_id} no encontrado"
                )
            
            if proceso.estado in ["COMPLETADO", "CANCELADO"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"No se puede cancelar un proceso en estado {proceso.estado}"
                )
            
            proceso.estado = "CANCELADO"
            proceso.observaciones_finales = f"PROCESO CANCELADO - Motivo: {motivo}"
            proceso.actualizado_en = datetime.utcnow()
            
            db.commit()
            db.refresh(proceso)
            
            logger.info(f"✅ Proceso cancelado: {proceso.codigo_proceso}")
            return proceso
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Error cancelando proceso {proceso_id}: {str(e)}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno cancelando proceso: {str(e)}"
            )
    
    @staticmethod
    def realizar_inspeccion(db: Session, proceso_id: int, inspeccion_data: ProcesoInspeccion) -> Proceso:
        """Realizar inspección de calidad del proceso"""
        try:
            proceso = ProcesoController.obtener_proceso_por_id(db, proceso_id)
            
            if not proceso:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Proceso con ID {proceso_id} no encontrado"
                )
            
            if proceso.estado != "COMPLETADO":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Solo se puede inspeccionar procesos completados"
                )
            
            # Verificar inspector
            inspector = db.query(Usuario).filter(
                and_(
                    Usuario.id == inspeccion_data.inspector_id,
                    Usuario.activo == True
                )
            ).first()
            
            if not inspector:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Inspector con ID {inspeccion_data.inspector_id} no encontrado"
                )
            
            # Actualizar datos de inspección
            proceso.inspeccion_realizada = True
            proceso.fecha_inspeccion = datetime.utcnow()
            proceso.resultado_inspeccion = inspeccion_data.resultado_inspeccion
            proceso.inspector_id = inspeccion_data.inspector_id
            proceso.actualizado_en = datetime.utcnow()
            
            db.commit()
            db.refresh(proceso)
            
            logger.info(f"✅ Inspección realizada para proceso: {proceso.codigo_proceso}")
            return proceso
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Error realizando inspección del proceso {proceso_id}: {str(e)}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno realizando inspección: {str(e)}"
            )
    
    @staticmethod
    def eliminar_proceso(db: Session, proceso_id: int) -> bool:
        """Eliminar proceso (soft delete)"""
        try:
            proceso = ProcesoController.obtener_proceso_por_id(db, proceso_id)
            
            if not proceso:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Proceso con ID {proceso_id} no encontrado"
                )
            
            # Solo se pueden eliminar procesos pendientes o cancelados
            if proceso.estado in ["EN_PROGRESO", "COMPLETADO"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"No se puede eliminar un proceso en estado {proceso.estado}"
                )
            
            proceso.activo = False
            proceso.actualizado_en = datetime.utcnow()
            
            db.commit()
            
            logger.info(f"✅ Proceso eliminado: {proceso.codigo_proceso}")
            return True
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ Error eliminando proceso {proceso_id}: {str(e)}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno eliminando proceso: {str(e)}"
            )
    
    @staticmethod
    def _generar_codigo_proceso(db: Session) -> str:
        """Generar código único para el proceso"""
        from datetime import datetime
        
        # Formato: PRO-YYYYMMDD-NNNN
        fecha_actual = datetime.now()
        fecha_str = fecha_actual.strftime("%Y%m%d")
        
        # Buscar el último proceso del día
        ultimo_proceso = db.query(Proceso).filter(
            Proceso.codigo_proceso.like(f"PRO-{fecha_str}-%")
        ).order_by(desc(Proceso.codigo_proceso)).first()
        
        if ultimo_proceso:
            # Extraer número secuencial del último código
            ultimo_numero = int(ultimo_proceso.codigo_proceso.split("-")[-1])
            siguiente_numero = ultimo_numero + 1
        else:
            siguiente_numero = 1
        
        return f"PRO-{fecha_str}-{siguiente_numero:04d}"
    
    @staticmethod
    def obtener_estadisticas_procesos(db: Session, automovil_id: Optional[int] = None) -> dict:
        """Obtener estadísticas de procesos"""
        try:
            query = db.query(Proceso).filter(Proceso.activo == True)
            
            if automovil_id:
                query = query.filter(Proceso.automovil_id == automovil_id)
            
            procesos = query.all()
            
            total_procesos = len(procesos)
            
            # Estadísticas por estado
            estados = {}
            tipos = {}
            prioridades = {}
            
            costo_total = 0
            duracion_total = 0
            procesos_con_duracion = 0
            
            for proceso in procesos:
                # Contar por estado
                estados[proceso.estado] = estados.get(proceso.estado, 0) + 1
                
                # Contar por tipo
                tipos[proceso.tipo_proceso] = tipos.get(proceso.tipo_proceso, 0) + 1
                
                # Contar por prioridad
                prioridades[proceso.prioridad] = prioridades.get(proceso.prioridad, 0) + 1
                
                # Sumar costos reales
                if proceso.costo_real:
                    costo_total += float(proceso.costo_real)
                
                # Sumar duraciones
                if proceso.duracion_real_horas:
                    duracion_total += float(proceso.duracion_real_horas)
                    procesos_con_duracion += 1
            
            return {
                "total_procesos": total_procesos,
                "procesos_por_estado": estados,
                "procesos_por_tipo": tipos,
                "procesos_por_prioridad": prioridades,
                "costo_total": costo_total,
                "duracion_promedio_horas": duracion_total / procesos_con_duracion if procesos_con_duracion > 0 else 0,
                "procesos_en_garantia": len([p for p in procesos if p.fecha_vencimiento_garantia and p.fecha_vencimiento_garantia > datetime.utcnow()])
            }
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo estadísticas de procesos: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno obteniendo estadísticas: {str(e)}"
            )