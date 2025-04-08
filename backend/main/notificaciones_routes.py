from flask import Blueprint, jsonify, request

notificaciones_bp = Blueprint('notificaciones', __name__)

@notificaciones_bp.route('/', methods=['POST'])
def enviar_notificacion():
    data = request.json
    return jsonify({"mensaje": "Notificación enviada", "datos": data}), 200
