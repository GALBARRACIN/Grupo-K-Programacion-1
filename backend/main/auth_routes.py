from flask import Blueprint, jsonify, request

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    return jsonify({"mensaje": "Login exitoso", "usuario": data.get("username")}), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({"mensaje": "Sesión cerrada correctamente"}), 200
