import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { AgentService } from '../../../core/services/agent.service';
import { Agent, AgentFilters, AgentPagination } from '../../../core/models/agent.model';

@Component({
  selector: 'app-agents-list',
  templateUrl: './agents-list.html',
  standalone: false,
  styles: [],
})
export class AgentsListComponent implements OnInit {
  agents: Agent[] = [];
  total = 0;
  page = 1;
  size = 12;
  loading = true;

  search = '';
  osFilter = '';
  statusFilter: boolean | null = null;

  osOptions = [
    { label: 'All OS', value: '' },
    { label: 'Windows', value: 'Windows' },
    { label: 'Linux', value: 'Linux' },
    { label: 'Darwin', value: 'Darwin' },
  ];

  statusOptions = [
    { label: 'All', value: null },
    { label: 'Online', value: true },
    { label: 'Offline', value: false },
  ];

  constructor(private agentService: AgentService, private cdr: ChangeDetectorRef) {}

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.loading = true;
    const filters: AgentFilters = {
      search: this.search || undefined,
      os: this.osFilter || undefined,
      status: this.statusFilter,
    };
    this.agentService.getAgents(this.page, this.size, filters).subscribe({
      next: (data: AgentPagination) => {
        this.agents = data.items;
        this.total = data.total;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: () => { this.loading = false; this.cdr.detectChanges(); },
    });
  }

  onPageChange(event: any): void {
    this.page = Math.floor(event.first / event.rows) + 1;
    this.size = event.rows;
    this.load();
  }

  applyFilters(): void {
    this.page = 1;
    this.load();
  }

  clearFilters(): void {
    this.search = '';
    this.osFilter = '';
    this.statusFilter = null;
    this.applyFilters();
  }
}
