from flask import Blueprint, jsonify, request

productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/', methods=['GET'])
def get_productos():
    return jsonify({"mensaje": "Lista de productos"}), 200

@productos_bp.route('/', methods=['POST'])
def crear_producto():
    data = request.json
    return jsonify({"mensaje": "Producto creado", "datos": data}), 201

@productos_bp.route('/<int:id>', methods=['GET'])
def get_producto(id):
    return jsonify({"mensaje": f"Producto con ID {id}"}), 200

@productos_bp.route('/<int:id>', methods=['PUT'])
def editar_producto(id):
    data = request.json
    return jsonify({"mensaje": f"Producto {id} editado", "datos": data}), 200

@productos_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    return jsonify({"mensaje": f"Producto {id} eliminado"}), 200
