import { Component,signal } from '@angular/core';
import { Layout } from "./layout/layout.component";

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [Layout],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  protected readonly title = signal('sitio-estructura');
}
