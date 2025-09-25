import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule }      from '@angular/router/testing';

import { DashboardPedidosComponent } from './dashboard-pedidos.component';

describe('DashboardPedidosComponent', () => {
  let component: DashboardPedidosComponent;
  let fixture: ComponentFixture<DashboardPedidosComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        RouterTestingModule,
        DashboardPedidosComponent
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(DashboardPedidosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create dashboard-pedidos component', () => {
    expect(component).toBeTruthy();
  });
});
