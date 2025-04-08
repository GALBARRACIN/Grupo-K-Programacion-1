from flask import Blueprint, jsonify, request

pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/', methods=['GET'])
def get_pedidos():
    return jsonify({"mensaje": "Lista de pedidos"}), 200

@pedidos_bp.route('/', methods=['POST'])
def crear_pedido():
    data = request.json
    return jsonify({"mensaje": "Pedido creado", "datos": data}), 201

@pedidos_bp.route('/<int:id>', methods=['GET'])
def get_pedido(id):
    return jsonify({"mensaje": f"Pedido con ID {id}"}), 200

@pedidos_bp.route('/<int:id>', methods=['PUT'])
def editar_pedido(id):
    data = request.json
    return jsonify({"mensaje": f"Pedido {id} editado", "datos": data}), 200

@pedidos_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_pedido(id):
    return jsonify({"mensaje": f"Pedido {id} eliminado o cancelado"}), 200
