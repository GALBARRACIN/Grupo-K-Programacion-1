from flask_restful import Resource
from flask import request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.models import NotificacionModel, UsuarioModel
from .. import db
from main.auth.decorators import role_required

class Notificaciones(Resource):
    @jwt_required()
    def get(self):
        """
        Listar notificaciones.
        - Usuarios no admin ven solo las suyas.
        """
        current_id = get_jwt_identity()
        current = UsuarioModel.query.get(current_id)

        usuario_id = request.args.get('usuario_id', type=int)
        tipo = request.args.get('tipo')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        query = NotificacionModel.query
        if tipo:
            query = query.filter_by(tipo=tipo)
        if current.rol not in ['admin', 'empleado']:
            query = query.filter_by(usuario_id=current_id)
        elif usuario_id:
            query = query.filter_by(usuario_id=usuario_id)

        notifs = query.paginate(page=page, per_page=per_page, error_out=False)
        return jsonify({
            'notificaciones': [n.to_json() for n in notifs.items],
            'total': notifs.total,
            'pages': notifs.pages,
            'page': page
        })

    @jwt_required()
    @role_required(roles=["admin", "empleado"])
    def post(self):
        """
        Enviar nueva notificación.
        Solo personal autorizado.
        """
        data = request.get_json(force=True)
        if 'usuario_id' not in data or 'mensaje' not in data:
            return {'message': 'usuario_id y mensaje requeridos'}, 400

        n = NotificacionModel(
            usuario_id=data['usuario_id'],
            mensaje=data['mensaje'],
            tipo=data.get('tipo', 'info'),
            leida=False
        )
        try:
            db.session.add(n)
            db.session.commit()
            return n.to_json(), 201
        except Exception as e:
            db.session.rollback()
            abort(500, description=str(e))