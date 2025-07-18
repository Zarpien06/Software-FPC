# app/controllers/user_controller.py

import os
import math
import logging
from uuid import uuid4
from typing import Optional
from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.user import User
from app.models.role import Role
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse, PasswordChangeRequest
from app.auth.password_handler import password_handler
from app.config import settings

logger = logging.getLogger(__name__)

class UserController:

    @staticmethod
    def get_user_by_id(db: Session, user_id: int, current_user: User) -> User:
        user = db.query(User).filter(User.usuario_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        if not current_user.is_admin() and current_user.usuario_id != user_id:
            raise HTTPException(status_code=403, detail="No tienes permisos para ver este usuario")
        return user

    @staticmethod
    def get_users_paginated(db: Session, current_user: User, page=1, size=10, search=None, role_filter=None, status_filter=None):
        if not current_user.is_admin():
            raise HTTPException(status_code=403, detail="Solo los administradores pueden listar usuarios")

        query = db.query(User)

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

        total = query.count()
        offset = (page - 1) * size
        users = query.offset(offset).limit(size).all()
        total_pages = math.ceil(total / size) if total > 0 else 1

        return UserListResponse(
            users=[UserResponse.from_orm(user) for user in users],
            total=total,
            page=page,
            size=size,
            total_pages=total_pages
        )

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        if db.query(User).filter(User.correo == user_data.correo).first():
            raise HTTPException(status_code=400, detail="El correo ya está registrado")

        hashed_password = password_handler.hash_password(user_data.password)
        db_user = User(
            correo=user_data.correo,
            nombre_completo=user_data.nombre_completo,
            numero_identificacion=user_data.numero_identificacion,
            telefono=user_data.telefono,
            tipo_identificacion=user_data.tipo_identificacion,
            password_hash=hashed_password,
            rol_id=user_data.rol_id or 3,  # cliente por defecto
            estado="activo"
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update_user(db: Session, user_id: int, user_update: UserUpdate, current_user: User) -> User:
        user = db.query(User).filter(User.usuario_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        if not current_user.is_admin() and current_user.usuario_id != user_id:
            raise HTTPException(status_code=403, detail="No tienes permisos para actualizar este usuario")

        if not current_user.is_admin() and (user_update.rol_id or user_update.estado):
            raise HTTPException(status_code=403, detail="Solo los administradores pueden cambiar roles o estado")

        if user_update.correo and user_update.correo != user.correo:
            existing = db.query(User).filter(User.correo == user_update.correo, User.usuario_id != user_id).first()
            if existing:
                raise HTTPException(status_code=400, detail="El correo ya está en uso")

        if user_update.numero_identificacion and user_update.numero_identificacion != user.numero_identificacion:
            tipo_id = user_update.tipo_identificacion or user.tipo_identificacion
            existing = db.query(User).filter(
                User.numero_identificacion == user_update.numero_identificacion,
                User.tipo_identificacion == tipo_id,
                User.usuario_id != user_id
            ).first()
            if existing:
                raise HTTPException(status_code=400, detail="El número de identificación ya está en uso")

        if user_update.rol_id:
            if not db.query(Role).filter(Role.id == user_update.rol_id).first():
                raise HTTPException(status_code=400, detail="Rol no válido")

        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update_user_with_file(
        db: Session,
        user_id: int,
        current_user: User,
        nombre_completo: str,
        correo: str,
        telefono: str,
        tipo_identificacion: str,
        numero_identificacion: str,
        foto_perfil: Optional[UploadFile] = None
    ) -> User:
        user = db.query(User).filter(User.usuario_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        if not current_user.is_admin() and current_user.usuario_id != user_id:
            raise HTTPException(status_code=403, detail="No tienes permisos para editar este usuario")

        if correo != user.correo:
            if db.query(User).filter(User.correo == correo, User.usuario_id != user_id).first():
                raise HTTPException(status_code=400, detail="El correo ya está en uso")

        if numero_identificacion != user.numero_identificacion:
            if db.query(User).filter(
                User.numero_identificacion == numero_identificacion,
                User.tipo_identificacion == tipo_identificacion,
                User.usuario_id != user_id
            ).first():
                raise HTTPException(status_code=400, detail="El número de identificación ya está en uso")

        if foto_perfil:
            ext = os.path.splitext(foto_perfil.filename)[-1]
            new_filename = f"{uuid4().hex}{ext}"
            upload_dir = os.path.join(settings.MEDIA_DIR, "usuarios")
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, new_filename)

            with open(file_path, "wb") as f:
                f.write(foto_perfil.file.read())

            user.foto_perfil = f"media/usuarios/{new_filename}"

        user.nombre_completo = nombre_completo
        user.correo = correo
        user.telefono = telefono
        user.tipo_identificacion = tipo_identificacion
        user.numero_identificacion = numero_identificacion

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int, current_user: User) -> dict:
        if not current_user.is_admin():
            raise HTTPException(status_code=403, detail="Solo los administradores pueden eliminar usuarios")
        if current_user.usuario_id == user_id:
            raise HTTPException(status_code=400, detail="No puedes eliminar tu propia cuenta")

        user = db.query(User).filter(User.usuario_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        db.delete(user)
        db.commit()
        return {"message": "Usuario eliminado exitosamente"}

    @staticmethod
    def toggle_user_status(db: Session, user_id: int, current_user: User) -> User:
        if not current_user.is_admin():
            raise HTTPException(status_code=403, detail="Solo los administradores pueden cambiar el estado")

        user = db.query(User).filter(User.usuario_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        user.estado = "inactivo" if user.estado == "activo" else "activo"
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def change_password(db: Session, user_id: int, password_data: PasswordChangeRequest, current_user: User) -> dict:
        if not current_user.is_admin() and current_user.usuario_id != user_id:
            raise HTTPException(status_code=403, detail="No tienes permisos para cambiar esta contraseña")

        user = db.query(User).filter(User.usuario_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        if current_user.usuario_id == user_id:
            if not password_handler.verify_password(password_data.current_password, user.password_hash):
                raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")

        if password_handler.verify_password(password_data.new_password, user.password_hash):
            raise HTTPException(status_code=400, detail="La nueva contraseña debe ser diferente")

        user.password_hash = password_handler.hash_password(password_data.new_password)
        db.commit()
        return {"message": "Contraseña actualizada exitosamente"}
