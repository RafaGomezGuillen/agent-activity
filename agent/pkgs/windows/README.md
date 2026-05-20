# Windows Package

The Windows package turns the agent into a tray application. It keeps the agent accessible from the system tray while allowing a user to start, stop, or quit the background loop.

![Windows app](../../../assets/agent/windows-app.png)

## Build

Activate the agent virtual environment on Windows, then run:

```bat
cd agent\pkgs\windows
build_windows.bat
```

The script cleans previous Windows build output, runs PyInstaller with the Windows spec, and writes the artifact under `agent\dist\windows`. The shared PyInstaller configuration currently uses one-dir mode, so the expected output is an application folder rather than a single executable.

![Windows notification](../../../assets/agent/windows-notification.png)

## Runtime Behavior

When bundled, runtime files are written under:

```text
%APPDATA%\agent-activity
```

The tray menu exposes Start Agent, Stop Agent, and Quit Agent actions. A named Windows mutex, `Local\agent-activity-single-instance`, prevents multiple copies from running at the same time.

![Windows tray menu](../../../assets/agent/windows-tray-menu.png)

## Uninstall

Activate the agent virtual environment, then run:

```bat
cd agent\pkgs\windows
uninstall_windows.bat
```

The uninstall script kills `agent-activity.exe` if it is running, removes Windows build artifacts, and deletes `%APPDATA%\agent-activity`.

## Notes

Windows security tools may warn about bundled monitoring software, especially because the agent can observe keyboard, clipboard, screenshot, process, and filesystem activity. Test in a controlled environment and make sure the backend URL in `config/settings.py` is reachable before packaging.
