import { NgModule } from '@angular/core';
import { SharedModule } from '../../shared/shared.module';
import { AgentsRoutingModule } from './agents-routing.module';
import { ChartModule } from 'primeng/chart';
import { TreeModule } from 'primeng/tree';
import { TabsModule } from 'primeng/tabs';
import { AccordionModule } from 'primeng/accordion';

import { AgentsListComponent } from './agents-list/agents-list.component';
import { AgentDetailComponent } from './agent-detail/agent-detail.component';
import { AgentClipboardsComponent } from './agent-clipboards/agent-clipboards.component';
import { AgentMetricsComponent } from './agent-metrics/agent-metrics.component';
import { AgentKeylogsComponent } from './agent-keylogs/agent-keylogs.component';
import { AgentScreenshotsComponent } from './agent-screenshots/agent-screenshots.component';
import { AgentCommandsComponent } from './agent-commands/agent-commands.component';

@NgModule({
  declarations: [
    AgentsListComponent,
    AgentDetailComponent,
    AgentClipboardsComponent,
    AgentMetricsComponent,
    AgentKeylogsComponent,
    AgentScreenshotsComponent,
    AgentCommandsComponent,
  ],
  imports: [SharedModule, AgentsRoutingModule, ChartModule, TreeModule, TabsModule, AccordionModule],
})
export class AgentsModule {}
