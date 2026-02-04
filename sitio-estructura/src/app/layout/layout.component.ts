import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { Breadcrumb } from '../component/shared/breadcrumb/breadcrumb.component';
@Component({
  selector: 'app-layout',
  imports: [RouterModule, Breadcrumb],
  templateUrl: './layout.component.html',
  styleUrl: './layout.component.css',
  standalone:true
})
export class LayoutComponent {

}
