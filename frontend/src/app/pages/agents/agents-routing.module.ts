import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AgentsListComponent } from './agents-list/agents-list.component';
import { AgentDetailComponent } from './agent-detail/agent-detail.component';
import { AgentClipboardsComponent } from './agent-clipboards/agent-clipboards.component';
import { AgentMetricsComponent } from './agent-metrics/agent-metrics.component';
import { AgentKeylogsComponent } from './agent-keylogs/agent-keylogs.component';
import { AgentScreenshotsComponent } from './agent-screenshots/agent-screenshots.component';
import { AgentCommandsComponent } from './agent-commands/agent-commands.component';

const routes: Routes = [
  { path: '', component: AgentsListComponent },
  { path: ':id', component: AgentDetailComponent },
  { path: ':id/clipboards', component: AgentClipboardsComponent },
  { path: ':id/metrics', component: AgentMetricsComponent },
  { path: ':id/keylogs', component: AgentKeylogsComponent },
  { path: ':id/screenshots', component: AgentScreenshotsComponent },
  { path: ':id/commands', component: AgentCommandsComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class AgentsRoutingModule {}
