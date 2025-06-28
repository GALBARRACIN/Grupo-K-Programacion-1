from .. import jwt, db
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps
from main.models import UsuarioModel  # Modelo de usuario

def role_required(roles):
    # Decorador para restringir acceso según roles permitidos
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Verifica que el JWT esté presente y sea válido
            verify_jwt_in_request()
            # Obtiene los claims del token (datos adicionales)
            claims = get_jwt()
            # Chequea si el rol está permitido
            if 'rol' in claims and claims['rol'] in roles:
                return fn(*args, **kwargs)  # Ejecuta la función protegida
            else:
                # Si el rol no tiene permiso, devuelve error 403
                return jsonify({'message': 'Rol sin permisos de acceso al recurso'}), 403
        return wrapper
    return decorator

@jwt.user_identity_loader
def user_identity_lookup(usuario_id):
    # Define qué se guarda como identidad en el token (el ID del usuario)
    return usuario_id

@jwt.additional_claims_loader
def add_claims_to_access_token(usuario_id):
    # Consulta la base para obtener datos adicionales del usuario
    usuario = db.session.query(UsuarioModel).get(usuario_id)
    if not usuario:
        # Si no existe el usuario, devuelve claims vacíos para evitar errores
        return {}
    # Retorna los claims que se guardan en el token (rol, id, email)
    return {
        'rol': usuario.rol,
        'id': usuario.id,
        'email': usuario.email
    }