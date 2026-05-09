import { Component, EventEmitter, Output } from "@angular/core";
import { ThemeService } from "../../core/services/theme.service";

@Component({
  selector: "app-topbar",
  templateUrl: "./topbar.html",
  standalone: false,
  styleUrls: ["./topbar.css"],
})
export class TopbarComponent {
  @Output() toggleSidebar = new EventEmitter<void>();

  constructor(public themeService: ThemeService) {}
}
