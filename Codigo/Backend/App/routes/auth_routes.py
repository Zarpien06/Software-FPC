from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.auth_controller import AuthController
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserResponse
from app.auth.password_handler import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Registra un nuevo usuario en el sistema
    """
    return AuthController.register_user(db, user_data)

@router.post("/login", response_model=TokenResponse)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Inicia sesión y devuelve el token de acceso
    """
    user_login =  LoginRequest(
        correo=form_data.username,
        password=form_data.password
    )
    return AuthController.login_user(db, user_login)

@router.post("/login-json", response_model=TokenResponse)
async def login_user_json(
    user_login:  LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Inicia sesión con JSON y devuelve el token de acceso
    """
    return AuthController.login_user(db, user_login)

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene la información del usuario autenticado
    """
    return current_user

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Refresca el token de acceso
    """
    return AuthController.refresh_token(db, current_user)