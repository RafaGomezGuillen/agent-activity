import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ButtonModule } from 'primeng/button';
import { TooltipModule } from 'primeng/tooltip';
import { BadgeModule } from 'primeng/badge';

import { MainLayoutComponent } from './main-layout/main-layout.component';
import { SidebarComponent } from './sidebar/sidebar.component';
import { TopbarComponent } from './topbar/topbar.component';

@NgModule({
  declarations: [MainLayoutComponent, SidebarComponent, TopbarComponent],
  imports: [CommonModule, RouterModule, ButtonModule, TooltipModule, BadgeModule],
  exports: [MainLayoutComponent],
})
export class LayoutModule {}
