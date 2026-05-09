import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpResponse } from '@angular/common/http';
import { finalize } from 'rxjs';
import { ClipboardService } from '../../../core/services/clipboard.service';
import { AgentService } from '../../../core/services/agent.service';
import { Clipboard, ClipboardFilters } from '../../../core/models/clipboard.model';
import { Agent } from '../../../core/models/agent.model';

@Component({
  selector: 'app-agent-clipboards',
  templateUrl: './agent-clipboards.html',
  standalone: false,
  styles: [],
})
export class AgentClipboardsComponent implements OnInit {
  agentId = '';
  agent: Agent | null = null;
  clipboards: Clipboard[] = [];
  total = 0;
  loading = true;
  downloading = false;

  limit = 50;
  offset = 0;
  appFilter = '';
  dateRange: Date[] | null = null;
  selectedClipboard: Clipboard | null = null;
  dialogVisible = false;

  constructor(
    private route: ActivatedRoute,
    private clipboardService: ClipboardService,
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
    const filters: ClipboardFilters = {
      agent_id: this.agentId,
      app: this.appFilter || undefined,
      limit: this.limit,
      offset: this.offset,
    };
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
    this.dateRange = null;
    this.applyFilters();
  }

  openDialog(c: Clipboard): void {
    this.selectedClipboard = c;
    this.dialogVisible = true;
  }

  closeDialog(): void {
    this.selectedClipboard = null;
    this.dialogVisible = false;
  }

  download(): void {
    if (!this.agentId || this.downloading) return;

    this.downloading = true;
    this.clipboardService
      .downloadClipboards(this.agentId)
      .pipe(
        finalize(() => {
          this.downloading = false;
          this.cdr.detectChanges();
        })
      )
      .subscribe({
        next: (response) => {
          this.saveBlobResponse(response, `${this.agentId}_clipboards.jsonl`);
        },
        error: () => {
          console.error('Failed to download clipboards');
        },
      });
  }

  private saveBlobResponse(response: HttpResponse<Blob>, fallbackFileName: string): void {
    if (!response.body) return;

    const contentDisposition = response.headers.get('content-disposition');
    const fileName = this.extractFileName(contentDisposition) ?? fallbackFileName;
    const objectUrl = URL.createObjectURL(response.body);
    const link = document.createElement('a');
    link.href = objectUrl;
    link.download = fileName;
    link.click();
    URL.revokeObjectURL(objectUrl);
  }

  private extractFileName(contentDisposition: string | null): string | null {
    if (!contentDisposition) return null;

    const utf8Match = contentDisposition.match(/filename\*=UTF-8''([^;]+)/i);
    if (utf8Match?.[1]) {
      return decodeURIComponent(utf8Match[1]);
    }

    const plainMatch = contentDisposition.match(/filename="?([^";]+)"?/i);
    return plainMatch?.[1] ?? null;
  }
}
