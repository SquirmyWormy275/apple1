"""Console syntax, plain-language help and presentation; no hardware access."""

from __future__ import annotations

import json
import shlex
import textwrap
from difflib import get_close_matches
from typing import Any

from .core import Neural1Error

COMMAND_HELP = {
    '1': '1: Select 4K MIND. Explore programs within a 4 KiB memory budget.',
    '2': '2: Select 1976 MULTIVERSE. Check partial CPU/RAM designs against reviewed historical sources.',
    '3': '3: Select SELFHOST/1. Begin with raw machine code; later construction stages need separate evidence.',
    '4': '4: Select 256-BYTE UNIVERSE. Test deposited 256-byte candidates against an output/return task.',
    '5': '5: Select RAM REPUBLIC. Observe participants interacting through shared memory.',
    'MODELS': 'MODELS: List the available model records.',
    'MODEL': 'MODEL model-id: Verify and select a local model. Example: MODEL qwen-coder',
    'START': 'START: Launch one bounded run of the selected experiment and model. Takes no arguments. Use STATUS to follow it.',
    'STATUS': 'STATUS: Show the selected model, worker state, runs and resource readings.',
    'RUNS': 'RUNS: List recorded runs and their state. Completion alone does not establish scientific success.',
    'SHOW': 'SHOW run-id: Read the family evaluation and checkpoint. Copy a run ID from RUNS.',
    'TRANSCRIPT': 'TRANSCRIPT run-id [page]: Show model/Monitor exchanges. Without a page, show the latest 12 per cell; page 0 starts at the beginning.',
    'STOP': 'STOP run-id: Request cancellation of that run. Its saved state is retained.',
    'RESUME': 'RESUME run-id: Continue a saved run using its recorded model registry.',
    'EXPORT': 'EXPORT run-id: Create a verified evidence bundle on the configured SSD.',
    'OPEN': 'OPEN bundle-path: Verify and inspect an exported bundle on the configured SSD. Quote paths containing spaces.',
    'META': 'META [LIST|QUEUE] or META CLAIM|HISTORY claim-id: Browse recorded claims, evidence and review work.',
    'SELFHOST': 'SELFHOST [LIST] or SELFHOST INGEST run-id | REBUILD artifact-id | QUALIFY evidence-path | EXPORT artifact-id | OPEN bundle-path: Inspect or work with the persistent virtual construction archive.',
    'LESSONS': 'LESSONS: List the available Field Library lesson folders.',
    'SOURCE': 'SOURCE lesson: Read a lesson and its sources without calling a model. Example: SOURCE S01. The older SOURCE lesson sources form also works.',
    'ASK': 'ASK lesson question: Ask a source-grounded question. Example: ASK S01 What is an Apple-1?',
    'HINT': 'HINT lesson question: Ask for a hint grounded in the lesson.',
    'EXPLAIN': 'EXPLAIN lesson question: Ask for an explanation grounded in the lesson.',
    'CHECK': 'CHECK lesson question: Check your work using the lesson and its answer material.',
    'TRACE': 'TRACE lesson "assembly with \\n separators": Execute assembly in the virtual harness, then request an explanation.',
    'HELP': 'HELP [command]: Show the command list or help for one command. Example: HELP START',
    'QUIT': 'QUIT: Close the console. Active runs continue in their user service; STOP run-id requests cancellation.',
}

ALIASES = {'?': 'HELP', 'EXIT': 'QUIT', '0': 'QUIT'}


def command_help(topic: str) -> str:
    name = ALIASES.get(topic.upper(), topic.upper())
    if name not in COMMAND_HELP:
        matches = get_close_matches(name, COMMAND_HELP, n=1, cutoff=0.6)
        suggestion = f' Did you mean {matches[0]}?' if matches else ''
        raise Neural1Error(f'Unknown command {topic!r}.{suggestion} Type HELP to list commands.')
    return COMMAND_HELP[name]


