export interface Metric {
  id: string;
  agent_id: string;
  timestamp: string;
  cpu_usage: number;
  memory_used_percent: number;
  memory_total_gb: number;
  memory_available_gb: number;
  disk_used_percent: number;
  disk_total_gb: number;
  bytes_sent_total: number;
  bytes_recv_total: number;
  packets_sent_total: number;
  packets_recv_total: number;
  upload_speed_kb: number;
  download_speed_kb: number;
  uptime_hours: number;
  process_count: number;
  battery_percent?: number;
  battery_plugged?: string;
  current_app: string;
}

export interface MetricResponse {
  total: number;
  limit: number;
  offset: number;
  items: Metric[];
}

export interface MetricFilters {
  start_time?: string;
  end_time?: string;
  limit?: number;
  offset?: number;
}
