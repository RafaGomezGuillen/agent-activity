# Linux Package

This folder contains the Linux PyInstaller entry point and install scripts for the agent. The packaged Linux agent runs as a `systemd` service.

![Linu service](../../../assets/agent/linux-service.png)

## Files

- `main_linux.py`: daemon entry point with signal handling and single-instance locking.
- `build_linux.spec`: PyInstaller spec for Linux.
- `runtime_linux_paths.py`: redirects bundled app data to the user's Linux data directory.
- `build_linux.sh`: builds, installs, enables, and starts the service.
- `uninstall_linux.sh`: stops and removes the service, binary, lock file, and app data.

## Build And Install

Run from this folder or any shell that can execute the script:

```sh
cd agent/pkgs/linux
chmod +x build_linux.sh uninstall_linux.sh
./build_linux.sh
```

> [!IMPORTANT]
> Ensure the Python virtual environment is **active** before running `build_linux.sh`.

## Runtime Paths

When bundled by PyInstaller, `runtime_linux_paths.py` changes the process working directory to:

```text
~/.local/share/agent-activity
```

Runtime data is stored below that directory:

- `data/`
- `logs/`
- `data/agent_id.txt`

Service output is appended to:

```text
~/.local/share/agent-activity/logs/service.log
```

## Service Commands

```sh
systemctl status agent-activity
systemctl start agent-activity
systemctl stop agent-activity
systemctl restart agent-activity
systemctl disable agent-activity
```

## Uninstall

```sh
cd agent/pkgs/linux
./uninstall_linux.sh
```

> [!IMPORTANT]
> Ensure the Python virtual environment is **active** before running `uninstall_linux.sh`.

The uninstall script stops and disables the service, removes the installed binary, removes `/usr/local/lib/agent-activity` when present, removes `/tmp/agent-activity.lock`, and deletes the user's app data directory.
