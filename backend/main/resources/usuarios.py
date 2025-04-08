from flask_restful import Resource
from flask import request

USUARIOS = {
    1: {"nombre": "Agus", "email": "agus@mail.com"},
    2: {"nombre": "Gonza", "email": "gonza@mail.com"}
}

class Usuarios(Resource):
    def get(self):
        return USUARIOS

    def post(self):
        data = request.get_json()
        new_id = max(USUARIOS.keys()) + 1
        USUARIOS[new_id] = data
        return {"mensaje": "Usuario creado", "id": new_id}, 201

class Usuario(Resource):
    def get(self, id):
        return USUARIOS.get(id, {"error": "Usuario no encontrado"}), 200

    def put(self, id):
        data = request.get_json()
        if id in USUARIOS:
            USUARIOS[id].update(data)
            return {"mensaje": f"Usuario {id} editado"}
        return {"error": "Usuario no encontrado"}, 404

    def delete(self, id):
        if id in USUARIOS:
            del USUARIOS[id]
            return {"mensaje": f"Usuario {id} eliminado o suspendido"}
        return {"error": "Usuario no encontrado"}, 404
