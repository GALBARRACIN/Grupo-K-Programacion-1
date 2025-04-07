from flask import Blueprint, jsonify, request

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/', methods=['GET'])
def get_usuarios():
    return jsonify({"mensaje": "Lista de usuarios"}), 200

@usuarios_bp.route('/', methods=['POST'])
def crear_usuario():
    data = request.json
    return jsonify({"mensaje": "Usuario creado", "datos": data}), 201

@usuarios_bp.route('/<int:id>', methods=['GET'])
def get_usuario(id):
    return jsonify({"mensaje": f"Usuario con ID {id}"}), 200

@usuarios_bp.route('/<int:id>', methods=['PUT'])
def editar_usuario(id):
    data = request.json
    return jsonify({"mensaje": f"Usuario {id} editado", "datos": data}), 200

@usuarios_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    return jsonify({"mensaje": f"Usuario {id} eliminado o suspendido"}), 200