def parse_command(line: str) -> list[str]:
    try:
        args = shlex.split(line)
    except ValueError as error:
        message = 'Unclosed quotation mark. Close the quote and try again.' if str(error) == 'No closing quotation' else 'Incomplete escape. Remove the trailing backslash or quote it literally.'
        raise Neural1Error(message) from error
    if not args:
        return []
    op = ALIASES.get(args[0].upper(), args[0].upper())
    args[0] = op
    usage = command_help(op)
    count = len(args) - 1
    if op in {'MODEL', 'STOP', 'RESUME', 'SHOW', 'EXPORT', 'OPEN'}:
        valid = count == 1
    elif op in {'ASK', 'HINT', 'EXPLAIN', 'CHECK', 'TRACE'}:
        valid = count >= 2 and all(arg.strip() for arg in args[1:])
    elif op == 'SOURCE':
        valid = count == 1 or (count == 2 and args[2].lower() == 'sources')
    elif op == 'TRANSCRIPT':
        valid = count in (1, 2)
    elif op == 'HELP':
        valid = count <= 1
    elif op == 'META':
        valid = (
            count == 0
            or (count == 1 and args[1].upper() in {'LIST', 'QUEUE'})
            or (count == 2 and args[1].upper() in {'CLAIM', 'HISTORY'})
        )
    elif op == 'SELFHOST':
        valid = (
            count == 0
            or (count == 1 and args[1].upper() == 'LIST')
            or (count == 2 and args[1].upper() in {'INGEST', 'REBUILD', 'QUALIFY', 'EXPORT', 'OPEN'})
        )
    else:
        valid = count == 0
    if not valid or any(not arg.strip() for arg in args[1:]):
        raise Neural1Error(f'Usage: {usage}')
    return args


def friendly_error(error: Exception) -> str:
    if isinstance(error, FileNotFoundError):
        return f'File or directory not found: {error.filename}. Check the path and try again.'
    if isinstance(error, PermissionError):
        return f'Permission denied: {error.filename}. Check that your account can access this path.'
    if isinstance(error, json.JSONDecodeError):
        return f'Invalid JSON at line {error.lineno}, column {error.colno}: {error.msg}. Check the input file.'
    return str(error)


def visible_text(text: str) -> str:
    """Show control bytes in recorded output without sending terminal escapes."""
    characters = []
    for char in text:
        if char == '\r':
            characters.append('\\r')
        elif char == '\t':
            characters.append('\\t')
        elif (ord(char) < 32 and char != '\n') or 127 <= ord(char) <= 159:
            characters.append(f'\\x{ord(char):02x}')
        else:
            characters.append(char)
    return ''.join(characters)


def format_text(text: str, width: int) -> str:
    """Wrap prose while keeping paths, IDs and hashes intact for copying."""
    return '\n'.join(
        textwrap.fill(line, width=width, break_long_words=False, break_on_hyphens=False, replace_whitespace=False) if line else ''
        for line in visible_text(text).splitlines()
    )


def render_result(value: Any, *, width: int = 88) -> str:
    """Present every returned field without interpreting research outcomes."""
    lines: list[str] = []

    def label(key: Any) -> str:
        text = str(key)
        if text.replace('_', '').isalpha() and text.islower():
            return text.replace('_', ' ').capitalize()
        return text

    def scalar(item: Any) -> str:
        if item is None:
            return 'null'
        if isinstance(item, bool):
            return 'Yes' if item else 'No'
        return str(item)

    def append(text: str, indent: int) -> None:
        prefix = ' ' * indent
        for line in visible_text(text).splitlines() or ['']:
            lines.append(textwrap.fill(prefix + line, width=width, subsequent_indent=prefix, break_long_words=False, break_on_hyphens=False, replace_whitespace=False))

    def visit(item: Any, indent: int = 0) -> None:
        if isinstance(item, dict):
            if not item:
                append('(empty)', indent)
            for key, child in item.items():
                if isinstance(child, (dict, list, tuple)):
                    append(label(key) + ':', indent)
                    visit(child, indent + 2)
                else:
                    append(f'{label(key)}: {scalar(child)}', indent)
        elif isinstance(item, (list, tuple)):
            if not item:
                append('(none)', indent)
            for index, child in enumerate(item, 1):
                if isinstance(child, (dict, list, tuple)):
                    append(f'{index}.', indent)
                    visit(child, indent + 2)
                else:
                    append(f'- {scalar(child)}', indent)
        else:
            append(scalar(item), indent)

    if value is None:
        return ''
    visit(value)
    return '\n'.join(lines)
