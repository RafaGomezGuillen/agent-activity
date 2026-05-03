export type CommandType =
  | 'filesystem.list_directory'
  | 'filesystem.read_file'
  | 'processes.list_processes';

export type CommandStatus = 'pending' | 'executed' | 'failed';

export interface Command {
  id: string;
  agent_id: string;
  command: CommandType;
  params?: Record<string, any>;
  status: CommandStatus;
  result?: Record<string, any> | null;
  created_at: string;
  executed_at?: string | null;
}

export interface CommandCreate {
  agent_id: string;
  command: CommandType;
  params?: Record<string, any>;
}

export interface CommandListResponse {
  total: number;
  limit: number;
  offset: number;
  items: Command[];
}

export interface DirectoryEntry {
  name: string;
  path: string;
  is_dir: boolean;
  size: number;
  modified: string;
}

export interface DirectoryResult {
  entries: DirectoryEntry[];
  error?: string;
}

export interface FileResult {
  path: string;
  size: number;
  content: string;
  error?: string;
}

export interface ProcessEntry {
  pid: number;
  name: string;
  status: string;
  cpu_percent?: number;
  memory_percent?: number;
}

export interface ProcessResult {
  processes: ProcessEntry[];
  error?: string;
}

export const AVAILABLE_COMMANDS: { label: string; value: CommandType; params: Record<string, string> }[] = [
  {
    label: 'List Directory',
    value: 'filesystem.list_directory',
    params: { path: '/' },
  },
  {
    label: 'Read File',
    value: 'filesystem.read_file',
    params: { path: '/etc/hosts' },
  },
  {
    label: 'List Processes',
    value: 'processes.list_processes',
    params: {},
  },
];
