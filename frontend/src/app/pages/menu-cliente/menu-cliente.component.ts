import { Component }    from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink }   from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-menu-cliente',
  imports: [
    CommonModule,
    RouterLink
  ],
  templateUrl: './menu-cliente.component.html',
  styleUrls: ['./menu-cliente.component.css']
})
export class MenuClienteComponent {}
