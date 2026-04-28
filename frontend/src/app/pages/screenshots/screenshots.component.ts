import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ScreenshotService } from '../../core/services/screenshot.service';
import { AgentService } from '../../core/services/agent.service';
import { Screenshot, ScreenshotFilters } from '../../core/models/screenshot.model';
import { Agent } from '../../core/models/agent.model';

@Component({
  selector: 'app-screenshots',
  templateUrl: './screenshots.html',
  standalone: false,
  styles: [],
})
export class ScreenshotsComponent implements OnInit {
  screenshots: Screenshot[] = [];
  agents: Agent[] = [];
  total = 0;
  loading = true;

  limit = 24;
  offset = 0;
  agentFilter = '';
  dateRange: Date[] | null = null;

  agentOptions: { label: string; value: string }[] = [];
  selectedScreenshot: Screenshot | null = null;
  dialogVisible = false;

  constructor(
    private screenshotService: ScreenshotService,
    private agentService: AgentService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.agentService.getAgents(1, 100).subscribe((r) => {
      this.agents = r.items;
      this.agentOptions = [
        { label: 'All Agents', value: '' },
        ...r.items.map((a) => ({ label: a.hostname, value: a.id })),
      ];
    });
    this.load();
  }

  load(): void {
    this.loading = true;
    const filters: ScreenshotFilters = { limit: this.limit, offset: this.offset };
    if (this.agentFilter) filters.agent_id = this.agentFilter;
    if (this.dateRange?.[0]) filters.start_time = this.dateRange[0].toISOString();
    if (this.dateRange?.[1]) filters.end_time = this.dateRange[1].toISOString();

    this.screenshotService.getScreenshots(filters).subscribe({
      next: (r) => { this.screenshots = r.items; this.total = r.total; this.loading = false; this.cdr.detectChanges(); },
      error: () => { this.loading = false; this.cdr.detectChanges(); },
    });
  }

  getFileUrl(s: Screenshot): string {
    return this.screenshotService.getScreenshotFileUrl(s.id);
  }

  openDialog(s: Screenshot): void {
    this.selectedScreenshot = s;
    this.dialogVisible = true;
  }

  getAgentHostname(agentId: string): string {
    return this.agents.find((a) => a.id === agentId)?.hostname || agentId;
  }

  onPageChange(event: any): void {
    this.offset = event.first;
    this.limit = event.rows;
    this.load();
  }

  applyFilters(): void {
    this.offset = 0;
    this.load();
  }

  clearFilters(): void {
    this.agentFilter = '';
    this.dateRange = null;
    this.applyFilters();
  }
}
