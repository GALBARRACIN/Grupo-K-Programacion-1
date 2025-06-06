from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

from pathlib import Path
import os

# Inicializamos las extensiones: API REST, SQLAlchemy y Flask-Mail
api = Api()
db = SQLAlchemy()
mailsender = Mail()

def create_app():
    app = Flask(__name__)
    load_dotenv()  # Carga variables desde el archivo .env

    # Configuración de la base de datos
    db_dir = Path(os.getenv('DATABASE_PATH'))
    db_name = os.getenv('DATABASE_NAME')
    db_path = db_dir / db_name

    # Asegurarse de que el directorio exista
    db_dir.mkdir(parents=True, exist_ok=True)
    # Crear el archivo de la base de datos si no existe
    if not db_path.exists():
        db_path.touch()

    # Configuración de SQLAlchemy
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(db_path.resolve())

    # Configuración de Flask-Mail
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.example.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() in ['true', '1']
    app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'False').lower() in ['true', '1']
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['FLASKY_MAIL_SENDER'] = os.getenv('FLASKY_MAIL_SENDER', 'no-reply@example.com')

    # Inicializar las extensiones en la aplicación
    db.init_app(app)
    mailsender.init_app(app)

    # Cargar los recursos (API endpoints)
    import main.resources as resources
    api.add_resource(resources.NotificacionesResource, "/notificaciones")

    api.add_resource(resources.PedidosResource, "/pedidos")
    api.add_resource(resources.PedidoResource, "/pedido/<int:id>")

    api.add_resource(resources.ProductosResource, "/productos")
    api.add_resource(resources.ProductoResource, "/producto/<int:id>")
    
    api.add_resource(resources.UsuariosResource, "/usuarios")
    api.add_resource(resources.UsuarioResource, "/usuario/<int:id>")
    
    api.add_resource(resources.ValoracionesResource, "/valoraciones")
    
    api.add_resource(resources.LoginResource, "/login/")
    api.add_resource(resources.LogoutResource, "/logout/")

    # Inicializar la API REST
    api.init_app(app)

    return app
