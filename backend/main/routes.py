from .usuarios_routes import usuarios_bp
from .productos_routes import productos_bp
from .pedidos_routes import pedidos_bp
from .auth_routes import auth_bp
from .notificaciones_routes import notificaciones_bp
from .valoraciones_routes import valoraciones_bp

def register_routes(app):
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
    app.register_blueprint(productos_bp, url_prefix='/productos')
    app.register_blueprint(pedidos_bp, url_prefix='/pedidos')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(notificaciones_bp, url_prefix='/notificaciones')
    app.register_blueprint(valoraciones_bp, url_prefix='/valoraciones')
