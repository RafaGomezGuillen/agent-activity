# Agent Activity

Agent Activity is a monitoring platform for registered desktop machines. It combines a Python endpoint agent, a FastAPI backend, and an Angular dashboard so system activity can be collected, organized, and reviewed from one place.

At a high level, each enrolled machine identifies itself to the backend, keeps sending health data, and checks whether there is any pending work to execute. The dashboard turns that stream of information into an operator console: online status, host details, system metrics, screenshots, activity logs, and command results are all available through a single interface.

> [!CAUTION]
> Agent Activity can collect sensitive information, including keyboard events, clipboard contents, screenshots, process data, and selected file contents. Use it only on machines where monitoring is authorized, disclosed, and appropriate. SO BE CAREFUL, THE AGENT COULD BE USE AS A MALWARE!

![Overview](assets/common/overview.gif)

### Real-time Agent Monitoring

Agents register with machine details such as hostname, operating system, IP address, MAC address, CPU information, and core count. Each agent sends regular heartbeat metrics, allowing the backend to keep track of which machines are online and which have gone quiet.

![Agent list](/assets/common/agent-list.png)

The dashboard uses that information to present a live fleet view. Operators can search agents, filter by operating system or status, open an individual agent, and quickly understand when it was last seen.

![Agent details](/assets/common/agent-details.png)

### Keyboard Capture (Keylogs)

On supported desktop platforms, the agent can collect keyboard activity and group typed input into structured events. Those events are buffered locally, written as JSON Lines, and periodically sent to the backend for review.

![Keyboard](/assets/common/keylogs.png)

The backend stores keylog events with timestamps, application context, event type, and value. From the dashboard, operators can inspect keylog history, filter it, and download it when needed.

![Keyboard overview](/assets/common/keylogs.gif)

### Clipboard Interception

The agent can monitor clipboard changes and capture text content that passes configured length checks. Like keylogs, clipboard events are buffered, persisted locally, and sent to the backend in batches.

![Clipboard](/assets/common/clipboards.png)

This makes it possible to review copied text alongside the application that was active when the clipboard changed. Because clipboard data is often highly sensitive, this feature should be enabled and used with particular care.

![Clipboard overview](/assets/common/clipboards.gif)

### Screenshot Capture

The screenshot service captures the desktop at a configured interval, compresses the image, stores it locally, and uploads it to the backend. The agent also removes old local screenshots once the configured maximum count is reached.

![Screenshots](/assets/common/screenshots.png)

The backend stores screenshot metadata and serves the image files to the dashboard. Operators can browse screenshots per agent, open individual captures, delete old captures, or download all screenshots for an agent as a ZIP archive.

![Screenshot details](/assets/common/screenshot-detail.png)

### System Metrics Collection

Every heartbeat includes system information such as CPU usage, memory usage, disk usage, network counters, upload and download speed estimates, uptime, process count, battery state, and current active application.

These metrics are stored as time-series records and shown in the dashboard so an operator can see how a machine is behaving over time, not only whether it is online.

![Agent metrics](/assets/common/agent-metrics.png)

### Remote Command Execution

![Commands overview](/assets/common/commands.gif)

The backend can queue commands for an online agent. The agent polls for pending commands, runs the matching handler, and reports the result back with a final status.

Currently supported commands are intentionally small and inspect-oriented: `filesystem.list_directory`, `filesystem.read_file`, and `processes.list_processes`. This keeps the command channel useful while limiting the command surface.

### filesystem.list_directory example

![List directory](/assets/common/list-directory.png)

### filesystem.read_file example

![Read file](/assets/common/read-file.png)

### processes.list_processes example

![List processes](/assets/common/list-processes.png)

## Getting Started

Start the backend first:

```sh
cd backend
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
alembic upgrade head
python -m app.main
```

Then start the dashboard:

```sh
cd frontend
npm install
npm start
```

Finally, start an agent from a machine that can reach the backend:

```sh
cd agent
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

On Windows, activate Python virtual environments with `venv\Scripts\activate`.

## Packaging The Agent

The agent can be packaged with PyInstaller for each supported operating system. Linux packaging installs a `systemd` service, macOS packaging creates a menu bar app and DMG, and Windows packaging creates a tray application.

- [Linux agent package](agent/pkgs/linux/README.md)
- [macOS agent package](agent/pkgs/mac/README.md)
- [Windows agent package](agent/pkgs/windows/README.md)

## More Documentation

- [Frontend guide](frontend/README.md)
- [Backend guide](backend/README.md)
- [Agent guide](agent/README.md)
