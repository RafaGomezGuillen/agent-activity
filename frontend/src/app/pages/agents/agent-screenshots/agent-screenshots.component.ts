import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ScreenshotService } from '../../../core/services/screenshot.service';
import { AgentService } from '../../../core/services/agent.service';
import { Screenshot, ScreenshotFilters } from '../../../core/models/screenshot.model';
import { Agent } from '../../../core/models/agent.model';

@Component({
  selector: 'app-agent-screenshots',
  templateUrl: './agent-screenshots.html',
  standalone: false,
  styles: [],
})
export class AgentScreenshotsComponent implements OnInit {
  agentId = '';
  agent: Agent | null = null;
  screenshots: Screenshot[] = [];
  total = 0;
  loading = true;

  limit = 24;
  offset = 0;
  dateRange: Date[] | null = null;

  selectedScreenshot: Screenshot | null = null;
  dialogVisible = false;

  constructor(
    private route: ActivatedRoute,
    private screenshotService: ScreenshotService,
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
    const filters: ScreenshotFilters = {
      agent_id: this.agentId,
      limit: this.limit,
      offset: this.offset,
    };
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
    this.dateRange = null;
    this.applyFilters();
  }
}
