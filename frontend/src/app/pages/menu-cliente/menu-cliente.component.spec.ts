import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule }      from '@angular/router/testing';

import { MenuClienteComponent }     from './menu-cliente.component';

describe('MenuClienteComponent', () => {
  let component: MenuClienteComponent;
  let fixture: ComponentFixture<MenuClienteComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        RouterTestingModule,
        MenuClienteComponent
      ]
    }).compileComponents();

    fixture   = TestBed.createComponent(MenuClienteComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create menu-cliente component', () => {
    expect(component).toBeTruthy();
  });
});
