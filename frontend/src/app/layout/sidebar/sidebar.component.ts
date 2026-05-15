import { Component, EventEmitter, Output } from "@angular/core";
import { ThemeService } from "../../core/services/theme.service";

interface NavItem {
  label: string;
  icon: string;
  route: string;
  exact?: boolean;
}

@Component({
  selector: "app-sidebar",
  templateUrl: "./sidebar.html",
  standalone: false,
  styleUrls: ["./sidebar.css"],
})
export class SidebarComponent {
  @Output() navigateItem = new EventEmitter<void>();

  constructor(public themeService: ThemeService) {}

  navItems: NavItem[] = [
    { label: "Dashboard", icon: "pi pi-th-large", route: "/", exact: true },
    { label: "Agents", icon: "pi pi-server", route: "/agents" },
    { label: "Clipboards", icon: "pi pi-clipboard", route: "/clipboards" },
    { label: "Keylogs", icon: "pi pi-align-justify", route: "/keylogs" },
    { label: "Screenshots", icon: "pi pi-image", route: "/screenshots" },
    { label: "About", icon: "pi pi-info-circle", route: "/about" },
  ];

  onNavigate(): void {
    this.navigateItem.emit();
  }
}
