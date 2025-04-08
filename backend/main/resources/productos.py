from flask_restful import Resource
from flask import request

PRODUCTOS = {
    1: {"nombre": "Empanada", "precio": 200},
    2: {"nombre": "Pizza", "precio": 1200}
}

class Productos(Resource):
    def get(self):
        return PRODUCTOS

    def post(self):
        data = request.get_json()
        new_id = max(PRODUCTOS.keys()) + 1
        PRODUCTOS[new_id] = data
        return {"mensaje": "Producto creado", "id": new_id}, 201

class Producto(Resource):
    def get(self, id):
        return PRODUCTOS.get(id, {"error": "Producto no encontrado"}), 200

    def put(self, id):
        data = request.get_json()
        if id in PRODUCTOS:
            PRODUCTOS[id].update(data)
            return {"mensaje": f"Producto {id} editado"}
        return {"error": "Producto no encontrado"}, 404

    def delete(self, id):
        if id in PRODUCTOS:
            del PRODUCTOS[id]
            return {"mensaje": f"Producto {id} eliminado"}
        return {"error": "Producto no encontrado"}, 404