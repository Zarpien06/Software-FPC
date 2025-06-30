from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, func, and_
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import datetime, timedelta
from decimal import Decimal
import uuid

from app.models.cotizacion import Cotizacion, ItemCotizacion, EstadoCotizacion
from app.schemas.cotizacion import CotizacionCreate, CotizacionUpdate
from app.models.user import User
from app.models.automovil import Automovil

class CotizacionController:
    
    @staticmethod
    def generar_numero_cotizacion() -> str:
        """Genera un número único de cotización"""
        fecha = datetime.now()
        codigo = f"COT-{fecha.year}{fecha.month:02d}{fecha.day:02d}-{uuid.uuid4().hex[:6].upper()}"
        return codigo
    
    @staticmethod
    def calcular_totales(items: List[ItemCotizacion]) -> tuple:
        """Calcula subtotal, impuestos y total de una cotización"""
        subtotal = sum(item.precio_total for item in items)
        impuestos = subtotal * Decimal('0.19')  # IVA 19%
        total = subtotal + impuestos
        return subtotal, impuestos, total
    
    @staticmethod
    def crear_cotizacion(db: Session, cotizacion_data: CotizacionCreate, empleado_id: int) -> Cotizacion:
        """Crea una nueva cotización"""
        
        # Validar que el cliente existe
        cliente = db.query(User).filter(User.id == cotizacion_data.cliente_id).first()
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado"
            )
        
        # Validar que el automóvil existe
        automovil = db.query(Automovil).filter(Automovil.id == cotizacion_data.automovil_id).first()
        if not automovil:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Automóvil no encontrado"
            )
        
        # Crear cotización
        db_cotizacion = Cotizacion(
            numero_cotizacion=CotizacionController.generar_numero_cotizacion(),
            cliente_id=cotizacion_data.cliente_id,
            automovil_id=cotizacion_data.automovil_id,
            empleado_id=empleado_id,
            descripcion_general=cotizacion_data.descripcion_general,
            observaciones=cotizacion_data.observaciones,
            tiempo_estimado_horas=cotizacion_data.tiempo_estimado_horas,
            kilometraje_actual=cotizacion_data.kilometraje_actual,
            fecha_vencimiento=cotizacion_data.fecha_vencimiento
        )
        
        db.add(db_cotizacion)
        db.flush()  # Para obtener el ID
        
        # Crear items
        items_db = []
        for item_data in cotizacion_data.items:
            precio_total = item_data.precio_unitario * item_data.cantidad
            item_db = ItemCotizacion(
                cotizacion_id=db_cotizacion.id,
                tipo_servicio=item_data.tipo_servicio,
                descripcion=item_data.descripcion,
                detalle=item_data.detalle,
                cantidad=item_data.cantidad,
                precio_unitario=item_data.precio_unitario,
                precio_total=precio_total,
                tiempo_estimado_horas=item_data.tiempo_estimado_horas
            )
            items_db.append(item_db)
            db.add(item_db)
        
        # Calcular totales
        subtotal, impuestos, total = CotizacionController.calcular_totales(items_db)
        db_cotizacion.subtotal = subtotal
        db_cotizacion.impuestos = impuestos
        db_cotizacion.total = total
        
        db.commit()
        db.refresh(db_cotizacion)
        return db_cotizacion
    
    @staticmethod
    def obtener_cotizaciones(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        estado: Optional[EstadoCotizacion] = None,
        cliente_id: Optional[int] = None
    ) -> List[Cotizacion]:
        """Obtiene lista de cotizaciones con filtros"""
        query = db.query(Cotizacion).options(
            joinedload(Cotizacion.cliente),
            joinedload(Cotizacion.automovil),
            joinedload(Cotizacion.empleado),
            joinedload(Cotizacion.items)
        )
        
        if estado:
            query = query.filter(Cotizacion.estado == estado)
        
        if cliente_id:
            query = query.filter(Cotizacion.cliente_id == cliente_id)
        
        return query.order_by(desc(Cotizacion.created_at)).offset(skip).limit(limit).all()
    
    @staticmethod
    def obtener_cotizacion_por_id(db: Session, cotizacion_id: int) -> Cotizacion:
        """Obtiene una cotización por ID"""
        cotizacion = db.query(Cotizacion).options(
            joinedload(Cotizacion.cliente),
            joinedload(Cotizacion.automovil),
            joinedload(Cotizacion.empleado),
            joinedload(Cotizacion.items)
        ).filter(Cotizacion.id == cotizacion_id).first()
        
        if not cotizacion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cotización no encontrada"
            )
        
        return cotizacion
    
    @staticmethod
    def actualizar_cotizacion(
        db: Session, 
        cotizacion_id: int, 
        cotizacion_data: CotizacionUpdate
    ) -> Cotizacion:
        """Actualiza una cotización existente"""
        cotizacion = CotizacionController.obtener_cotizacion_por_id(db, cotizacion_id)
        
        # Solo se pueden editar cotizaciones en estado BORRADOR
        if cotizacion.estado != EstadoCotizacion.BORRADOR:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se pueden editar cotizaciones en estado borrador"
            )
        
        # Actualizar campos básicos
        for field, value in cotizacion_data.dict(exclude_unset=True).items():
            if field != "items":
                setattr(cotizacion, field, value)
        
        # Actualizar items si se proporcionan
        if cotizacion_data.items is not None:
            # Eliminar items existentes
            db.query(ItemCotizacion).filter(ItemCotizacion.cotizacion_id == cotizacion_id).delete()
            
            # Crear nuevos items
            items_db = []
            for item_data in cotizacion_data.items:
                precio_total = item_data.precio_unitario * item_data.cantidad
                item_db = ItemCotizacion(
                    cotizacion_id=cotizacion.id,
                    tipo_servicio=item_data.tipo_servicio,
                    descripcion=item_data.descripcion,
                    detalle=item_data.detalle,
                    cantidad=item_data.cantidad,
                    precio_unitario=item_data.precio_unitario,
                    precio_total=precio_total,
                    tiempo_estimado_horas=item_data.tiempo_estimado_horas
                )
                items_db.append(item_db)
                db.add(item_db)
            
            # Recalcular totales
            subtotal, impuestos, total = CotizacionController.calcular_totales(items_db)
            cotizacion.subtotal = subtotal
            cotizacion.impuestos = impuestos
            cotizacion.total = total
        
        db.commit()
        db.refresh(cotizacion)
        return cotizacion
    
    @staticmethod
    def cambiar_estado_cotizacion(
        db: Session, 
        cotizacion_id: int, 
        nuevo_estado: EstadoCotizacion
    ) -> Cotizacion:
        """Cambia el estado de una cotización"""
        cotizacion = CotizacionController.obtener_cotizacion_por_id(db, cotizacion_id)
        
        # Validar transiciones de estado válidas
        transiciones_validas = {
            EstadoCotizacion.BORRADOR: [EstadoCotizacion.ENVIADA],
            EstadoCotizacion.ENVIADA: [EstadoCotizacion.ACEPTADA, EstadoCotizacion.RECHAZADA, EstadoCotizacion.VENCIDA],
            EstadoCotizacion.ACEPTADA: [EstadoCotizacion.CONVERTIDA],
        }
        
        if nuevo_estado not in transiciones_validas.get(cotizacion.estado, []):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No se puede cambiar de {cotizacion.estado} a {nuevo_estado}"
            )
        
        cotizacion.estado = nuevo_estado
        
        if nuevo_estado == EstadoCotizacion.ACEPTADA:
            cotizacion.fecha_aceptacion = datetime.now()
        
        db.commit()
        db.refresh(cotizacion)
        return cotizacion
    
    @staticmethod
    def eliminar_cotizacion(db: Session, cotizacion_id: int) -> bool:
        """Elimina una cotización (solo en estado BORRADOR)"""
        cotizacion = CotizacionController.obtener_cotizacion_por_id(db, cotizacion_id)
        
        if cotizacion.estado != EstadoCotizacion.BORRADOR:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se pueden eliminar cotizaciones en estado borrador"
            )
        
        db.delete(cotizacion)
        db.commit()
        return True
    
    @staticmethod
    def obtener_estadisticas(db: Session) -> dict:
        """Obtiene estadísticas de las cotizaciones"""
        
        # Total de cotizaciones
        total_cotizaciones = db.query(Cotizacion).count()
        
        # Cotizaciones por estado
        cotizaciones_por_estado = {}
        for estado in EstadoCotizacion:
            count = db.query(Cotizacion).filter(Cotizacion.estado == estado).count()
            cotizaciones_por_estado[estado.value] = count
        
        # Valor total de cotizaciones
        valor_total = db.query(func.sum(Cotizacion.total)).scalar() or Decimal('0')
        
        # Cotizaciones vencidas
        cotizaciones_vencidas = db.query(Cotizacion).filter(
            and_(
                Cotizacion.fecha_vencimiento < datetime.now(),
                Cotizacion.estado == EstadoCotizacion.ENVIADA
            )
        ).count()
        
        # Promedio de valor por cotización
        promedio_valor = valor_total / total_cotizaciones if total_cotizaciones > 0 else Decimal('0')
        
        # Servicios más solicitados
        servicios_populares = db.query(
            ItemCotizacion.tipo_servicio,
            func.count(ItemCotizacion.id).label('cantidad'),
            func.sum(ItemCotizacion.precio_total).label('valor_total')
        ).group_by(ItemCotizacion.tipo_servicio).order_by(desc('cantidad')).limit(5).all()
        
        servicios_mas_solicitados = [
            {
                "servicio": servicio.tipo_servicio.value,
                "cantidad": servicio.cantidad,
                "valor_total": float(servicio.valor_total)
            }
            for servicio in servicios_populares
        ]
        
        return {
            "total_cotizaciones": total_cotizaciones,
            "cotizaciones_por_estado": cotizaciones_por_estado,
            "valor_total_cotizaciones": float(valor_total),
            "cotizaciones_vencidas": cotizaciones_vencidas,
            "promedio_valor_cotizacion": float(promedio_valor),
            "servicios_mas_solicitados": servicios_mas_solicitados
        }