from flask import Flask
import os
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

# Crear app Flask
app = Flask(__name__)

# Registrar rutas
from main.routes import register_routes
register_routes(app)

# Ejecutar
if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv('PORT', 5000)))
