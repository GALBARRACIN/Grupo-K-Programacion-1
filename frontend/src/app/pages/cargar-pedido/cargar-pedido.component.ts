import { Component }    from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule }  from '@angular/forms';

@Component({
  standalone: true,
  selector: 'app-cargar-pedido',
  imports: [
    CommonModule,
    FormsModule
  ],
  templateUrl: './cargar-pedido.component.html',
  styleUrls: ['./cargar-pedido.component.css']
})
export class CargarPedidoComponent {}
