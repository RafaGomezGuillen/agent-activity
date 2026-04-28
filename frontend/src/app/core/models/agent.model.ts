export interface Agent {
  id: string;
  hostname: string;
  ip_address: string;
  mac_address: string;
  os: string;
  os_release?: string;
  os_version?: string;
  architecture?: string;
  processor?: string;
  physical_cores: number;
  total_cores: number;
  max_frequency?: string;
  status: boolean;
  created_at: string;
  last_seen: string;
}

export interface AgentPagination {
  total: number;
  page: number;
  size: number;
  items: Agent[];
}

export interface AgentFilters {
  search?: string;
  os?: string;
  status?: boolean | null;
}
