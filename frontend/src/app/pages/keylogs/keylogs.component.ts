import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { KeylogService } from '../../core/services/keylog.service';
import { AgentService } from '../../core/services/agent.service';
import { Keylog, KeylogFilters } from '../../core/models/keylog.model';
import { Agent } from '../../core/models/agent.model';

@Component({
  selector: 'app-keylogs',
  templateUrl: './keylogs.html',
  standalone: false,
  styles: [],
})
export class KeylogsComponent implements OnInit {
  keylogs: Keylog[] = [];
  agents: Agent[] = [];
  total = 0;
  loading = true;

  limit = 50;
  offset = 0;
  appFilter = '';
  typeFilter = '';
  agentFilter = '';
  dateRange: Date[] | null = null;

  agentOptions: { label: string; value: string }[] = [];
  typeOptions = [
    { label: 'All Types', value: '' },
    { label: 'keypress', value: 'keypress' },
    { label: 'keydown', value: 'keydown' },
    { label: 'keyup', value: 'keyup' },
  ];

  constructor(
    private keylogService: KeylogService,
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
    const filters: KeylogFilters = {
      app: this.appFilter || undefined,
      type: this.typeFilter || undefined,
      limit: this.limit,
      offset: this.offset,
    };
    if (this.agentFilter) filters.agent_id = this.agentFilter;
    if (this.dateRange?.[0]) filters.start_time = this.dateRange[0].toISOString();
    if (this.dateRange?.[1]) filters.end_time = this.dateRange[1].toISOString();

    this.keylogService.getKeylogs(filters).subscribe({
      next: (r) => { this.keylogs = r.data; this.total = r.total; this.loading = false; this.cdr.detectChanges(); },
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
    this.typeFilter = '';
    this.agentFilter = '';
    this.dateRange = null;
    this.applyFilters();
  }

  getAgentHostname(agentId: string): string {
    return this.agents.find((a) => a.id === agentId)?.hostname || agentId;
  }
}
