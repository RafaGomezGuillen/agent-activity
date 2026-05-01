import { Component } from "@angular/core";

@Component({
  selector: "app-main-layout",
  templateUrl: "./main-layout.html",
  standalone: false,
  styleUrls: ["./main-layout.css"],
})
export class MainLayoutComponent {
  isSidebarOpen = false;

  toggleSidebar(): void {
    this.isSidebarOpen = !this.isSidebarOpen;
  }

  closeSidebar(): void {
    this.isSidebarOpen = false;
  }
}

