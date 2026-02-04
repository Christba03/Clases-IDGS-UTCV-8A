import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { delay } from 'rxjs/operators';
import { SITE_INDEX, SiteItem } from '../data/site-index';

/**
 * Define la estructura de los filtros de búsqueda.
 * El signo de interrogación ? significa que la propiedad es opcional (puede no estar presente).
 */
export type SearchFilters = {
  type?: 'todos' | 'pagina' | 'seccion';
  section?: 'todas' | string;
};

/**
 * @Injectable({ providedIn: 'root' })
 *
 * ANALOGÍA:
 * Imagina que este servicio es como una "Herramienta Navaja Suiza" que Angular guarda en una caja de herramientas global (root).
 * Cualquier parte de tu aplicación (componentes) puede pedir prestada esta herramienta para usar sus funciones
 * sin tener que crear una nueva herramienta cada vez (new SearchApi()). Angular se encarga de dársela lista para usar.
 */
@Injectable({ providedIn: 'root' })
export class SearchApi {

  /**
   * Método principal de búsqueda.
   *
   * @param query - El texto que el usuario escribió para buscar.
   * @param filters - Las opciones extra seleccionadas (tipo, sección).
   * @returns Observable<SiteItem[]>
   *
   * ANALOGÍA DE OBSERVABLE:
   * Un Observable no es el dato en sí, sino una "tubería" o un "paquete de Amazon" que está en camino.
   * Cuando llamas a esta función, no recibes los resultados inmediatamente (como cuando compras algo online).
   * Recibes un "número de seguimiento" (el Observable). Te tienes que "suscribir" (estar atento)
   * para abrir el paquete cuando finalmente llegue con los datos adentro.
   */
  search(query: string, filters: SearchFilters): Observable<SiteItem[]> {
    // Limpiamos el texto de búsqueda: quitamos espacios al inicio/final y lo pasamos a minúsculas
    // para que "HOLA" y "hola" sean lo mismo.
    const q = (query || '').trim().toLowerCase();

    // Creamos una copia de los datos originales usando el operador spread (...)
    // Es como sacar una fotocopia de un documento original para poder rayarla y recortarla sin dañar el original.
    let data = [...SITE_INDEX];

    // --- 1) Búsqueda simple (palabras clave) ---
    if (q.length > 0) {
      // .filter() es como un colador. Pasan solo los elementos que cumplen la condición (true).
      data = data.filter(item => {
        // "Pajar" (haystack): Juntamos título, descripción y palabras clave en un solo texto largo.
        const haystack =
          (item.title + ' ' + item.description + ' ' + item.keywords.join(' '))
            .toLowerCase();
        // Buscamos si la "aguja" (q) está dentro del "pajar".
        return haystack.includes(q);
      });
    }

    // --- 2) Búsqueda avanzada (filtros) ---

    // Filtro por tipo (ej: solo mostrar "páginas" o "secciones")
    if (filters.type && filters.type !== 'todos') {
      data = data.filter(item => item.type === filters.type);
    }

    // Filtro por sección (ej: solo mostrar cosas de "Unidad 1")
    if (filters.section && filters.section !== 'todas') {
      data = data.filter(item => item.section === filters.section);
    }

    // simulamos una latencia de red con delay(200) ms.
    // of(...) toma nuestros datos ya filtrados y los empaqueta dentro de un Observable.
    // Es como decir: "Aquí está el paquete, pero el camión tardará 200 milisegundos en entregarlo".
    return of(data).pipe(delay(200));
  }

  /**
   * Obtiene la lista de todas las secciones únicas disponibles.
   * Útil para llenar el menú desplegable (dropdown) en el filtro.
   */
  getSections(): string[] {
    // .map() transforma una lista de objetos en una lista de strings (solo saca la propiedad 'section').
    // new Set() elimina duplicados automáticamente. Es como una colección que no permite cromos repetidos.
    const set = new Set(SITE_INDEX.map(x => x.section));

    // Convertimos el Set de vuelta a un Array y lo ordenamos alfabéticamente.
    return Array.from(set).sort((a, b) => a.localeCompare(b));
  }
}