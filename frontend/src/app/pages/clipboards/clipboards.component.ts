import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ClipboardService } from '../../core/services/clipboard.service';
import { AgentService } from '../../core/services/agent.service';
import { Clipboard, ClipboardFilters } from '../../core/models/clipboard.model';
import { Agent } from '../../core/models/agent.model';

@Component({
  selector: 'app-clipboards',
  templateUrl: './clipboards.html',
  standalone: false,
  styles: [],
})
export class ClipboardsComponent implements OnInit {
  clipboards: Clipboard[] = [];
  agents: Agent[] = [];
  total = 0;
  loading = true;

  limit = 50;
  offset = 0;
  appFilter = '';
  agentFilter = '';
  dateRange: Date[] | null = null;

  agentOptions: { label: string; value: string }[] = [];

  constructor(
    private clipboardService: ClipboardService,
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
      this.load();
    });
  }

  load(): void {
    this.loading = true;
    const filters: ClipboardFilters = {
      app: this.appFilter || undefined,
      limit: this.limit,
      offset: this.offset,
    };
    if (this.agentFilter) filters.agent_id = this.agentFilter;
    if (this.dateRange?.[0]) filters.start_time = this.dateRange[0].toISOString();
    if (this.dateRange?.[1]) filters.end_time = this.dateRange[1].toISOString();

    this.clipboardService.getClipboards(filters).subscribe({
      next: (r) => { this.clipboards = r.data; this.total = r.total; this.loading = false; this.cdr.detectChanges(); },
      error: () => { this.loading = false; this.cdr.detectChanges(); },
    });
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
    this.appFilter = '';
    this.agentFilter = '';
    this.dateRange = null;
    this.applyFilters();
  }

  getAgentHostname(agentId: string): string {
    return this.agents.find((a) => a.id === agentId)?.hostname || agentId;
  }
}
