from flask_restful import Resource
from flask import request

NOTIFICACIONES = {
    1: {"id_emisor": 1, "id_receptor": 3, "mensaje": "Tiene un descuento!"},
    2: {"id_emisor": 2, "id_receptor": 1, "mensaje": "Su pedido está listo"},
    3: {"id_emisor": 3, "id_receptor": 2, "mensaje": "Envío cancelado!"}
}

class Notificaciones(Resource):
    def get(self):
        return NOTIFICACIONES

    def post(self):
        data = request.get_json()
        new_id = max(NOTIFICACIONES.keys()) + 1
        NOTIFICACIONES[new_id] = data
        return {"mensaje": "Notificación enviada", "id": new_id}, 201
