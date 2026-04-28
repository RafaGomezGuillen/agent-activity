import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

// PrimeNG
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { SelectModule } from 'primeng/select';
import { TagModule } from 'primeng/tag';
import { CardModule } from 'primeng/card';
import { TooltipModule } from 'primeng/tooltip';
import { DialogModule } from 'primeng/dialog';
import { ProgressBarModule } from 'primeng/progressbar';
import { SkeletonModule } from 'primeng/skeleton';
import { ToastModule } from 'primeng/toast';
import { PaginatorModule } from 'primeng/paginator';
import { BadgeModule } from 'primeng/badge';
import { DatePickerModule } from 'primeng/datepicker';
import { TextareaModule } from 'primeng/textarea';
import { ToolbarModule } from 'primeng/toolbar';
import { DividerModule } from 'primeng/divider';
import { ChipModule } from 'primeng/chip';
import { IconFieldModule } from 'primeng/iconfield';
import { InputIconModule } from 'primeng/inputicon';

import { StatCardComponent } from './components/stat-card/stat-card.component';
import { StatusBadgeComponent } from './components/status-badge/status-badge.component';
import { PageHeaderComponent } from './components/page-header/page-header.component';

const PRIMENG = [
  TableModule,
  ButtonModule,
  InputTextModule,
  SelectModule,
  TagModule,
  CardModule,
  TooltipModule,
  DialogModule,
  ProgressBarModule,
  SkeletonModule,
  ToastModule,
  PaginatorModule,
  BadgeModule,
  DatePickerModule,
  TextareaModule,
  ToolbarModule,
  DividerModule,
  ChipModule,
  IconFieldModule,
  InputIconModule,
];

@NgModule({
  declarations: [StatCardComponent, StatusBadgeComponent, PageHeaderComponent],
  imports: [CommonModule, RouterModule, FormsModule, ReactiveFormsModule, ...PRIMENG],
  exports: [
    CommonModule,
    RouterModule,
    FormsModule,
    ReactiveFormsModule,
    StatCardComponent,
    StatusBadgeComponent,
    PageHeaderComponent,
    ...PRIMENG,
  ],
})
export class SharedModule {}
