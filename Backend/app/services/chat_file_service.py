# app/services/chat_file_service.py
import os
import uuid
import aiofiles
from typing import Optional, Tuple
from fastapi import UploadFile, HTTPException
from PIL import Image
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class ChatFileService:
    """Servicio para gestionar archivos en el chat"""
    
    def __init__(self):
        # Configuración de archivos
        self.upload_dir = "uploads/chat"
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        self.allowed_image_types = {"image/jpeg", "image/png", "image/gif", "image/webp"}
        self.allowed_file_types = {
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "text/plain",
            "application/zip",
            "application/x-zip-compressed"
        }
        
        # Crear directorio si no existe
        os.makedirs(self.upload_dir, exist_ok=True)
        
    async def upload_chat_file(self, file: UploadFile, chat_id: int, user_id: int) -> Tuple[str, str]:
        """
        Subir archivo al chat
        Returns: (file_url, file_type)
        """
        try:
            # Validar tamaño
            content = await file.read()
            if len(content) > self.max_file_size:
                raise HTTPException(
                    status_code=413,
                    detail=f"Archivo muy grande. Máximo {self.max_file_size // (1024*1024)}MB"
                )
            
            # Validar tipo de archivo
            file_type = self._determine_file_type(file.content_type)
            if not file_type:
                raise HTTPException(
                    status_code=415,
                    detail="Tipo de archivo no permitido"
                )
            
            # Generar nombre único
            file_extension = self._get_file_extension(file.filename)
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            
            # Crear subdirectorio por chat
            chat_dir = os.path.join(self.upload_dir, str(chat_id))
            os.makedirs(chat_dir, exist_ok=True)
            
            file_path = os.path.join(chat_dir, unique_filename)
            
            # Guardar archivo
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(content)
            
            # Procesar imagen si es necesario
            if file_type == "IMAGEN":
                await self._process_image(file_path)
            
            # Generar URL
            file_url = f"/api/v1/chat/files/{chat_id}/{unique_filename}"
            
            logger.info(f"Archivo subido: {file_url} por usuario {user_id}")
            
            return file_url, file_type
            
        except Exception as e:
            logger.error(f"Error subiendo archivo: {e}")
            raise HTTPException(status_code=500, detail="Error interno subiendo archivo")
            
    async def get_chat_file(self, chat_id: int, filename: str) -> Optional[str]:
        """Obtener ruta del archivo del chat"""
        try:
            file_path = os.path.join(self.upload_dir, str(chat_id), filename)
            
            if os.path.exists(file_path):
                return file_path
            return None
            
        except Exception as e:
            logger.error(f"Error obteniendo archivo: {e}")
            return None
            
    async def delete_chat_file(self, chat_id: int, filename: str) -> bool:
        """Eliminar archivo del chat"""
        try:
            file_path = os.path.join(self.upload_dir, str(chat_id), filename)
            
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Archivo eliminado: {file_path}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error eliminando archivo: {e}")
            return False
            
    def _determine_file_type(self, content_type: str) -> Optional[str]:
        """Determinar tipo de archivo basado en content-type"""
        if content_type in self.allowed_image_types:
            return "IMAGEN"
        elif content_type in self.allowed_file_types:
            return "ARCHIVO"
        else:
            return None
            
    def _get_file_extension(self, filename: str) -> str:
        """Obtener extensión del archivo"""
        if not filename:
            return ""
        return os.path.splitext(filename)[1].lower()
        
    async def _process_image(self, file_path: str):
        """Procesar imagen (redimensionar, optimizar)"""
        try:
            with Image.open(file_path) as img:
                # Convertir a RGB si es necesario
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Redimensionar si es muy grande
                max_size = (1920, 1080)
                if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    
                # Guardar optimizada
                img.save(file_path, optimize=True, quality=85)
                
        except Exception as e:
            logger.warning(f"Error procesando imagen {file_path}: {e}")
            
    def get_file_info(self, file_path: str) -> dict:
        """Obtener información del archivo"""
        try:
            stat = os.stat(file_path)
            return {
                "size": stat.st_size,
                "created": stat.st_ctime,
                "modified": stat.st_mtime,
                "extension": self._get_file_extension(file_path)
            }
        except Exception as e:
            logger.error(f"Error obteniendo info del archivo: {e}")
            return {}

# Instancia global del servicio
chat_file_service = ChatFileService()