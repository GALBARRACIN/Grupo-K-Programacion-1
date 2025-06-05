# main/auth/routes.py

from flask import request, jsonify, Blueprint
from main.models.usuarios_db import Usuarios as UsuarioModel  # Asegúrate que este alias coincide con tu modelo de usuario
from main import db
from flask_jwt_extended import create_access_token

# Blueprint para los endpoints de autenticación
auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Email y password requeridos'}), 400

    usuario = UsuarioModel.query.filter_by(email=data['email']).first()
    
    if not usuario or not usuario.validate_pass(data['password']):
        return jsonify({'message': 'Credenciales inválidas'}), 401

    # Generar el token JWT pasando el objeto completo para que los loaders configurados (en decorators.py) puedan trabajar
    access_token = create_access_token(identity=usuario)
    
    return jsonify({
        'message': 'Login exitoso',
        'access_token': access_token,
        'usuario': usuario.to_json()
    }), 200

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    usuario = UsuarioModel.from_json(data)
    exists = UsuarioModel.query.filter_by(email=usuario.email).scalar() is not None
    
    if exists:
        return jsonify({'message': 'Duplicated mail'}), 409
    
    try:
        db.session.add(usuario)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        return jsonify({'message': str(error)}), 409

    return jsonify(usuario.to_json()), 201

@auth.route('/logout', methods=['POST'])
def logout():
    # El logout en JWT normalmente se maneja en el cliente o mediante un sistema de revocación de tokens
    return jsonify({'message': 'Sesión cerrada'}), 200
