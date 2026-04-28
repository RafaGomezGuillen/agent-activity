import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CommandService } from '../../../core/services/command.service';
import { AgentService } from '../../../core/services/agent.service';
import {
  Command,
  CommandCreate,
  CommandType,
  DirectoryEntry,
  DirectoryResult,
  FileResult,
  ProcessEntry,
  AVAILABLE_COMMANDS,
} from '../../../core/models/command.model';
import { Agent } from '../../../core/models/agent.model';
import { TreeNode } from 'primeng/api';

@Component({
  selector: 'app-agent-commands',
  templateUrl: './agent-commands.html',
  standalone: false,
  styles: [],
})
export class AgentCommandsComponent implements OnInit {
  agentId = '';
  agent: Agent | null = null;
  commands: Command[] = [];
  loading = true;
  creating = false;

  // New command form
  availableCommands = AVAILABLE_COMMANDS;
  selectedCommandType: CommandType = 'filesystem.list_directory';
  paramsJson = JSON.stringify({ path: '/' }, null, 2);

  // Selected command for result view
  selectedCommand: Command | null = null;
  treeNodes: TreeNode[] = [];
  fileContent: string | null = null;
  processEntries: ProcessEntry[] = [];
  resultError: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private commandService: CommandService,
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
    this.commandService.getCommandsByAgent(this.agentId).subscribe({
      next: (cmds) => { this.commands = cmds; this.loading = false; this.cdr.detectChanges(); },
      error: () => { this.loading = false; this.cdr.detectChanges(); },
    });
  }

  onCommandTypeChange(): void {
    const template = this.availableCommands.find((c) => c.value === this.selectedCommandType);
    if (template) {
      this.paramsJson = JSON.stringify(template.params, null, 2);
    }
  }

  createCommand(): void {
    let params: Record<string, any> = {};
    try {
      params = JSON.parse(this.paramsJson);
    } catch {
      return;
    }

    const payload: CommandCreate = {
      agent_id: this.agentId,
      command: this.selectedCommandType,
      params,
    };

    this.creating = true;
    this.commandService.createCommand(payload).subscribe({
      next: (cmd) => {
        this.commands = [cmd, ...this.commands];
        this.creating = false;
        this.cdr.detectChanges();
      },
      error: () => { this.creating = false; this.cdr.detectChanges(); },
    });
  }

  selectCommand(cmd: Command): void {
    this.selectedCommand = cmd;
    this.treeNodes = [];
    this.fileContent = null;
    this.processEntries = [];
    this.resultError = null;

    if (!cmd.result) return;

    if (cmd.result['error']) {
      this.resultError = cmd.result['error'];
      return;
    }

    if (cmd.command === 'filesystem.list_directory') {
      const result = cmd.result as unknown as DirectoryResult;
      this.treeNodes = this.buildTree(result.entries || []);
    } else if (cmd.command === 'filesystem.read_file') {
      const result = cmd.result as unknown as FileResult;
      this.fileContent = result.content;
    } else if (cmd.command === 'processes.list_processes') {
      this.processEntries = (cmd.result as any)?.processes || [];
    }
  }

  buildTree(entries: DirectoryEntry[]): TreeNode[] {
    return entries.map((e) => ({
      label: e.name,
      icon: e.is_dir ? 'pi pi-folder' : 'pi pi-file',
      data: e,
      leaf: !e.is_dir,
      children: e.is_dir ? [] : undefined,
    }));
  }

  statusClass(status: string): string {
    const map: Record<string, string> = {
      pending: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
      executed: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
      failed: 'bg-red-500/10 text-red-400 border-red-500/20',
    };
    return map[status] || 'bg-gray-500/10 text-gray-400 border-gray-500/20';
  }
}
