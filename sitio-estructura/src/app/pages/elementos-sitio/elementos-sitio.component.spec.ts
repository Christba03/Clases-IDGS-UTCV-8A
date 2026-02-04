import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ElementosSitioComponent } from './elementos-sitio.component';

describe('ElementosSitioComponent', () => {
  let component: ElementosSitioComponent;
  let fixture: ComponentFixture<ElementosSitioComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ElementosSitioComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ElementosSitioComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
