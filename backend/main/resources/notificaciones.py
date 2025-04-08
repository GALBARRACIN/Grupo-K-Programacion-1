from flask_restful import Resource
from flask import request
from .. import db
from main.models import NotificacionModel

class Notificaciones(Resource):
    def get(self):
        notificaciones = Notificacion.query.all()
        return [n.to_dict() for n in notificaciones], 200

    def post(self):
        data = request.get_json()

        nueva = Notificacion(
            usuario_id=data.get("usuario_id"),
            tipo=data.get("tipo"),
            mensaje=data.get("mensaje"),
            leida=data.get("leida", False)  # opcional, por defecto False
        )

        db.session.add(nueva)
        db.session.commit()

        return {
            "mensaje": "Notificación creada exitosamente",
            "notificacion": nueva.to_dict()
        }, 201
