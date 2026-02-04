import { Routes } from '@angular/router';
import { InicioComponent } from './pages/inicio/inicio.component';
import { ElementosSitioComponent } from './pages/elementos-sitio/elementos-sitio.component';
import { MenuComponent } from './pages/menu/menu.component';
import { Breadcrumb } from './component/shared/breadcrumb/breadcrumb.component';
import { MapaSitioComponent } from './pages/mapa-sitio/mapa-sitio.component';
import { Error404Component } from './pages/error-404/error-404.component';

export const routes: Routes = [
    {
        path:'',
        component:InicioComponent,
        pathMatch:'full'
    },
    {
        path:'elementos',
        component:ElementosSitioComponent,
    },
    {
        path:'menu',
        component:MenuComponent
    },
    {
        path:'breadcrumps',
        component:Breadcrumb
    },
    {
        path:'mapa-sitio',
        component:MapaSitioComponent
    },
    {
        path:'**',
        component:Error404Component
    }

];
