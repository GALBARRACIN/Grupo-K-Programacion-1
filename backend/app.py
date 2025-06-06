from main import create_app
from main import db
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager

# Cargar variables del archivo .env
load_dotenv()

app = create_app()

# Configuración de JWT: utiliza la variable de entorno JWT_SECRET_KEY o una clave por defecto
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'clave-secreta-por-defecto')

# Inicializar JWTManager
jwt = JWTManager(app)

# Registrar los blueprints (por ejemplo, de autenticación)
from main.auth.routes import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# Empujar el contexto de la aplicación para evitar problemas en operaciones fuera de una request
app.app_context().push()

# Ejecutar la aplicación
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host='0.0.0.0', port=os.getenv('PORT'))
