from flask_restful import Resource
from flask import request

PEDIDOS = {
    1: {"cliente": "Agus", "producto": "Pizza"},
    2: {"cliente": "Gonza", "producto": "Empanadas"}
}

class Pedidos(Resource):
    def get(self):
        return PEDIDOS

    def post(self):
        data = request.get_json()
        new_id = max(PEDIDOS.keys()) + 1
        PEDIDOS[new_id] = data
        return {"mensaje": "Pedido creado", "id": new_id}, 201

class Pedido(Resource):
    def get(self, id):
        return PEDIDOS.get(id, {"error": "Pedido no encontrado"}), 200

    def put(self, id):
        data = request.get_json()
        if id in PEDIDOS:
            PEDIDOS[id].update(data)
            return {"mensaje": f"Pedido {id} editado"}
        return {"error": "Pedido no encontrado"}, 404

    def delete(self, id):
        if id in PEDIDOS:
            del PEDIDOS[id]
            return {"mensaje": f"Pedido {id} cancelado"}
        return {"error": "Pedido no encontrado"}, 404