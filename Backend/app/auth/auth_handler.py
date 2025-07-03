# Archivo de compatibilidad para mantener los imports existentes
from app.auth.password_handler import (
    get_current_user, 
    get_current_admin_user,
    get_current_active_user,
    get_password_hash,
    verify_password,
    decode_token,
    JWTBearer,
    auth_handler, 
    password_handler
)

# Re-exportar para mantener compatibilidad
__all__ = [
    'get_current_user', 
    'get_current_admin_user',
    'get_current_active_user',
    'get_password_hash',
    'verify_password',
    'decode_token',
    'auth_handler', 
    'JWTBearer',
    'password_handler'
]