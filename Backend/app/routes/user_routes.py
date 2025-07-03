from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.controllers.user_controller import UserController
from app.schemas.user import UserResponse, UserUpdate, UserListResponse
from app.auth.auth_handler import get_current_user, get_current_admin_user
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=UserListResponse)
async def get_all_users(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a devolver"),
    search: Optional[str] = Query(None, description="Buscar por nombre o correo"),
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene todos los usuarios del sistema (solo admin)
    """
    return UserController.get_all_users(db, skip=skip, limit=limit, search=search)

@router.get("/me", response_model=UserResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene el perfil del usuario autenticado
    """
    return current_user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene un usuario específico por ID
    Los usuarios solo pueden ver su propio perfil, los admin pueden ver cualquiera
    """
    # Si no es admin, solo puede ver su propio perfil
    if not current_user.is_admin() and current_user.usuario_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver este usuario"
        )
    
    return UserController.get_user_by_id(db, user_id)

@router.put("/me", response_model=UserResponse)
async def update_my_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualiza el perfil del usuario autenticado
    """
    return UserController.update_user(db, current_user.usuario_id, user_update, current_user)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Actualiza un usuario específico
    Los usuarios solo pueden actualizar su propio perfil, los admin pueden actualizar cualquiera
    """
    # Si no es admin, solo puede actualizar su propio perfil
    if not current_user.is_admin() and current_user.usuario_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar este usuario"
        )
    
    return UserController.update_user(db, user_id, user_update, current_user)

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Elimina un usuario del sistema (solo admin)
    """
    return UserController.delete_user(db, user_id, current_user)

@router.patch("/{user_id}/toggle-status")
async def toggle_user_status(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Activa/desactiva un usuario (solo admin)
    """
    return UserController.toggle_user_status(db, user_id, current_user)