import { Component, OnInit, ChangeDetectorRef } from "@angular/core";
import { ActivatedRoute, Router } from "@angular/router";
import { AgentService } from "../../../core/services/agent.service";
import { MetricService } from "../../../core/services/metric.service";
import { Agent } from "../../../core/models/agent.model";
import { Metric } from "../../../core/models/metric.model";

@Component({
  selector: "app-agent-detail",
  templateUrl: "./agent-detail.html",
  standalone: false,
  styles: [],
})
export class AgentDetailComponent implements OnInit {
  agentId = "";
  agent: Agent | null = null;
  metrics: Metric[] = [];
  loading = true;
  metricsLoading = true;

  chartData: any = {};
  chartOptions: any = {};

  navLinks: { label: string; icon: string; path: string; tooltip: string }[] = [];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private agentService: AgentService,
    private metricService: MetricService,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.agentId = this.route.snapshot.paramMap.get("id") || "";
    this.navLinks = [
      {
        label: "Clipboards",
        icon: "pi pi-clipboard",
        path: `/agents/${this.agentId}/clipboards`,
        tooltip: "View clipboard history",
      },
      {
        label: "Metrics",
        icon: "pi pi-chart-line",
        path: `/agents/${this.agentId}/metrics`,
        tooltip: "View performance metrics",
      },
      {
        label: "Keylogs",
        icon: "pi pi-align-justify",
        path: `/agents/${this.agentId}/keylogs`,
        tooltip: "View keylog history",
      },
      {
        label: "Screenshots",
        icon: "pi pi-image",
        path: `/agents/${this.agentId}/screenshots`,
        tooltip: "View screenshots",
      },
      {
        label: "Commands",
        icon: "pi pi-code",
        path: `/agents/${this.agentId}/commands`,
        tooltip: "View executed commands",
      },
    ];
    this.loadAgent();
    this.loadMetrics();
  }

  loadAgent(): void {
    this.agentService.getAgent(this.agentId).subscribe({
      next: (a) => {
        this.agent = a;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: () => {
        this.loading = false;
        this.cdr.detectChanges();
      },
    });
  }

  loadMetrics(): void {
    this.metricService.getMetrics(this.agentId, { limit: 20 }).subscribe({
      next: (data) => {
        this.metrics = data.items.reverse();
        this.buildChart();
        this.metricsLoading = false;
        this.cdr.detectChanges();
      },
      error: () => {
        this.metricsLoading = false;
        this.cdr.detectChanges();
      },
    });
  }

  buildChart(): void {
    const labels = this.metrics.map((m) =>
      new Date(m.timestamp).toLocaleTimeString(),
    );
    this.chartData = {
      labels,
      datasets: [
        {
          label: "CPU %",
          data: this.metrics.map((m) => m.cpu_usage),
          borderColor: "#38bdf8",
          backgroundColor: "rgba(56,189,248,0.1)",
          tension: 0.4,
          fill: true,
        },
        {
          label: "Memory %",
          data: this.metrics.map((m) => m.memory_used_percent),
          borderColor: "#34d399",
          backgroundColor: "rgba(52,211,153,0.1)",
          tension: 0.4,
          fill: true,
        },
        {
          label: "Disk %",
          data: this.metrics.map((m) => m.disk_used_percent),
          borderColor: "#f59e0b",
          backgroundColor: "rgba(245,158,11,0.1)",
          tension: 0.4,
          fill: true,
        },
      ],
    };
    this.chartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { labels: { color: "#94a3b8", font: { family: "monospace" } } },
      },
      scales: {
        x: {
          ticks: { color: "#475569", font: { family: "monospace", size: 10 } },
          grid: { color: "#1e293b" },
        },
        y: {
          min: 0,
          max: 100,
          ticks: { color: "#475569", font: { family: "monospace", size: 10 } },
          grid: { color: "#1e293b" },
        },
      },
    };
  }
}
