import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule }      from '@angular/router/testing';

import { GestionUsuariosComponent } from './gestion-usuarios.component';

describe('GestionUsuariosComponent', () => {
  let component: GestionUsuariosComponent;
  let fixture: ComponentFixture<GestionUsuariosComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        RouterTestingModule,
        GestionUsuariosComponent
      ]
    }).compileComponents();

    fixture   = TestBed.createComponent(GestionUsuariosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create gestion-usuarios component', () => {
    expect(component).toBeTruthy();
  });
});
