import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-stat-card',
  templateUrl: './stat-card.html',
  standalone: false,
  styles: [],
})
export class StatCardComponent {
  @Input() label = '';
  @Input() value: string | number = '—';
  @Input() icon = 'pi pi-chart-bar';
  @Input() color: 'cyan' | 'emerald' | 'red' | 'amber' | 'purple' = 'cyan';

  get colorClasses(): { bg: string; text: string; border: string } {
    const map: Record<string, { bg: string; text: string; border: string }> = {
      cyan: { bg: 'bg-cyan-500/10', text: 'text-cyan-400', border: 'border-cyan-500/20' },
      emerald: { bg: 'bg-emerald-500/10', text: 'text-emerald-400', border: 'border-emerald-500/20' },
      red: { bg: 'bg-red-500/10', text: 'text-red-400', border: 'border-red-500/20' },
      amber: { bg: 'bg-amber-500/10', text: 'text-amber-400', border: 'border-amber-500/20' },
      purple: { bg: 'bg-purple-500/10', text: 'text-purple-400', border: 'border-purple-500/20' },
    };
    return map[this.color];
  }
}
