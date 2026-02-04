import { Component } from '@angular/core';
import { NgFor } from '@angular/common';
import { RouterModule } from '@angular/router';

import { SITE_INDEX, SiteItem } from '../../data/site-index';

@Component({
  selector: 'app-mapa-sitio',
  standalone: true,
  imports: [RouterModule, NgFor],
  templateUrl: './mapa-sitio.component.html',
  styleUrl: './mapa-sitio.component.css'
})
export class MapaSitioComponent {
  readonly groups = groupBySection(SITE_INDEX);
}

type SiteGroup = {
  section: string;
  items: SiteItem[];
};

function groupBySection(items: SiteItem[]): SiteGroup[] {
  const map = new Map<string, SiteItem[]>();

  for (const item of items) {
    const key = (item.section || 'Otros').trim() || 'Otros';
    if (!map.has(key)) map.set(key, []);
    map.get(key)!.push(item);
  }

  const groups: SiteGroup[] = Array.from(map.entries()).map(([section, list]) => ({
    section,
    items: [...list].sort((a, b) => a.title.localeCompare(b.title)),
  }));

  return groups.sort((a, b) => a.section.localeCompare(b.section));
}
