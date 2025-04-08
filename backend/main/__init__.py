from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

import os

# Inicializamos restful
api = Api()
db = SQLAlchemy()

def create_app():
    load_dotenv()

    app = Flask(__name__)

    db_path = os.getenv('DATABASE_PATH')
    db_name = os.getenv('DATABASE_NAME')

    if not db_path or not db_name:
        raise ValueError("Faltan las variables DATABASE_PATH o DATABASE_NAME en el entorno")

    full_db_path = os.path.join(db_path, db_name)

    if not os.path.exists(full_db_path):
        open(full_db_path, 'a').close()

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{full_db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Cargar los recursos
    import main.resources as resources
    api.add_resource(resources.NotificacionesResource, "/notificaciones")

    api.add_resource(resources.PedidosResource, "/pedidos")
    api.add_resource(resources.PedidoResource, "/pedido/<int:id>")

    api.add_resource(resources.ProductosResource, "/productos")
    api.add_resource(resources.ProductoResource, "/producto/<int:id>")

    api.add_resource(resources.UsuariosResource, "/usuarios")
    api.add_resource(resources.UsuarioResource, "/usuario/<int:id>")

    api.add_resource(resources.ValoracionesResource, "/valoraciones")
    
    api.add_resource(resources.LoginResource, "/login")
    api.add_resource(resources.LogoutResource, "/logout")

    return app
