export type SiteItemType = 'pagina' | 'section' ;
export interface SiteItem {
  id: string;
  title: string;
  description: string;
  path:string
  type: SiteItemType;
  section: string;
  keywords: string[];
  otro?: string;
};

export const SITE_INDEX: SiteItem[] = [
    {
        id:'inicio',
        title:'Inicio',
        description:'Página de inicio del sitio',
        path:'/',
        type:'pagina',
        section:'Estructura del sitio',
        keywords:['inicio','home','principal', 'estructura'],
        otro: "asdasd"
    },
    {
        id:'elementos',
        title:'Elementos del sitio',
        description:'Identifica los elelmentos del sitio web',
        path:'/elementos',
        type:'pagina',
        section:'Estructura del sitio',
        keywords:['elementos','sitio','header', 'footer', 'main','layout'],
    },
    {
        id:'menu',
        title:'Menú',
        description:'Elemntos princiaples del menu web y su utilidad',
        path:'/menu',
        type:'pagina',
        section: 'Navegacion',
        keywords:['menu','navegacion','links', 'navbar','links','persitente'],
    },
    {
        id: 'breadcrumbs',
        title: 'Breadcrumbs',
        description: 'Describe el funcinoamiento y utlidad de los breadcryumbs.',
        path:'/breadcrumbs',
        type: 'pagina',
        section: 'Navegacion',
        keywords: ['breadcrumbs', 'migas', 'ruta', 'navegacion', 'ux'],
    },
    {
        id:'mapa',
        title:'Mapa del sitio',
        description:'Dise;o del mapa del sitio y relacion con la navegacion',
        path: '/mapa-sitio',
        type: 'pagina',
        section: 'Estructura del sitio',
        keywords: ['mapa', 'sitio', 'estructura', 'sitemap', 'rutas'],
    },
    {
        id:'busqueda',
        title:'Búsqueda',
        description:'Búsqueda simple y avanzada dentro del sitio (filtros por tipo y sección).',
        path:'/busqueda',
        type:'pagina',
        section:'Navegacion',
        keywords:['busqueda','buscar','filtros','resultados','sitio','navegacion'],
    },
    {
        id: 'error404',
        title: 'Error 404',
        description: 'Pagina de error 404 personalizada',
        path: '/no-existe',
        section: 'Errores',
        keywords: ['error', '404', 'no encontrada', 'ruta'],
        type: "pagina"
    }
];

