import { NgModule, provideBrowserGlobalErrorListeners } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";
import { provideHttpClient } from "@angular/common/http";
import { MessageService } from "primeng/api";
import { ToastModule } from "primeng/toast";

import { AppRoutingModule } from "./app-routing-module";
import { App } from "./app";
import { LayoutModule } from "./layout/layout.module";

// Libraries
import { providePrimeNG } from "primeng/config";
import Aura from "@primeuix/themes/aura";

@NgModule({
  declarations: [App],
  imports: [BrowserModule, AppRoutingModule, LayoutModule, ToastModule],
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideHttpClient(),
    MessageService,
    providePrimeNG({
      ripple: true,
      theme: {
        preset: Aura,
        options: {
          darkModeSelector: '.dark',
        },
      },
    }),
  ],
  bootstrap: [App],
})
export class AppModule {}
