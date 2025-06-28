# main/resources/__init__.py

# ───────────────────────────────
# 📁 Usuarios
# ───────────────────────────────
# Colección completa y un usuario individual
from .usuarios import Usuarios as UsuariosResource
from .usuarios import Usuario as UsuarioResource

# ───────────────────────────────
# 📁 Productos
# ───────────────────────────────
# Productos múltiples y detalle por ID
from .productos import Productos as ProductosResource
from .productos import Producto as ProductoResource

# ───────────────────────────────
# 📁 Pedidos
# ───────────────────────────────
# Listado y gestión individual
from .pedidos import Pedidos as PedidosResource
from .pedidos import Pedido as PedidoResource

# ───────────────────────────────
# 📁 Notificaciones
# ───────────────────────────────
from .notificaciones import Notificaciones as NotificacionesResource

# ───────────────────────────────
# 📁 Valoraciones
# ───────────────────────────────
from .valoraciones import Valoraciones as ValoracionesResource

# 🔹 Opcional: si más adelante agregás recursos específicos de autenticación (ej: LoginResource)
# podés descomentar e integrarlos aquí
# from .auth import Login as LoginResource
# from .auth import Logout as LogoutResource
