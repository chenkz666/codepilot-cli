from __future__ import annotations

from typing import Protocol

from codepilot.commands.registry import CommandContext


class SessionHandle(Protocol):
    session_id: str


def switch_session(ctx: CommandContext, session: SessionHandle) -> None:
    """切换会话，并统一重置所有会话级 Agent 状态。"""
    setter = ctx.config.get("set_session")
    if setter is None:
        raise RuntimeError("当前运行模式未提供会话切换支持")
    setter(session)

    if ctx.agent is not None:
        ctx.agent.session_id = session.session_id
        ctx.agent.reset_session_state()
