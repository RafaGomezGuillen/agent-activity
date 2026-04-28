export interface Clipboard {
  id: string;
  agent_id: string;
  timestamp: string;
  app?: string;
  value?: string;
}

export interface ClipboardResponse {
  total: number;
  limit: number;
  offset: number;
  data: Clipboard[];
}

export interface ClipboardFilters {
  agent_id?: string;
  start_time?: string;
  end_time?: string;
  app?: string;
  limit?: number;
  offset?: number;
}
