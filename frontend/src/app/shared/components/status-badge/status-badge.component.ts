import { Component, Input } from "@angular/core";

@Component({
  selector: "app-status-badge",
  templateUrl: "./status-badge.html",
  standalone: false,
  styles: [],
})
export class StatusBadgeComponent {
  @Input() online = false;
}
