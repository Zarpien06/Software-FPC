from typing import Dict, Any
import logging
from datetime import datetime
from app.models.cotizacion import Cotizacion, EstadoCotizacion

logger = logging.getLogger(__name__)

class NotificationService:
    """Servicio para envío de notificaciones relacionadas con cotizaciones"""
    
    @staticmethod
    def enviar_notificacion_cotizacion_creada(cotizacion: Cotizacion) -> bool:
        """Envía notificación cuando se crea una cotización"""
        try:
            # Aquí iría la lógica para enviar email/SMS al cliente
            mensaje = f"""
            Nueva cotización creada
            
            Número: {cotizacion.numero_cotizacion}
            Cliente: {cotizacion.cliente.nombre} {cotizacion.cliente.apellido}
            Vehículo: {cotizacion.automovil.marca} {cotizacion.automovil.modelo}
            Total: ${cotizacion.total:,.2f}
            
            La cotización estará disponible hasta: {cotizacion.fecha_vencimiento.strftime('%d/%m/%Y')}
            """
            
            logger.info(f"Notificación enviada para cotización {cotizacion.numero_cotizacion}")
            return True
            
        except Exception as e:
            logger.error(f"Error enviando notificación: {str(e)}")
            return False
    
    @staticmethod
    def enviar_notificacion_cambio_estado(cotizacion: Cotizacion, estado_anterior: EstadoCotizacion) -> bool:
        """Envía notificación cuando cambia el estado de una cotización"""
        try:
            mensajes = {
                EstadoCotizacion.ENVIADA: "Su cotización ha sido enviada y está pendiente de revisión",
                EstadoCotizacion.ACEPTADA: "¡Excelente! Su cotización ha sido aceptada",
                EstadoCotizacion.RECHAZADA: "Su cotización ha sido rechazada. Puede solicitar una nueva",
                EstadoCotizacion.VENCIDA: "Su cotización ha vencido. Contacte para renovarla",
                EstadoCotizacion.CONVERTIDA: "Su cotización se ha convertido en orden de trabajo"
            }
            
            mensaje = mensajes.get(cotizacion.estado, "Estado de cotización actualizado")
            
            logger.info(f"Notificación de cambio de estado enviada para cotización {cotizacion.numero_cotizacion}")
            return True
            
        except Exception as e:
            logger.error(f"Error enviando notificación de cambio de estado: {str(e)}")
            return False
