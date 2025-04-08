from flask_restful import Resource
from flask import request
from main.models import PedidoModel
from .. import db

class Pedido(Resource):
    def get(self):
        pedidos = Pedido.query.all()
        return [p.to_dict() for p in pedidos], 200

    def post(self):
        data = request.get_json()
        nuevo_pedido = Pedido(cliente=data["cliente"], producto=data["producto"])
        db.session.add(nuevo_pedido)
        db.session.commit()
        return {"mensaje": "Pedido creado", "id": nuevo_pedido.id}, 201

class Pedidos(Resource):
    def get(self, id):
        pedido = Pedido.query.get(id)
        if pedido:
            return pedido.to_dict(), 200
        return {"error": "Pedido no encontrado"}, 404

    def put(self, id):
        pedido = Pedido.query.get(id)
        if not pedido:
            return {"error": "Pedido no encontrado"}, 404

        data = request.get_json()
        pedido.cliente = data.get("cliente", pedido.cliente)
        pedido.producto = data.get("producto", pedido.producto)
        db.session.commit()
        return {"mensaje": f"Pedido {id} editado"}, 200

    def delete(self, id):
        pedido = Pedido.query.get(id)
        if not pedido:
            return {"error": "Pedido no encontrado"}, 404

        db.session.delete(pedido)
        db.session.commit()
        return {"mensaje": f"Pedido {id} cancelado"}, 200