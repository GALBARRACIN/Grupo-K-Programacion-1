from flask_restful import Resource
from flask import request, jsonify, abort
from main.models import ProductoModel
from .. import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import role_required

class Productos(Resource):
    @jwt_required()  # Requiere que el usuario esté autenticado
    def get(self):
        """
        Lista productos con paginación y filtros opcionales.
        Parámetros GET:
        - page: página actual (default 1)
        - per_page: cantidad por página (default 10)
        - categoria: filtrar por categoría exacta
        - nombre: búsqueda parcial por nombre
        - sortby_nombre: 'asc' o 'desc'
        """
        try:
            # Parámetros de paginación
            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=10, type=int)

            # Query base
            query = ProductoModel.query.filter(ProductoModel.estado != 'inactivo')  # No se listan productos eliminados

            # Filtros opcionales
            if request.args.get('categoria'):
                query = query.filter(ProductoModel.categoria.ilike(f"%{request.args.get('categoria')}%"))
            if request.args.get('nombre'):
                query = query.filter(ProductoModel.nombre.ilike(f"%{request.args.get('nombre')}%"))

            # Ordenamiento opcional
            if request.args.get('sortby_nombre'):
                orden = request.args.get('sortby_nombre')
                query = query.order_by(ProductoModel.nombre.desc() if orden == 'desc' else ProductoModel.nombre.asc())

            # Aplicar paginación
            productos = query.paginate(page=page, per_page=per_page, error_out=False)

            return jsonify({
                'productos': [p.to_json() for p in productos.items],
                'total': productos.total,
                'pages': productos.pages,
                'page': page
            })
        except Exception as e:
            abort(500, description=str(e))

    @jwt_required()
    @role_required(roles=["admin", "empleado"])
    def post(self):
        """
        Crea un nuevo producto.
        Requiere autenticación y rol admin o empleado.
        Campos obligatorios:
        - nombre
        - precio (mayor a 0)
        - descripcion
        """
        data = request.get_json()
        required = ['nombre', 'precio', 'descripcion']
        missing = [f for f in required if f not in data]
        if missing:
            return {'message': f"Faltan campos: {', '.join(missing)}"}, 400

        if data['precio'] <= 0:
            return {'message': "El precio debe ser mayor a 0"}, 400

        try:
            producto = ProductoModel.from_json(data)
            producto.estado = 'activo'  # Estado inicial
            db.session.add(producto)
            db.session.commit()
            return producto.to_json(), 201
        except Exception as e:
            db.session.rollback()
            abort(500, description=f"Error al crear producto: {str(e)}")

class Producto(Resource):
    @jwt_required()
    def get(self, id):
        """
        Obtiene los detalles de un producto específico.
        No muestra productos inactivos.
        """
        producto = ProductoModel.query.get_or_404(id)
        if producto.estado == 'inactivo':
            abort(404, description="Producto no encontrado")
        return producto.to_json()

    @jwt_required()
    @role_required(roles=["admin", "empleado"])
    def put(self, id):
        """
        Actualiza los datos de un producto.
        Solo accesible por admin o empleado.
        """
        producto = ProductoModel.query.get_or_404(id)
        data = request.get_json()

        if 'precio' in data and data['precio'] <= 0:
            return {'message': "El precio debe ser mayor a 0"}, 400

        try:
            for key, value in data.items():
                if key != 'id' and hasattr(producto, key):
                    setattr(producto, key, value)
            db.session.commit()
            return producto.to_json(), 200
        except Exception as e:
            db.session.rollback()
            abort(500, description=f"Error al actualizar producto: {str(e)}")

    @jwt_required()
    @role_required(roles=["admin", "empleado"])
    def delete(self, id):
        """
        Eliminación lógica del producto.
        Cambia el estado a 'inactivo' en lugar de borrarlo físicamente.
        """
        producto = ProductoModel.query.get_or_404(id)
        try:
            producto.estado = 'inactivo'
            db.session.commit()
            return {'message': 'Producto marcado como inactivo'}, 200
        except Exception as e:
            db.session.rollback()
            abort(500, description=f"Error al eliminar producto: {str(e)}")
