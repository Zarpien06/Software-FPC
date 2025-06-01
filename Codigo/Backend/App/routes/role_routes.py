from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.role_controller import RoleController
from app.schemas.role import RoleResponse, RoleCreate, RoleUpdate, RoleListResponse, RoleAssignRequest
from app.schemas.user import UserResponse
from app.auth.auth_handler import get_current_user, get_current_admin_user
from app.models.user import User

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("/", response_model=RoleListResponse)
async def get_all_roles(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene todos los roles del sistema
    """
    return RoleController.get_all_roles(db)

@router.get("/{role_id}", response_model=RoleResponse)
async def get_role_by_id(
    role_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene un rol específico por ID
    """
    role = RoleController.get_role_by_id(db, role_id)
    return RoleResponse.from_orm(role)

@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_data: RoleCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo rol (solo admin)
    """
    role = RoleController.create_role(db, role_data, current_user)
    return RoleResponse.from_orm(role)

@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int,
    role_update: RoleUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Actualiza un rol existente (solo admin)
    """
    role = RoleController.update_role(db, role_id, role_update, current_user)
    return RoleResponse.from_orm(role)

@router.delete("/{role_id}")
async def delete_role(
    role_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Elimina un rol (solo admin)
    """
    return RoleController.delete_role(db, role_id, current_user)

@router.post("/assign/{user_id}", response_model=UserResponse)
async def assign_role_to_user(
    user_id: int,
    role_assign: RoleAssignRequest,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Asigna un rol a un usuario (solo admin)
    """
    updated_user = RoleController.assign_role_to_user(db, user_id, role_assign, current_user)
    return UserResponse.from_orm(updated_user)