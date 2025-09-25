import { Component }    from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink }   from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-estado-pedido',
  imports: [
    CommonModule,
    RouterLink
  ],
  templateUrl: './estado-pedido.component.html',
  styleUrls: ['./estado-pedido.component.css']
})
export class EstadoPedidoComponent {}
