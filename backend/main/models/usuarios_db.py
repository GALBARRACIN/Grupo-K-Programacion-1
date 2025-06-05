from .. import db
from werkzeug.security import generate_password_hash, check_password_hash # se utiliza para gestionar contraseñas de manera segura en aplicaciones Flask

class Usuarios(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(255))
    password_hash = db.Column(db.String(128), nullable=False)  # Para almacenar la contraseña de manera segura
    rol = db.Column(db.String(50), default='user')  # Campo para distinguir el rol del usuario (e.g., "user", "admin")

    # Relaciones (ajusta según tu aplicación)
    notificaciones = db.relationship("Notificaciones", back_populates="usuario", cascade="all, delete-orphan")
    pedidos = db.relationship("Pedidos", back_populates="usuario", cascade="all, delete-orphan")
    valoraciones = db.relationship("Valoraciones", back_populates="usuario", cascade="all, delete-orphan")
    
    def set_password(self, password):
        """Genera y asigna el hash de la contraseña."""
        self.password_hash = generate_password_hash(password)
    
    def validate_pass(self, password):
        """Valida la contraseña ingresada comparándola con el hash almacenado."""
        return check_password_hash(self.password_hash, password)

    def to_json(self):
        """Serializa el objeto para devolverlo en un JSON."""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'telefono': self.telefono if self.telefono else '',
            'direccion': self.direccion if self.direccion else '',
            'rol': self.rol
        }
    
    @staticmethod
    def from_json(json_data):
        """
        Crea una instancia de Usuarios a partir de un JSON.
        Se espera que el JSON tenga, al menos, 'nombre', 'email' y 'password'.
        """
        user = Usuarios(
            nombre=json_data.get('nombre'),
            email=json_data.get('email'),
            telefono=json_data.get('telefono'),
            direccion=json_data.get('direccion'),
            rol=json_data.get('rol', 'user')  # Asigna 'user' por defecto si no se especifica
        )
        password = json_data.get('password')
        if password:
            user.set_password(password)
        return user
