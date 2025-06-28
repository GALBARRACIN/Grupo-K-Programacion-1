# main/__init__.py

import os
from flask import Flask
from dotenv import load_dotenv

from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail

from pathlib import Path

# 🌍 Cargar variables desde .env
load_dotenv()

# 📦 Inicialización global de extensiones
api = Api()
db = SQLAlchemy()
mailsender = Mail()
jwt = JWTManager()

def create_app():
    # 🧪 Crear app Flask con configuración dinámica
    app = Flask(__name__)

    # ───────────────────────────────
    # 🔗 BASE DE DATOS (SQLite)
    # ───────────────────────────────
    db_dir = Path(os.getenv('DATABASE_PATH'))
    db_name = os.getenv('DATABASE_NAME')
    db_path = db_dir / db_name

    # Crear carpeta si no existe
    db_dir.mkdir(parents=True, exist_ok=True)
    # Crear archivo .db si no existe
    if not db_path.exists():
        db_path.touch()

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(db_path.resolve())
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ───────────────────────────────
    # 🔐 CONFIGURACIÓN JWT
    # ───────────────────────────────
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES'))
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ["access", "refresh"]

    # ───────────────────────────────
    # 📧 CONFIGURACIÓN MAIL
    # ───────────────────────────────
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.example.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() in ['true', '1']
    app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'False').lower() in ['true', '1']
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['FLASKY_MAIL_SENDER'] = os.getenv('FLASKY_MAIL_SENDER')
    app.config['MAIL_HOSTNAME'] = os.getenv('MAIL_HOSTNAME')

    # ───────────────────────────────
    # 🔧 Inicializar extensiones
    # ───────────────────────────────
    db.init_app(app)
    mailsender.init_app(app)
    jwt.init_app(app)

    # ───────────────────────────────
    # 🔁 Token revocado: validador y respuesta
    # ───────────────────────────────
    from main.auth.routes import token_blacklist

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        return jwt_payload["jti"] in token_blacklist

    @jwt.revoked_token_loader
    def revoked_token_response(jwt_header, jwt_payload):
        return {"message": "Token revocado o inválido"}, 401

    # ───────────────────────────────
    # 🧩 Rutas y recursos RESTful
    # ───────────────────────────────
    import main.resources as resources
    api.add_resource(resources.NotificacionesResource, "/notificaciones")
    api.add_resource(resources.PedidosResource, "/pedidos")
    api.add_resource(resources.PedidoResource, "/pedido/<int:id>")
    api.add_resource(resources.ProductosResource, "/productos")
    api.add_resource(resources.ProductoResource, "/producto/<int:id>")
    api.add_resource(resources.UsuariosResource, "/usuarios")
    api.add_resource(resources.UsuarioResource, "/usuario/<int:id>")
    api.add_resource(resources.ValoracionesResource, "/valoraciones")
    api.init_app(app)

    # ───────────────────────────────
    # 🔗 Registrar blueprint de autenticación
    # ───────────────────────────────
    from main.auth.routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
