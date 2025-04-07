from flask import Blueprint, jsonify, request

valoraciones_bp = Blueprint('valoraciones', __name__)

@valoraciones_bp.route('/', methods=['POST'])
def agregar_valoracion():
    data = request.json
    return jsonify({"mensaje": "Valoración agregada", "datos": data}), 201

@valoraciones_bp.route('/<int:producto_id>', methods=['GET'])
def obtener_valoracion(producto_id):
    return jsonify({"mensaje": f"Valoraciones del producto {producto_id}"}), 200
