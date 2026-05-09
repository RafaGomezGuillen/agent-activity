import { Component, Input } from "@angular/core";

@Component({
  selector: "app-page-header",
  templateUrl: "./page-header.html",
  standalone: false,
  styleUrls: ["./page-header.css"],
})
export class PageHeaderComponent {
  @Input() title = "";
  @Input() subtitle = "";
  @Input() breadcrumbRootLabel = "";
  @Input() breadcrumbRootLink: string | any[] | null = null;
  @Input() breadcrumbMiddleLabel = "";
  @Input() breadcrumbMiddleLink: string | any[] | null = null;
  @Input() breadcrumbCurrent = "";
}
