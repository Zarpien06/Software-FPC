from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
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
        """
        Autentica un usuario verificando email y contraseña
        """
        try:
            # Buscar usuario por email
            user = db.query(User).filter(User.correo == login_data.correo).first()
            
            if not user:
                logger.warning(f"Intento de login con email inexistente: {login_data.correo}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciales inválidas"
                )
            
            # Verificar contraseña
            if not password_handler.verify_password(login_data.password, user.password_hash):
                logger.warning(f"Intento de login con contraseña incorrecta para: {login_data.correo}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciales inválidas"
                )
            
            # Verificar que el usuario esté activo
            if not user.is_active():
                logger.warning(f"Intento de login con usuario inactivo: {login_data.correo}")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Usuario inactivo"
                )
            
            logger.info(f"Login exitoso para usuario: {user.correo}")
            return user
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error durante autenticación: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    @staticmethod
    def register_user(db: Session, register_data: RegisterRequest) -> User:
        """
        Registra un nuevo usuario en el sistema
        """
        try:
            # Validar fortaleza de la contraseña
            is_valid, message = password_handler.validate_password_strength(register_data.password)
            if not is_valid:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=message
                )
            
            # Verificar si el email ya existe
            existing_user = db.query(User).filter(User.correo == register_data.correo).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El email ya está registrado"
                )
            
            # Verificar si el número de identificación ya existe
            existing_id = db.query(User).filter(
                User.numero_identificacion == register_data.numero_identificacion,
                User.tipo_identificacion == register_data.tipo_identificacion
            ).first()
            if existing_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El número de identificación ya está registrado"
                )
            
            # Obtener rol de cliente por defecto
            default_role = db.query(Role).filter(Role.nombre == "cliente").first()
            if not default_role:
                logger.error("Rol 'cliente' no encontrado en la base de datos")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error de configuración del sistema"
                )
            
            # Cifrar contraseña
            hashed_password = password_handler.hash_password(register_data.password)
            
            # Crear nuevo usuario
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
            
            logger.info(f"Usuario registrado exitosamente: {new_user.correo}")
            return new_user
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error durante registro: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    @staticmethod
    def create_user_token(user: User) -> TokenResponse:
        """
        Crea un token JWT para el usuario autenticado
        """
        try:
            # Obtener información del rol
            role_name = user.role.nombre if user.role else "sin_rol"
            
            # Crear token
            access_token = auth_handler.create_user_token(
                user_id=user.usuario_id,
                user_email=user.correo,
                user_role=role_name
            )
            
            # Información básica del usuario para el response
            user_info = {
                "usuario_id": user.usuario_id,
                "nombre_completo": user.nombre_completo,
                "correo": user.correo,
                "role": user.role.to_dict() if user.role else None,
                "estado": user.estado if user.estado else None  # <-- Corregido aquí
            }
            
            return TokenResponse(
                access_token=access_token,
                token_type="bearer",
                expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # convertir a segundos
                user_info=user_info
            )
            
        except Exception as e:
            logger.error(f"Error creando token para usuario {user.usuario_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error generando token de acceso"
            )
    
    @staticmethod
    def get_current_user_from_token(db: Session, token: str) -> User:
        """
        Obtiene el usuario actual desde el token JWT
        """
        try:
            # Verificar token y obtener user_id
            user_id = auth_handler.get_user_id_from_token(token)
            
            # Buscar usuario en la base de datos
            user = db.query(User).filter(User.usuario_id == user_id).first()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Usuario no encontrado"
                )
            
            if not user.is_active():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Usuario inactivo"
                )
            
            return user
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error obteniendo usuario actual: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )

# Instancia global del controlador
auth_controller = AuthController()
