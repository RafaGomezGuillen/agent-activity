export interface Screenshot {
  id: string;
  agent_id: string;
  filename: string;
  uri: string;
  created_at: string;
}

export interface ScreenshotResponse {
  total: number;
  limit: number;
  offset: number;
  items: Screenshot[];
}

export interface ScreenshotFilters {
  agent_id?: string;
  start_time?: string;
  end_time?: string;
  limit?: number;
  offset?: number;
}
