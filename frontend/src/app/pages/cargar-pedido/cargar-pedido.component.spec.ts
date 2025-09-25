import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule }      from '@angular/router/testing';

import { CargarPedidoComponent } from './cargar-pedido.component';

describe('CargarPedidoComponent', () => {
  let component: CargarPedidoComponent;
  let fixture: ComponentFixture<CargarPedidoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        RouterTestingModule,
        CargarPedidoComponent
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(CargarPedidoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create cargar-pedido component', () => {
    expect(component).toBeTruthy();
  });
});
