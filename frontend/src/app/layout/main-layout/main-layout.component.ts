import { Component } from "@angular/core";

@Component({
  selector: "app-main-layout",
  templateUrl: "./main-layout.html",
  standalone: false,
  styles: [
    `
      :host {
        display: flex;
        height: 100vh;
        overflow: hidden;
      }
      .layout-wrapper {
        display: flex;
        width: 100%;
        height: 100%;
      }
      .layout-content {
        flex: 1;
        display: flex;
        flex-direction: column;
        overflow: hidden;
      }
      .page-content {
        flex: 1;
        overflow-y: auto;
        padding: 1.5rem;
      }
    `,
  ],
})
export class MainLayoutComponent {}
