export interface Keylog {
  id: string;
  agent_id: string;
  timestamp: string;
  app?: string;
  type?: string;
  value?: string;
}

export interface KeylogResponse {
  total: number;
  limit: number;
  offset: number;
  data: Keylog[];
}

export interface KeylogFilters {
  agent_id?: string;
  start_time?: string;
  end_time?: string;
  app?: string;
  type?: string;
  limit?: number;
  offset?: number;
}
