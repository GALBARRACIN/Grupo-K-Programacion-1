from .. import db

class Animal(db.Model):
    ##__tablename__ = 'animales'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    raza = db.Column(db.String(100))

    def __init__(self, nombre, raza):
        self.nombre = nombre
        self.raza = raza

    # Convertir a JSON
    def to_json(self):
        animal_json = {
            'id': self.id,
            'nombre': self.nombre,
            'raza': self.raza
        }
        return animal_json