# Cargar variables de entorno desde .env
from dotenv import load_dotenv
load_dotenv()

# Importar la función factory y la base de datos
from main import create_app
from main import db
import os

# Crear la aplicación Flask a partir del factory
app = create_app()

# Empujar el contexto de la aplicación para operaciones fuera de una request
app.app_context().push()

# Ejecutar la aplicación
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
