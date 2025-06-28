from flask_restful import Resource
from flask import request, abort, jsonify
from main.models import ValoracionModel, UsuarioModel
from .. import db
from flask_jwt_extended import jwt_required, get_jwt_identity

class Valoraciones(Resource):
    @jwt_required()
    def get(self):
        """
        Lista valoraciones con opción de filtrar por producto_id.
        Accesible para cualquier usuario autenticado.
        """
        try:
            producto_id = request.args.get('producto_id', type=int)
            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=10, type=int)

            # Query base
            query = ValoracionModel.query

            # Filtro por producto
            if producto_id:
                query = query.filter_by(producto_id=producto_id)

            # Paginación con Flask-SQLAlchemy
            valoraciones = query.paginate(page=page, per_page=per_page, error_out=False)

            return jsonify({
                'valoraciones': [v.to_json() for v in valoraciones.items],
                'total': valoraciones.total,
                'pages': valoraciones.pages,
                'page': page
            })
        except Exception as e:
            abort(500, description=str(e))

    @jwt_required()
    def post(self):
        """
        Crea una nueva valoración.
        El usuario autenticado es quien valora.
        Campos requeridos:
        - producto_id
        - puntuacion (1 a 5)
        """
        json_data = request.get_json(force=True)

        # Validación de campos obligatorios
        required_fields = ['producto_id', 'puntuacion']
        missing_fields = [field for field in required_fields if field not in json_data]
        if missing_fields:
            return {'message': f"Faltan campos obligatorios: {', '.join(missing_fields)}"}, 400

        # Validación del rango de puntuación
        if not (1 <= json_data['puntuacion'] <= 5):
            return {'message': "La puntuación debe estar entre 1 y 5"}, 400

        # Obtener usuario desde el token
        usuario_id = get_jwt_identity()
        json_data['usuario_id'] = usuario_id

        # Verificar si el usuario ya valoró ese producto
        existe = ValoracionModel.query.filter_by(
            usuario_id=usuario_id,
            producto_id=json_data['producto_id']
        ).first()
        if existe:
            return {'message': "Ya valoraste este producto"}, 400

        try:
            valoracion = ValoracionModel.from_json(json_data)
            db.session.add(valoracion)
            db.session.commit()
            return valoracion.to_json(), 201
        except Exception as e:
            db.session.rollback()
            abort(500, description=f"Error al guardar valoración: {str(e)}")