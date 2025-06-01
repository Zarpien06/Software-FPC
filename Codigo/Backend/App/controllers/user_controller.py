from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from typing import List, Optional
from app.models.user import User
from app.models.role import Role
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse, PasswordChangeRequest
from app.auth.password_handler import password_handler
import logging
import math

logger = logging.getLogger(__name__)

class UserController:
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int, current_user: User) -> User:
        """
        Obtiene un usuario por su ID
        """
        try:
            user = db.query(User).filter(User.usuario_id == user_id).first()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado"
                )
            
            # Solo admin puede ver otros usuarios, o el usuario puede verse a sí mismo
            if not current_user.is_admin() and current_user.usuario_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permisos para ver este usuario"
                )
            
            return user
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error obteniendo usuario {user_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    @staticmethod
    def get_users_paginated(
        db: Session, 
        current_user: User,
        page: int = 1, 
        size: int = 10,
        search: Optional[str] = None,
        role_filter: Optional[str] = None,
        status_filter: Optional[str] = None
    ) -> UserListResponse:
        """
        Obtiene lista paginada de usuarios (solo admin)
        """
        try:
            # Verificar permisos de admin
            if not current_user.is_admin():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Solo los administradores pueden listar usuarios"
                )
            
            # Construir query base
            query = db.query(User)
            
            # Aplicar filtros
            if search:
                search_term = f"%{search}%"
                query = query.filter(
                    (User.nombre_completo.ilike(search_term)) |
                    (User.correo.ilike(search_term)) |
                    (User.numero_identificacion.ilike(search_term))
                )
            
            if role_filter:
                query = query.join(Role).filter(Role.nombre == role_filter)
            
            if status_filter:
                query = query.filter(User.estado == status_filter)
            
            # Contar total de registros
            total = query.count()
            
            # Aplicar paginación
            offset = (page - 1) * size
            users = query.offset(offset).limit(size).all()
            
            # Calcular total de páginas
            total_pages = math.ceil(total / size) if total > 0 else 1
            
            return UserListResponse(
                users=[UserResponse.from_orm(user) for user in users],
                total=total,
                page=page,
                size=size,
                total_pages=total_pages
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error obteniendo lista de usuarios: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    @staticmethod
    def update_user(db: Session, user_id: int, user_update: UserUpdate, current_user: User) -> User:
        """
        Actualiza un usuario
        """
        try:
            # Obtener usuario a actualizar
            user = db.query(User).filter(User.usuario_id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado"
                )
            
            # Verificar permisos
            can_update = (
                current_user.is_admin() or  # Admin puede actualizar cualquier usuario
                current_user.usuario_id == user_id  # Usuario puede actualizarse a sí mismo
            )
            
            if not can_update:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permisos para actualizar este usuario"
                )
            
            # Solo admin puede cambiar roles y estado
            if not current_user.is_admin():
                if user_update.rol_id is not None or user_update.estado is not None:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Solo los administradores pueden cambiar roles y estado"
                    )
            
            # Verificar email único si se está cambiando
            if user_update.correo and user_update.correo != user.correo:
                existing_email = db.query(User).filter(
                    User.correo == user_update.correo,
                    User.usuario_id != user_id
                ).first()
                if existing_email:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="El email ya está en uso"
                    )
            
            # Verificar número de identificación único si se está cambiando
            if (user_update.numero_identificacion and 
                user_update.numero_identificacion != user.numero_identificacion):
                
                tipo_id = user_update.tipo_identificacion or user.tipo_identificacion
                existing_id = db.query(User).filter(
                    User.numero_identificacion == user_update.numero_identificacion,
                    User.tipo_identificacion == tipo_id,
                    User.usuario_id != user_id
                ).first()
                if existing_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="El número de identificación ya está en uso"
                    )
            
            # Verificar que el rol existe si se está asignando
            if user_update.rol_id:
                role = db.query(Role).filter(Role.id == user_update.rol_id).first()
                if not role:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="El rol especificado no existe"
                    )
            
            # Actualizar campos
            update_data = user_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(user, field, value)
            
            db.commit()
            db.refresh(user)
            
            logger.info(f"Usuario {user_id} actualizado por {current_user.usuario_id}")
            return user
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error actualizando usuario {user_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    @staticmethod
    def delete_user(db: Session, user_id: int, current_user: User) -> dict:
        """
        Elimina un usuario (solo admin)
        """
        try:
            # Verificar permisos de admin
            if not current_user.is_admin():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Solo los administradores pueden eliminar usuarios"
                )
            
            # No permitir que un admin se elimine a sí mismo
            if current_user.usuario_id == user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No puedes eliminar tu propia cuenta"
                )
            
            user = db.query(User).filter(User.usuario_id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado"
                )
            
            db.delete(user)
            db.commit()
            
            logger.info(f"Usuario {user_id} eliminado por {current_user.usuario_id}")
            return {"message": "Usuario eliminado exitosamente"}
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error eliminando usuario {user_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    @staticmethod
    def change_password(db: Session, user_id: int, password_data: PasswordChangeRequest, current_user: User) -> dict:
        """
        Cambia la contraseña de un usuario
        """
        try:
            # Solo el usuario puede cambiar su propia contraseña o un admin
            if not current_user.is_admin() and current_user.usuario_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permisos para cambiar esta contraseña"
                )
            
            user = db.query(User).filter(User.usuario_id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado"
                )
            
            # Verificar contraseña actual (solo si no es admin cambiando la de otro usuario)
            if current_user.usuario_id == user_id:
                if not password_handler.verify_password(password_data.current_password, user.password_hash):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Contraseña actual incorrecta"
                    )
            
            # Verificar que la nueva contraseña sea diferente
            if password_handler.verify_password(password_data.new_password, user.password_hash):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La nueva contraseña debe ser diferente a la actual"
                )
            
            # Cifrar nueva contraseña
            new_password_hash = password_handler.hash_password(password_data.new_password)
            user.password_hash = new_password_hash
            
            db.commit()
            
            logger.info(f"Contraseña cambiada para usuario {user_id}")
            return {"message": "Contraseña actualizada exitosamente"}
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error cambiando contraseña usuario {user_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )

# Instancia global del controlador
user_controller = UserController()
