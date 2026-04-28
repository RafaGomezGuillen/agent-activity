import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { AgentService } from '../../core/services/agent.service';
import { Agent } from '../../core/models/agent.model';

@Component({
  selector: 'app-home',
  templateUrl: './home.html',
  standalone: false,
  styles: [],
})
export class HomeComponent implements OnInit {
  totalAgents = 0;
  onlineAgents = 0;
  offlineAgents = 0;
  recentAgents: Agent[] = [];
  loading = true;

  constructor(private agentService: AgentService, private cdr: ChangeDetectorRef) {}

  ngOnInit(): void {
    this.loadStats();
  }

  loadStats(): void {
    this.agentService.getAgents(1, 100).subscribe({
      next: (data) => {
        this.totalAgents = data.total;
        this.onlineAgents = data.items.filter((a) => a.status).length;
        this.offlineAgents = data.items.filter((a) => !a.status).length;
        this.recentAgents = data.items.slice(0, 5);
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: () => {
        this.loading = false;
        this.cdr.detectChanges();
      },
    });
  }
}
