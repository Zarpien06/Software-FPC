from celery import Celery
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.cotizacion import Cotizacion, EstadoCotizacion
from app.services.notification_service import NotificationService

# Configurar Celery (esto iría en un archivo de configuración separado)
celery_app = Celery('fullpaintcars')

@celery_app.task
def verificar_cotizaciones_vencidas():
    """Tarea programada para marcar cotizaciones vencidas"""
    db = SessionLocal()
    try:
        # Buscar cotizaciones vencidas
        cotizaciones_vencidas = db.query(Cotizacion).filter(
            Cotizacion.fecha_vencimiento < datetime.now(),
            Cotizacion.estado == EstadoCotizacion.ENVIADA
        ).all()
        
        for cotizacion in cotizaciones_vencidas:
            cotizacion.estado = EstadoCotizacion.VENCIDA
            NotificationService.enviar_notificacion_cambio_estado(
                cotizacion, EstadoCotizacion.ENVIADA
            )
        
        db.commit()
        return f"Procesadas {len(cotizaciones_vencidas)} cotizaciones vencidas"
        
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

@celery_app.task
def enviar_recordatorios_cotizaciones():
    """Envía recordatorios de cotizaciones próximas a vencer"""
    db = SessionLocal()
    try:
        # Cotizaciones que vencen en 2 días
        fecha_limite = datetime.now() + timedelta(days=2)
        
        cotizaciones_por_vencer = db.query(Cotizacion).filter(
            Cotizacion.fecha_vencimiento <= fecha_limite,
            Cotizacion.fecha_vencimiento > datetime.now(),
            Cotizacion.estado == EstadoCotizacion.ENVIADA
        ).all()
        
        for cotizacion in cotizaciones_por_vencer:
            # Enviar recordatorio al cliente
            pass
        
        return f"Enviados {len(cotizaciones_por_vencer)} recordatorios"
        
    except Exception as e:
        raise e
    finally:
        db.close()