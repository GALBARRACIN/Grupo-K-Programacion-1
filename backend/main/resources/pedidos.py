from flask_restful import Resource
from flask import request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.models import PedidoModel, ItemPedidoModel, ProductoModel, UsuarioModel
from .. import db
from main.auth.decorators import role_required

class Pedidos(Resource):
    @jwt_required()
    def get(self):
        """
        Listar pedidos con filtros por usuario_id y estado.
        - Si no sos admin/empleado, solo ves tus propios pedidos.
        """
        current_user_id = get_jwt_identity()
        current_user = UsuarioModel.query.get(current_user_id)
        
        usuario_id = request.args.get('usuario_id', type=int)
        estado = request.args.get('estado')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        query = PedidoModel.query
        if usuario_id:
            query = query.filter_by(usuario_id=usuario_id)
        if estado:
            query = query.filter_by(estado=estado)

        if current_user.rol not in ['admin', 'empleado']:
            query = query.filter_by(usuario_id=current_user_id)

        pedidos = query.paginate(page=page, per_page=per_page, error_out=False)
        return jsonify({
            'pedidos': [p.to_json() for p in pedidos.items],
            'total': pedidos.total,
            'pages': pedidos.pages,
            'page': page
        })

    @jwt_required()
    @role_required(roles=["admin", "empleado"])
    def post(self):
        """
        Crear un nuevo pedido.
        Solo accessible por admin/empleado.
        """
        data = request.get_json(force=True)
        missing = [f for f in ['usuario_id', 'items'] if f not in data]
        if missing:
            return {'message': f"Faltan campos: {', '.join(missing)}"}, 400
        if not isinstance(data['items'], list) or not data['items']:
            return {'message': "El pedido debe contener al menos un item"}, 400

        pedido = PedidoModel(usuario_id=data['usuario_id'], estado='pendiente', total=0)
        total = 0
        for item in data['items']:
            if 'producto_id' not in item or 'cantidad' not in item:
                return {'message': "Cada item necesita producto_id y cantidad"}, 400
            producto = ProductoModel.query.get(item['producto_id'])
            if not producto:
                return {'message': f"Producto {item['producto_id']} no encontrado"}, 404
            precio = producto.precio
            pedido.items.append(ItemPedidoModel(
                producto_id=item['producto_id'], cantidad=item['cantidad'], precio_unitario=precio))
            total += item['cantidad'] * precio

        pedido.total = total
        try:
            db.session.add(pedido)
            db.session.commit()
            return pedido.to_json(), 201
        except Exception as e:
            db.session.rollback()
            abort(500, description=f"Error al crear pedido: {str(e)}")

class Pedido(Resource):
    @jwt_required()
    def get(self, id):
        """
        Ver detalles de un pedido.
        Solo el dueño, admin o empleado puede verlo.
        """
        pedido = PedidoModel.query.get_or_404(id)
        current = UsuarioModel.query.get(get_jwt_identity())
        if current.rol not in ['admin', 'empleado'] and pedido.usuario_id != current.id:
            return {'message': 'No autorizado'}, 403
        return pedido.to_json()

    @jwt_required()
    @role_required(roles=["admin", "empleado"])
    def put(self, id):
        """
        Actualizar estado del pedido.
        Solo admin/empleado.
        """
        pedido = PedidoModel.query.get_or_404(id)
        data = request.get_json()
        if 'estado' in data:
            validos = ['pendiente', 'preparacion', 'listo', 'entregado', 'cancelado']
            if data['estado'] not in validos:
                return {'message': f"Estado inválido. Use: {', '.join(validos)}"}, 400
            pedido.estado = data['estado']
        try:
            db.session.commit()
            return pedido.to_json(), 200
        except Exception as e:
            db.session.rollback()
            abort(500, description=f"Error al actualizar pedido: {str(e)}")

    @jwt_required()
    @role_required(roles=["admin", "empleado"])
    def delete(self, id):
        """
        Eliminar un pedido físicamente.
        Solo admin/empleado.
        """
        pedido = PedidoModel.query.get_or_404(id)
        try:
            db.session.delete(pedido)
            db.session.commit()
            return {'message': 'Pedido eliminado'}, 200
        except Exception as e:
            db.session.rollback()
            abort(500, description=f"Error al eliminar pedido: {str(e)}")
