import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule }      from '@angular/router/testing';
import { FormsModule }              from '@angular/forms';

import { RegistroComponent }        from './registro.component';

describe('RegistroComponent', () => {
  let component: RegistroComponent;
  let fixture: ComponentFixture<RegistroComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        RouterTestingModule,
        FormsModule,
        RegistroComponent
      ]
    }).compileComponents();

    fixture   = TestBed.createComponent(RegistroComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create registro component', () => {
    expect(component).toBeTruthy();
  });
});
