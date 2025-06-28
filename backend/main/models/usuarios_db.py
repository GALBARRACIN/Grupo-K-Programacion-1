from .. import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuarios(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(255))
    _password_hash = db.Column("password_hash", db.String(128), nullable=False)
    rol = db.Column(db.String(50), default='user')

    # Relaciones
    notificaciones = db.relationship("Notificaciones", back_populates="usuario", cascade="all, delete-orphan")
    pedidos = db.relationship("Pedidos", back_populates="usuario", cascade="all, delete-orphan")
    valoraciones = db.relationship("Valoraciones", back_populates="usuario", cascade="all, delete-orphan")

    # Manejo seguro de contraseñas
    @property
    def contrasena_plana(self):
        raise AttributeError("La contraseña no se puede leer directamente.")
    
    @contrasena_plana.setter
    def contrasena_plana(self, contrasena):
        self._password_hash = generate_password_hash(contrasena)

    def validate_pass(self, contrasena):
        return check_password_hash(self._password_hash, contrasena)

    def to_json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'telefono': self.telefono or '',
            'direccion': self.direccion or '',
            'rol': self.rol
        }

    @staticmethod
    def from_json(json_data):
        user = Usuarios(
            nombre=json_data.get('nombre'),
            email=json_data.get('email'),
            telefono=json_data.get('telefono'),
            direccion=json_data.get('direccion'),
            rol=json_data.get('rol', 'user')
        )
        if json_data.get('password'):
            user.contrasena_plana = json_data.get('password')
        return user