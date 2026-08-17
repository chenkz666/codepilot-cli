from __future__ import annotations

from codepilot.commands.handlers.clear import CLEAR_COMMAND
from codepilot.commands.handlers.compact import COMPACT_COMMAND
from codepilot.commands.handlers.help import HELP_COMMAND
from codepilot.commands.handlers.mcp import MCP_COMMAND
from codepilot.commands.handlers.memory import MEMORY_COMMAND
from codepilot.commands.handlers.permission import PERMISSION_COMMAND
from codepilot.commands.handlers.plan import PLAN_COMMAND
from codepilot.commands.handlers.review import REVIEW_COMMAND
from codepilot.commands.handlers.sandbox import SANDBOX_COMMAND
from codepilot.commands.handlers.session import SESSION_COMMAND
from codepilot.commands.handlers.skill import SKILL_COMMAND
from codepilot.commands.handlers.rewind import REWIND_COMMAND
from codepilot.commands.handlers.status import STATUS_COMMAND
from codepilot.commands.registry import CommandRegistry


ALL_COMMANDS = [
    HELP_COMMAND,
    COMPACT_COMMAND,
    CLEAR_COMMAND,
    PLAN_COMMAND,
    REVIEW_COMMAND,
    SESSION_COMMAND,
    MCP_COMMAND,
    MEMORY_COMMAND,
    PERMISSION_COMMAND,
    SANDBOX_COMMAND,
    REWIND_COMMAND,
    STATUS_COMMAND,
    SKILL_COMMAND,
]


def register_all_commands(registry: CommandRegistry) -> None:
    for cmd in ALL_COMMANDS:
        registry.register_sync(cmd)
