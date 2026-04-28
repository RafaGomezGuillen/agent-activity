import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { KeylogService } from '../../../core/services/keylog.service';
import { AgentService } from '../../../core/services/agent.service';
import { Keylog, KeylogFilters } from '../../../core/models/keylog.model';
import { Agent } from '../../../core/models/agent.model';

@Component({
  selector: 'app-agent-keylogs',
  templateUrl: './agent-keylogs.html',
  standalone: false,
  styles: [],
})
export class AgentKeylogsComponent implements OnInit {
  agentId = '';
  agent: Agent | null = null;
  keylogs: Keylog[] = [];
  total = 0;
  loading = true;

  limit = 50;
  offset = 0;
  appFilter = '';
  typeFilter = '';
  dateRange: Date[] | null = null;

  typeOptions = [
    { label: 'All Types', value: '' },
    { label: 'keypress', value: 'keypress' },
    { label: 'keydown', value: 'keydown' },
    { label: 'keyup', value: 'keyup' },
  ];

  constructor(
    private route: ActivatedRoute,
    private keylogService: KeylogService,
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
    const filters: KeylogFilters = {
      agent_id: this.agentId,
      app: this.appFilter || undefined,
      type: this.typeFilter || undefined,
      limit: this.limit,
      offset: this.offset,
    };
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
    this.dateRange = null;
    this.applyFilters();
  }
}
