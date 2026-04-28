import { Component } from '@angular/core';

@Component({
  selector: 'app-docs',
  templateUrl: './docs.html',
  standalone: false,
  styles: [],
})
export class DocsComponent {
  apiSections = [
    {
      name: 'Agents',
      endpoints: [
        { method: 'GET', path: '/agents/', desc: 'List agents (page, size, search, os, status)' },
        { method: 'GET', path: '/agents/:id', desc: 'Get agent by ID' },
        { method: 'POST', path: '/agents/register', desc: 'Register or update agent' },
      ],
    },
    {
      name: 'Keylogs',
      endpoints: [
        { method: 'GET', path: '/keylogs/', desc: 'List keylogs (agent_id, start_time, end_time, app, type, limit, offset)' },
        { method: 'POST', path: '/keylogs/:agent_id', desc: 'Ingest keylog events' },
      ],
    },
    {
      name: 'Clipboards',
      endpoints: [
        { method: 'GET', path: '/clipboards/', desc: 'List clipboards (agent_id, start_time, end_time, app, limit, offset)' },
        { method: 'POST', path: '/clipboards/:agent_id', desc: 'Ingest clipboard events' },
      ],
    },
    {
      name: 'Screenshots',
      endpoints: [
        { method: 'GET', path: '/screenshots/', desc: 'List screenshots (agent_id, start_time, end_time, limit, offset)' },
        { method: 'GET', path: '/screenshots/file/:id', desc: 'Retrieve screenshot file' },
        { method: 'POST', path: '/screenshots/:agent_id', desc: 'Upload screenshot' },
      ],
    },
    {
      name: 'Metrics',
      endpoints: [
        { method: 'GET', path: '/metrics/:agent_id', desc: 'Get metrics (start_time, end_time, limit, offset)' },
        { method: 'POST', path: '/metrics/:agent_id', desc: 'Ingest metrics snapshot' },
      ],
    },
    {
      name: 'Commands',
      endpoints: [
        { method: 'GET', path: '/commands/', desc: 'List commands (agent_id, status, page, size)' },
        { method: 'POST', path: '/commands/', desc: 'Create new command' },
        { method: 'PUT', path: '/commands/:id', desc: 'Update command result/status' },
      ],
    },
  ];

  commandDocs = [
    {
      name: 'filesystem.list_directory',
      desc: 'List contents of a directory on the remote agent.',
      example: `{"command": "filesystem.list_directory", "params": {"path": "/etc"}}`,
    },
    {
      name: 'filesystem.read_file',
      desc: 'Read the content of a text file on the remote agent.',
      example: `{"command": "filesystem.read_file", "params": {"path": "/etc/hosts"}}`,
    },
    {
      name: 'processes.list_processes',
      desc: 'List all running processes on the remote agent.',
      example: `{"command": "processes.list_processes", "params": {}}`,
    },
  ];
}
