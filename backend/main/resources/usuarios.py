from flask_restful import Resource
from flask import request, jsonify, abort
from main.models import UsuarioModel
from .. import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import role_required

class Usuarios(Resource):
    # Endpoint para obtener listado de usuarios y crear nuevos
    @jwt_required()  # Requiere autenticación JWT
    @role_required(roles=["admin", "empleado"])  # Solo accesible para admin/empleado
    def get(self):
        """
        Obtiene listado paginado de usuarios con filtros opcionales
        Parámetros GET opcionales:
        - page: Número de página (default: 1)
        - per_page: Items por página (default: 10)
        - nombre: Filtro por nombre (búsqueda parcial)
        - email: Filtro por email (búsqueda parcial)
        - estado: Filtro por estado exacto
        - sortby_nombre: Ordenamiento (asc/desc)
        """
        try:
            # Configuración de paginación
            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=10, type=int)
            
            # Query base sin ejecutar
            query = UsuarioModel.query

            # Sistema de filtrado dinámico
            if request.args.get('nombre'):
                # Búsqueda insensible a mayúsculas/minúsculas
                query = query.filter(UsuarioModel.nombre.ilike(f"%{request.args.get('nombre')}%"))
            if request.args.get('email'):
                query = query.filter(UsuarioModel.email.ilike(f"%{request.args.get('email')}%"))
            if request.args.get('estado'):
                # Filtro exacto por estado
                query = query.filter(UsuarioModel.estado == request.args.get('estado'))

            # Sistema de ordenamiento
            if request.args.get('sortby_nombre'):
                order = UsuarioModel.nombre.desc() if request.args.get('sortby_nombre') == 'desc' else UsuarioModel.nombre.asc()
                query = query.order_by(order)

            # Ejecuta la consulta paginada
            usuarios = query.paginate(page=page, per_page=per_page, error_out=False)

            # Estructura de respuesta estándar
            return jsonify({
                'usuarios': [u.to_json() for u in usuarios.items],  # Lista de usuarios serializados
                'total': usuarios.total,      # Total de registros
                'pages': usuarios.pages,      # Total de páginas
                'page': page                  # Página actual
            })

        except Exception as e:
            # Manejo centralizado de errores
            abort(500, description=str(e))
    
    def post(self):
        """
        Crea un nuevo usuario
        Campos obligatorios en JSON:
        - nombre
        - email (debe ser único)
        Campos opcionales:
        - password
        """
        data = request.get_json()
        
        # Validación de campos obligatorios
        if not data or 'email' not in data or 'nombre' not in data:
            return {'message': 'Nombre y email requeridos'}, 400
            
        # Verificación de email único
        if UsuarioModel.query.filter_by(email=data['email']).first():
            return {'message': 'El email ya está registrado'}, 400
            
        try:
            # Creación del usuario con valores por defecto
            usuario = UsuarioModel(
                nombre=data['nombre'],
                email=data['email'],
                password=data.get('password'),  # El modelo debe hashear la contraseña
                estado='activo',               # Estado inicial
                rol='usuario'                  # Rol por defecto
            )
            db.session.add(usuario)
            db.session.commit()
            return usuario.to_json(), 201  # HTTP 201: Created
        except Exception as e:
            # Rollback en caso de error
            db.session.rollback()
            abort(500, description=str(e))

class Usuario(Resource):
    # Endpoint para operaciones con usuario específico
    @jwt_required()
    def get(self, id):
        """
        Obtiene detalles de un usuario
        - Usuario actual ve todos sus datos (to_json_complete)
        - Admin/empleado ven todos los datos
        - Otros usuarios ven datos básicos (to_json)
        """
        usuario = UsuarioModel.query.get_or_404(id)  # 404 si no existe
        current_user = UsuarioModel.query.get(get_jwt_identity())  # Usuario actual
        
        # Control de visibilidad diferenciada
        if current_user.id == usuario.id or current_user.rol in ['admin', 'empleado']:
            return usuario.to_json_complete()  # Vista completa
        return usuario.to_json()               # Vista básica

    @jwt_required()
    def put(self, id):
        """
        Actualiza un usuario existente
        - Solo el propio usuario o admin pueden editar
        - No permite modificar el ID
        """
        usuario = UsuarioModel.query.get_or_404(id)
        current_user = UsuarioModel.query.get(get_jwt_identity())
        
        # Autorización: dueño o admin
        if current_user.id != usuario.id and current_user.rol != 'admin':
            return {'message': 'No autorizado'}, 403  # HTTP 403: Forbidden
            
        data = request.get_json()
        try:
            # Actualización dinámica de campos
            for key, value in data.items():
                if key != 'id' and hasattr(usuario, key):  # Protección contra modificación de ID
                    setattr(usuario, key, value)
            db.session.commit()
            return usuario.to_json(), 200
        except Exception as e:
            db.session.rollback()
            abort(500, description=str(e))

    @jwt_required()
    @role_required(roles=["admin", "empleado"])  # Solo para roles específicos
    def delete(self, id):
        """
        Eliminación lógica (bloqueo) de usuario
        - No elimina físicamente el registro
        - Cambia estado a 'bloqueado'
        """
        usuario = UsuarioModel.query.get_or_404(id)
        try:
            # Eliminación lógica (no física)
            usuario.estado = 'bloqueado'
            db.session.commit()
            return {'message': 'Usuario bloqueado'}, 200
        except Exception as e:
            db.session.rollback()
            abort(500, description=str(e))