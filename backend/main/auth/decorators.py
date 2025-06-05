# main/auth/decorators.py

from .. import jwt
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps

# Decorador para restringir el acceso a usuarios/animales por rol
def role_required(roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Verificar que el JWT es correcto
            verify_jwt_in_request()
            # Obtener claims de adentro del JWT
            claims = get_jwt()
            # Verificar que el rol sea uno de los permitidos por la ruta
            if claims['rol'] in roles:
                # Ejecutar la función
                return fn(*args, **kwargs)
            else:
                return jsonify({'message': 'Rol sin permisos de acceso al recurso'}), 403
        return wrapper
    return decorator

# Define el atributo que se utilizará para identificar al usuario
@jwt.user_identity_loader
def user_identity_lookup(animal):
    return animal.id

# Define qué atributos se guardarán dentro del token
@jwt.additional_claims_loader
def add_claims_to_access_token(animal):
    claims = {
        'rol': animal.rol,
        'id': animal.id,
        'email': animal.email
    }
    return claims
