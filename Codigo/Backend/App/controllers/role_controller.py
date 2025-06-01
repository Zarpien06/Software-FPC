from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List
from app.models.role import Role
from app.models.user import User
from app.schemas.role import RoleCreate, RoleUpdate, RoleResponse, RoleListResponse, RoleAssignRequest
import logging

logger = logging.getLogger(__name__)

class RoleController:
    
    @staticmethod
    def get_all_roles(db: Session) -> RoleListResponse:
        """
        Obtiene todos los roles del sistema
        """
        try:
            roles = db.query(Role).all()
            
            return RoleListResponse(
                roles=[RoleResponse.from_orm(role) for role in roles],
                total=len(roles)
            )
            
        except Exception as e:
            logger.error(f"Error obteniendo roles: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    @staticmethod
    def get_role_by_id(db: Session, role_id: int) -> Role:
        """
        Obtiene un rol por su ID
        """
        try:
            role = db.query(Role).filter(Role.id == role_id).first()
            
            if not role:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Rol no encontrado"
                )
            
            return role
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error obteniendo rol {role_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    @staticmethod
    def create_role(db: Session, role_data: RoleCreate, current_user: User) -> Role:
        """
        Crea un nuevo rol (solo admin)
        """
        try:
            # Verificar permisos de admin
            if not current_user.is_admin():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Solo los administradores pueden crear roles"
                )
            
            # Verificar si el rol ya existe
            existing_role = db.query(Role).filter(Role.nombre == role_data.nombre).first()
            if existing_role:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe un rol con ese nombre"
                )
            
            # Crear nuevo rol
            new_role = Role(nombre=role_data.nombre)
            
            db.add(new_role)
            db.commit()
            db.refresh(new_role)
            
            logger.info(f"Rol '{new_role.nombre}' creado por usuario {current_user.usuario_id}")
            return new_role
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error creando rol: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    @staticmethod
    def update_role(db: Session, role_id: int, role_update: RoleUpdate, current_user: User) -> Role:
        """
        Actualiza un rol existente (solo admin)
        """
        try:
            # Verificar permisos de admin
            if not current_user.is_admin():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Solo los administradores pueden actualizar roles"
                )
            
            # Obtener rol a actualizar
            role = db.query(Role).filter(Role.id == role_id).first()
            if not role:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Rol no encontrado"
                )
            
            # Verificar que no se esté cambiando a un nombre que ya existe
            if role_update.nombre and role_update.nombre != role.nombre:
                existing_role = db.query(Role).filter(Role.nombre == role_update.nombre).first()
                if existing_role:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Ya existe un rol con ese nombre"
                    )
            
            # Actualizar campos
            if role_update.nombre:
                role.nombre = role_update.nombre
            
            db.commit()
            db.refresh(role)
            
            logger.info(f"Rol {role_id} actualizado por usuario {current_user.usuario_id}")
            return role
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error actualizando rol {role_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    @staticmethod
    def delete_role(db: Session, role_id: int, current_user: User) -> dict:
        """
        Elimina un rol (solo admin)
        """
        try:
            # Verificar permisos de admin
            if not current_user.is_admin():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Solo los administradores pueden eliminar roles"
                )
            
            # Obtener rol a eliminar
            role = db.query(Role).filter(Role.id == role_id).first()
            if not role:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Rol no encontrado"
                )
            
            # Verificar que no haya usuarios con este rol
            users_with_role = db.query(User).filter(User.rol_id == role_id).count()
            if users_with_role > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"No se puede eliminar el rol porque {users_with_role} usuario(s) lo tienen asignado"
                )
            
            # Eliminar rol
            role_name = role.nombre
            db.delete(role)
            db.commit()
            
            logger.info(f"Rol '{role_name}' eliminado por usuario {current_user.usuario_id}")
            return {"message": f"Rol '{role_name}' eliminado exitosamente"}
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error eliminando rol {role_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    @staticmethod
    def assign_role_to_user(db: Session, user_id: int, role_assign: RoleAssignRequest, current_user: User) -> User:
        """
        Asigna un rol a un usuario (solo admin)
        """
        try:
            # Verificar permisos de admin
            if not current_user.is_admin():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Solo los administradores pueden asignar roles"
                )
            
            # Verificar que el usuario existe
            user = db.query(User).filter(User.usuario_id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado"
                )
            
            # Verificar que el rol existe
            role = db.query(Role).filter(Role.id == role_assign.rol_id).first()
            if not role:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Rol no encontrado"
                )
            
            # Asignar rol al usuario
            old_role_id = user.rol_id
            user.rol_id = role_assign.rol_id
            
            db.commit()
            db.refresh(user)
            
            logger.info(f"Rol {role_assign.rol_id} asignado al usuario {user_id} por admin {current_user.usuario_id}")
            return user
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error asignando rol al usuario {user_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )