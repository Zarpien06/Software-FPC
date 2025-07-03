from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.models.role import Role
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.auth.password_handler import auth_handler, password_handler
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class AuthController:
    
    @staticmethod
    def authenticate_user(db: Session, login_data: LoginRequest) -> User:
        try:
            user = db.query(User).filter(User.correo == login_data.correo).first()
            if not user:
                logger.warning(f"Email no encontrado: {login_data.correo}")
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

            if not password_handler.verify_password(login_data.password, user.password_hash):
                logger.warning(f"Contraseña incorrecta para: {login_data.correo}")
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

            if not user.is_active():
                logger.warning(f"Usuario inactivo: {login_data.correo}")
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario inactivo")

            logger.info(f"Login exitoso: {user.correo}")
            return user

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error autenticando usuario: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

    @staticmethod
    def login_user(db: Session, login_data: LoginRequest) -> TokenResponse:
        user = AuthController.authenticate_user(db, login_data)
        return AuthController.create_user_token(user)

    @staticmethod
    def register_user(db: Session, register_data: RegisterRequest) -> User:
        try:
            is_valid, message = password_handler.validate_password_strength(register_data.password)
            if not is_valid:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

            if db.query(User).filter(User.correo == register_data.correo).first():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El email ya está registrado")

            if db.query(User).filter(
                User.numero_identificacion == register_data.numero_identificacion,
                User.tipo_identificacion == register_data.tipo_identificacion
            ).first():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Identificación ya registrada")

            default_role = db.query(Role).filter(Role.nombre == "cliente").first()
            if not default_role:
                logger.error("Rol 'cliente' no encontrado")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error de configuración")

            hashed_password = password_handler.hash_password(register_data.password)

            new_user = User(
                nombre_completo=register_data.nombre_completo,
                correo=register_data.correo,
                telefono=register_data.telefono,
                tipo_identificacion=register_data.tipo_identificacion,
                numero_identificacion=register_data.numero_identificacion,
                password_hash=hashed_password,
                rol_id=default_role.id
            )

            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            logger.info(f"Usuario registrado: {new_user.correo}")
            return new_user

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error registrando usuario: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

    @staticmethod
    def create_user_token(user: User) -> TokenResponse:
        try:
            role_name = user.role.nombre if user.role else "sin_rol"

            token = auth_handler.create_user_token(
                user_id=user.usuario_id,
                user_email=user.correo,
                user_role=role_name
            )

            user_info = {
                "usuario_id": user.usuario_id,
                "nombre_completo": user.nombre_completo,
                "correo": user.correo,
                "role": user.role.to_dict() if user.role else None,
                "estado": user.estado.value if user.estado else None
            }

            return TokenResponse(
                access_token=token,
                token_type="bearer",
                expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                user_info=user_info
            )

        except Exception as e:
            logger.error(f"Error creando token: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error generando token")

    @staticmethod
    def get_current_user_from_token(db: Session, token: str) -> User:
        try:
            user_id = auth_handler.get_user_id_from_token(token)
            user = db.query(User).filter(User.usuario_id == user_id).first()

            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")

            if not user.is_active():
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario inactivo")

            return user

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error obteniendo usuario desde token: {e}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
