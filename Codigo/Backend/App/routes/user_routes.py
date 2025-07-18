# app/routes/users.py

from fastapi import APIRouter, Depends, HTTPException, status, Query, Form, File, UploadFile
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.controllers.user_controller import UserController
from app.schemas.user import UserResponse, UserUpdate, UserListResponse, UserCreate, PasswordChangeRequest
from app.auth.auth_handler import get_current_user, get_current_admin_user
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=UserListResponse)
async def get_all_users(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    role_filter: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    return UserController.get_users_paginated(db, current_user, page, size, search, role_filter, status_filter)


@router.get("/me", response_model=UserResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return UserController.get_user_by_id(db, user_id, current_user)


@router.put("/me", response_model=UserResponse)
async def update_my_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return UserController.update_user(db, current_user.usuario_id, user_update, current_user)


@router.put("/me/form", response_model=UserResponse)
async def update_my_profile_form(
    nombre_completo: str = Form(...),
    correo: str = Form(...),
    telefono: str = Form(...),
    tipo_identificacion: str = Form(...),
    numero_identificacion: str = Form(...),
    foto_perfil: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return UserController.update_user_with_file(
        db=db,
        user_id=current_user.usuario_id,
        current_user=current_user,
        nombre_completo=nombre_completo,
        correo=correo,
        telefono=telefono,
        tipo_identificacion=tipo_identificacion,
        numero_identificacion=numero_identificacion,
        foto_perfil=foto_perfil
    )


@router.put("/{user_id}", response_model=UserResponse)
async def update_user_by_admin_or_self(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return UserController.update_user(db, user_id, user_update, current_user)


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    return UserController.delete_user(db, user_id, current_user)


@router.patch("/{user_id}/toggle-status", response_model=UserResponse)
async def toggle_user_status(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    return UserController.toggle_user_status(db, user_id, current_user)


# ✅ Ruta para cambiar contraseña
@router.put("/{user_id}/change-password")
async def change_password(
    user_id: int,
    password_data: PasswordChangeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return UserController.change_password(db, user_id, password_data, current_user)


# ✅ Ruta para crear un nuevo usuario (solo admin por seguridad)
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    return UserController.create_user(db, user_data)
