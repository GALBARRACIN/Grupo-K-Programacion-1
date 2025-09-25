// src/app/app.routes.ts
import { Routes } from '@angular/router';

import { InicioComponent }             from './pages/inicio/inicio.component';
import { GestionClientesComponent }    from './pages/gestion-clientes/gestion-clientes.component';
import { GestionMenuComponent }        from './pages/gestion-menu/gestion-menu.component';
import { MenuClienteComponent }        from './pages/menu-cliente/menu-cliente.component';
import { PromocionesComponent }        from './pages/promociones/promociones.component';
import { StockComponent }              from './pages/stock/stock.component';
import { RegistroComponent }           from './pages/registro/registro.component';
import { CarritoComponent }            from './pages/carrito/carrito.component';
import { CargarPedidoComponent }       from './pages/cargar-pedido/cargar-pedido.component';
import { CalificacionComponent }       from './pages/calificacion/calificacion.component';
import { HistorialPedidosComponent }   from './pages/historial-pedidos/historial-pedidos.component';
import { EstadoPedidoComponent }       from './pages/estado-pedido/estado-pedido.component';
import { DashboardPedidosComponent }   from './pages/dashboard-pedidos/dashboard-pedidos.component';
import { GestionUsuariosComponent }    from './pages/gestion-usuarios/gestion-usuarios.component';
import { LoginComponent }              from './pages/login/login.component';

export const routes: Routes = [
  { path: '',                   redirectTo: 'inicio',           pathMatch: 'full' },
  { path: 'inicio',             component: InicioComponent,         title: 'Rotiseria La Sabrosa – Inicio' },
  { path: 'clientes',           component: GestionClientesComponent, title: 'Rotiseria La Sabrosa – Clientes' },
  { path: 'gestion-usuarios',   component: GestionUsuariosComponent, title: 'Rotiseria La Sabrosa – Usuarios' },
  { path: 'menu',               component: GestionMenuComponent,     title: 'Rotiseria La Sabrosa – Menú' },
  { path: 'menu-cliente',       component: MenuClienteComponent,     title: 'Rotiseria La Sabrosa – Menú Cliente' },
  { path: 'promociones',        component: PromocionesComponent,     title: 'Rotiseria La Sabrosa – Promociones' },
  { path: 'stock',              component: StockComponent,           title: 'Rotiseria La Sabrosa – Stock' },
  { path: 'registro',           component: RegistroComponent,        title: 'Rotiseria La Sabrosa – Registro' },
  { path: 'carrito',            component: CarritoComponent,         title: 'Rotiseria La Sabrosa – Carrito' },
  { path: 'cargar-pedido',      component: CargarPedidoComponent,    title: 'Rotiseria La Sabrosa – Cargar Pedido' },
  { path: 'calificacion',       component: CalificacionComponent,    title: 'Rotiseria La Sabrosa – Calificación' },
  { path: 'historial',          component: HistorialPedidosComponent,title: 'Rotiseria La Sabrosa – Historial' },
  { path: 'estado-pedido',      component: EstadoPedidoComponent,    title: 'Rotiseria La Sabrosa – Estado del Pedido' },
  { path: 'dashboard-pedidos',  component: DashboardPedidosComponent, title: 'Rotiseria La Sabrosa – Dashboard Pedidos' },
  { path: 'login',              component: LoginComponent,            title: 'Rotiseria La Sabrosa – Cerrar sesión' },
  { path: '**',                 redirectTo: 'inicio' }
];
