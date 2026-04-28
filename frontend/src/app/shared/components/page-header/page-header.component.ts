import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-page-header',
  template: `
    <div class="mb-6">
      <div class="flex items-center gap-2 text-[var(--text-muted)] text-xs font-mono mb-1">
        <i class="pi pi-chevron-right text-cyan-500/60"></i>
        <span>{{ breadcrumb }}</span>
      </div>
      <h1 class="text-[var(--text-primary)] text-2xl font-bold font-mono tracking-wide">
        <span class="text-cyan-500">// </span>{{ title }}
      </h1>
      <p *ngIf="subtitle" class="text-[var(--text-secondary)] text-sm mt-1 font-mono">{{ subtitle }}</p>
    </div>
  `,
  standalone: false,
  styles: [],
})
export class PageHeaderComponent {
  @Input() title = '';
  @Input() subtitle = '';
  @Input() breadcrumb = '';
}
