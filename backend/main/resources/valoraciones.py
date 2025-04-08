from flask_restful import Resource
from flask import request

VALORACIONES = {
    1: {"producto_id": 1, "puntuacion": 5, "comentario": "Muy rico"},
    2: {"producto_id": 2, "puntuacion": 3, "comentario": "Normal"}
}

class Valoraciones(Resource):
    def get(self):
        return VALORACIONES

    def post(self):
        data = request.get_json()
        new_id = max(VALORACIONES.keys()) + 1
        VALORACIONES[new_id] = data
        return {"mensaje": "Valoración agregada", "id": new_id}, 201
