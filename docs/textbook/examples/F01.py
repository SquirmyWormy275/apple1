from neural1.console_ui import command_help, parse_command
from neural1.core import Neural1Error

for command in ("START", "START extra", "META CLAIM", "STATR", "HELP START"):
    try:
        print(command, "->", parse_command(command))
    except Neural1Error as error:
        print(command, "-> REJECTED:", error)
assert parse_command("HELP START") == ["HELP", "START"]
print(command_help("START"))
