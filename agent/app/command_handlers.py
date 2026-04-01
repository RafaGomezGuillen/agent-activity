from logger import logger
from actions.filesystem import list_directory, read_file
from actions.processes import list_processes


def _handle_list_directory(params):
    path = params.get("path", ".")
    return list_directory(path)


def _handle_read_file(params):
    path = params.get("path")
    if not path:
        return {"error": "Path parameter required"}
    return read_file(path)


def _handle_list_processes(params):
    # Params currently not used;
    processes = list_processes()
    return {"processes": processes}


COMMAND_HANDLERS = {
    "filesystem.list_directory": _handle_list_directory,
    "filesystem.read_file": _handle_read_file,
    "processes.list_processes": _handle_list_processes,
}


def execute_command(command):
    try:
        cmd = command.get("command")
        params = command.get("params", {})

        handler = COMMAND_HANDLERS.get(cmd)
        if handler is None:
            return "failed", {"error": f"Unknown command: {cmd}"}

        result = handler(params)
        return "executed", result

    except Exception as e:
        logger.error(f"Command execution error: {e}")
        return "failed", {"error": str(e)}
