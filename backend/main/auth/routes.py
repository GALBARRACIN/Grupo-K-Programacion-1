# main/auth/routes.py

from flask import request, jsonify, Blueprint
from main.models.usuarios_db import Usuarios as UsuarioModel
from main import db
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    jwt_required
)
from main.mail.functions import sendMail  # ✅ Sistema de envío de mails

# 🎯 Blueprint de autenticación, todas las rutas comienzan con /auth
auth = Blueprint('auth', __name__, url_prefix='/auth')

# 🧼 Lista negra de tokens revocados (almacenada en memoria)
token_blacklist = set()

# ✅ LOGIN: genera access y refresh token
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Email y password requeridos'}), 400

    usuario = UsuarioModel.query.filter_by(email=data['email']).first()

    if not usuario or not usuario.validate_pass(data['password']):
        return jsonify({'message': 'Credenciales inválidas'}), 401

    # Generar tokens JWT
    access_token = create_access_token(identity=str(usuario.id))
    refresh_token = create_refresh_token(identity=str(usuario.id))

    return jsonify({
        'message': 'Login exitoso',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'usuario': usuario.to_json()
    }), 200

# ✅ REGISTER: crea usuario y envía correo
@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    usuario = UsuarioModel.from_json(data)

    exists = UsuarioModel.query.filter_by(email=usuario.email).scalar() is not None
    if exists:
        return jsonify({'message': 'Email ya registrado'}), 409

    try:
        db.session.add(usuario)
        db.session.commit()

        # Enviar correo de bienvenida
        sendMail(
            to=usuario.email,
            subject="¡Bienvenido a la Rotisería!",
            template="register",
            usuario=usuario
        )

    except Exception as error:
        db.session.rollback()
        return jsonify({'message': str(error)}), 409

    return jsonify(usuario.to_json()), 201

# ✅ LOGOUT: invalida el token actual agregándolo a la blacklist
@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    token_blacklist.add(jti)
    return jsonify({'message': 'Sesión cerrada'}), 200

# ✅ REFRESH: emite nuevo access token usando un refresh token válido
@auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    return jsonify({
        'access_token': new_access_token,
        'message': 'Token renovado exitosamente'
    }), 200

# 🔍 Diagnóstico de carga del módulo y del Blueprint
print("🔄 Endpoint /auth/refresh cargado correctamente")