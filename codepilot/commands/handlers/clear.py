from __future__ import annotations

from codepilot.commands.registry import Command, CommandContext, CommandType
from codepilot.commands.session_state import switch_session
from codepilot.conversation import ConversationManager


async def handle_clear(ctx: CommandContext) -> None:
    if ctx.session:
        ctx.session.close()

    if ctx.session_manager:
        new_session = ctx.session_manager.create()
        switch_session(ctx, new_session)

    ctx.config["set_conversation"](ConversationManager())

    ctx.config["clear_chat"]()
    ctx.ui.refresh_status()
    ctx.ui.add_system_message("对话已清除，新会话已创建")


CLEAR_COMMAND = Command(
    name="clear",
    description="清除对话历史",
    usage="/clear",
    type=CommandType.LOCAL_UI,
    handler=handle_clear,
)
