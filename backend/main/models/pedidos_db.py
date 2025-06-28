from .. import db
from datetime import datetime

class Pedidos(db.Model):
    __tablename__ = 'pedido'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=True)
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp())
    estado = db.Column(db.String(50), default="pendiente")
    total = db.Column(db.Float, default=0.0)
    
    # Relaciones
    usuario = db.relationship("Usuarios", back_populates="pedidos")
    items = db.relationship("ItemsPedidos", back_populates="pedido", cascade="all, delete-orphan")
    
    def to_json(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'estado': self.estado,
            'total': self.total,
            'items': [item.to_json() for item in self.items]
        }
    
    def to_json_completo(self):
        # Opción para agregar más info anidada
        json_data = self.to_json()
        if self.usuario:
            json_data['usuario'] = {
                'id': self.usuario.id,
                'nombre': getattr(self.usuario, 'nombre', None),
                'email': getattr(self.usuario, 'email', None)
            }
        return json_data

    @staticmethod
    def from_json(data):
        return Pedidos(
            usuario_id=data.get('usuario_id'),
            fecha=data.get('fecha') or datetime.utcnow(),
            estado=data.get('estado', 'pendiente'),
            total=data.get('total', 0.0)
        )