import { NgModule } from "@angular/core";
import { RouterModule, Routes } from "@angular/router";
import { MainLayoutComponent } from "./layout/main-layout/main-layout.component";

const routes: Routes = [
  {
    path: "",
    component: MainLayoutComponent,
    children: [
      {
        path: "",
        loadChildren: () =>
          import("./pages/home/home.module").then((m) => m.HomeModule),
      },
      {
        path: "agents",
        loadChildren: () =>
          import("./pages/agents/agents.module").then((m) => m.AgentsModule),
      },
      {
        path: "clipboards",
        loadChildren: () =>
          import("./pages/clipboards/clipboards.module").then(
            (m) => m.ClipboardsModule,
          ),
      },
      {
        path: "keylogs",
        loadChildren: () =>
          import("./pages/keylogs/keylogs.module").then((m) => m.KeylogsModule),
      },
      {
        path: "screenshots",
        loadChildren: () =>
          import("./pages/screenshots/screenshots.module").then(
            (m) => m.ScreenshotsModule,
          ),
      },
      {
        path: "about",
        loadChildren: () =>
          import("./pages/about/about.module").then((m) => m.AboutModule),
      },
      { path: "**", redirectTo: "" },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
