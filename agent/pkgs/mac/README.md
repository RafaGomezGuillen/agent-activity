# macOS Package

This folder contains the macOS PyInstaller entry point and package scripts for the agent. The packaged macOS agent runs as a menu bar app with Start, Stop, and Force Quit controls.

![macOS app](../../../assets/agent/macos-app.png)

## Files

- `main_mac.py`: `rumps` menu bar app entry point.
- `build_mac.spec`: PyInstaller spec that creates an `.app` bundle.
- `runtime_mac_paths.py`: redirects bundled app data to Application Support.
- `build_mac.sh`: builds the `.app` bundle and wraps it in a DMG.
- `uninstall_mac.sh`: removes the app bundle and Application Support data.

## Build

Run on macOS from this folder:

```sh
cd agent/pkgs/mac
chmod +x build_mac.sh uninstall_mac.sh
./build_mac.sh
```

> [!IMPORTANT]
> Ensure the Python virtual environment is **active** before running `build_mac.sh`.

![DMG app](../../../assets/agent/dmg-app.png)

## Runtime Paths

When bundled by PyInstaller, `runtime_mac_paths.py` changes the process working directory to:

```text
~/Library/Application Support/agent-activity
```

Runtime data is stored below that directory:

- `data/`
- `logs/`
- `data/agent_id.txt`
- `data/keylog.jsonl`
- `data/clipboard.jsonl`
- `data/screenshots/`

## Menu Bar Behavior

The app exposes:

- `Start Agent`: starts the agent loop in a background thread.
- `Stop Agent`: signals the loop to stop.
- `Force Quit`: stops the loop and exits the menu bar app.

The entry point checks for another running app instance using the bundle identifier from the current app bundle.

![macOS menu bar](../../../assets/agent/menu-bar.png)

## Permissions

macOS may require explicit privacy permissions depending on which services are used:

- Accessibility/Input Monitoring for keyboard capture.
- Screen Recording for screenshots.
- Automation permissions may be requested when active application detection calls AppleScript.

These permissions are controlled by macOS System Settings and may need to be granted after first launch.

![macOS menu bar](../../../assets/agent/mac-notification.png)

## Uninstall

```sh
cd agent/pkgs/mac
./uninstall_mac.sh
```

The uninstall script kills running app processes, removes `/Applications/agent-activity.app` if present, and deletes:

```text
~/Library/Application Support/agent-activity
```

> [!IMPORTANT]
> Ensure the Python virtual environment is **active** before running `uninstall_mac.sh`.
