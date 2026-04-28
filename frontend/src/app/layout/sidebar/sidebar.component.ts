import { Component } from '@angular/core';

interface NavItem {
  label: string;
  icon: string;
  route: string;
  exact?: boolean;
}

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.html',
  standalone: false,
  styles: [`
    :host { display: block; }
    .nav-item { transition: all 0.2s ease; }
    .nav-item:hover { background: rgba(56, 189, 248, 0.08); }
    .nav-item.active { background: rgba(56, 189, 248, 0.12); border-left-color: #38bdf8; }
  `],
})
export class SidebarComponent {
  navItems: NavItem[] = [
    { label: 'Dashboard', icon: 'pi pi-th-large', route: '/', exact: true },
    { label: 'Agents', icon: 'pi pi-server', route: '/agents' },
    { label: 'Clipboards', icon: 'pi pi-copy', route: '/clipboards' },
    { label: 'Keylogs', icon: 'pi pi-keyboard', route: '/keylogs' },
    { label: 'Screenshots', icon: 'pi pi-image', route: '/screenshots' },
    { label: 'About', icon: 'pi pi-info-circle', route: '/about' },
    { label: 'Docs', icon: 'pi pi-book', route: '/docs' },
  ];
}
