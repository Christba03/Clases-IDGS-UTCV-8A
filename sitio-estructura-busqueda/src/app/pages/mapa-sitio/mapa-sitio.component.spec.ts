import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MapaSitioComponent } from './mapa-sitio.component';

describe('MapaSitioComponent', () => {
  let component: MapaSitioComponent;
  let fixture: ComponentFixture<MapaSitioComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MapaSitioComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MapaSitioComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
