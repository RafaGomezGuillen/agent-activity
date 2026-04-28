import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MetricService } from '../../../core/services/metric.service';
import { AgentService } from '../../../core/services/agent.service';
import { Metric, MetricFilters } from '../../../core/models/metric.model';
import { Agent } from '../../../core/models/agent.model';

@Component({
  selector: 'app-agent-metrics',
  templateUrl: './agent-metrics.html',
  standalone: false,
  styles: [],
})
export class AgentMetricsComponent implements OnInit {
  agentId = '';
  agent: Agent | null = null;
  metrics: Metric[] = [];
  total = 0;
  loading = true;

  limit = 200;
  offset = 0;
  dateRange: Date[] | null = null;

  chartData: any = {};
  networkChartData: any = {};
  chartOptions: any = {};
  networkChartOptions: any = {};

  showCpu = true;
  showMemory = true;
  showDisk = true;

  constructor(
    private route: ActivatedRoute,
    private metricService: MetricService,
    private agentService: AgentService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.agentId = this.route.snapshot.paramMap.get('id') || '';
    this.agentService.getAgent(this.agentId).subscribe((a) => (this.agent = a));
    this.load();
  }

  load(): void {
    this.loading = true;
    const filters: MetricFilters = { limit: this.limit, offset: this.offset };
    if (this.dateRange?.[0]) filters.start_time = this.dateRange[0].toISOString();
    if (this.dateRange?.[1]) filters.end_time = this.dateRange[1].toISOString();

    this.metricService.getMetrics(this.agentId, filters).subscribe({
      next: (r) => {
        this.metrics = r.items.reverse();
        this.total = r.total;
        this.buildCharts();
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: () => { this.loading = false; this.cdr.detectChanges(); },
    });
  }

  buildCharts(): void {
    const labels = this.metrics.map((m) => new Date(m.timestamp).toLocaleTimeString());
    const baseOptions = {
      responsive: true,
      maintainAspectRatio: false,
      animation: false,
      plugins: {
        legend: { labels: { color: '#94a3b8', font: { family: 'monospace', size: 11 } } },
        tooltip: { mode: 'index', intersect: false },
        zoom: { zoom: { wheel: { enabled: true }, pinch: { enabled: true }, mode: 'x' } },
      },
      scales: {
        x: { ticks: { color: '#475569', font: { family: 'monospace', size: 10 }, maxTicksLimit: 15 }, grid: { color: '#1e293b' } },
        y: { ticks: { color: '#475569', font: { family: 'monospace', size: 10 } }, grid: { color: '#1e293b' } },
      },
    };

    const datasets: any[] = [];
    if (this.showCpu) datasets.push({
      label: 'CPU %', data: this.metrics.map((m) => m.cpu_usage.toFixed(1)),
      borderColor: '#38bdf8', backgroundColor: 'rgba(56,189,248,0.1)', tension: 0.3, fill: true,
    });
    if (this.showMemory) datasets.push({
      label: 'Memory %', data: this.metrics.map((m) => m.memory_used_percent.toFixed(1)),
      borderColor: '#34d399', backgroundColor: 'rgba(52,211,153,0.1)', tension: 0.3, fill: true,
    });
    if (this.showDisk) datasets.push({
      label: 'Disk %', data: this.metrics.map((m) => m.disk_used_percent.toFixed(1)),
      borderColor: '#f59e0b', backgroundColor: 'rgba(245,158,11,0.1)', tension: 0.3, fill: true,
    });

    this.chartData = { labels, datasets };
    this.chartOptions = { ...baseOptions, scales: { ...baseOptions.scales, y: { ...baseOptions.scales.y, min: 0, max: 100 } } };

    this.networkChartData = {
      labels,
      datasets: [
        {
          label: 'Upload KB/s', data: this.metrics.map((m) => m.upload_speed_kb.toFixed(2)),
          borderColor: '#a78bfa', backgroundColor: 'rgba(167,139,250,0.1)', tension: 0.3, fill: true,
        },
        {
          label: 'Download KB/s', data: this.metrics.map((m) => m.download_speed_kb.toFixed(2)),
          borderColor: '#fb7185', backgroundColor: 'rgba(251,113,133,0.1)', tension: 0.3, fill: true,
        },
      ],
    };
    this.networkChartOptions = baseOptions;
  }

  toggleMetric(type: 'cpu' | 'memory' | 'disk'): void {
    if (type === 'cpu') this.showCpu = !this.showCpu;
    if (type === 'memory') this.showMemory = !this.showMemory;
    if (type === 'disk') this.showDisk = !this.showDisk;
    this.buildCharts();
  }

  applyFilters(): void {
    this.offset = 0;
    this.load();
  }

  clearFilters(): void {
    this.dateRange = null;
    this.limit = 200;
    this.applyFilters();
  }

  latestMetric(): Metric | null {
    return this.metrics.length ? this.metrics[this.metrics.length - 1] : null;
  }
}
