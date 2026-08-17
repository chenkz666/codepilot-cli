from __future__ import annotations

import pytest

from codepilot.app import CodePilotApp
from codepilot.config import ProviderConfig, SandboxAppConfig, WorktreeConfig


@pytest.mark.asyncio
async def test_tui_clear_creates_and_binds_a_fresh_session(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    provider = ProviderConfig(
        name="smoke",
        protocol="openai-compat",
        base_url="http://127.0.0.1:9/v1",
        model="smoke-model",
        api_key="test-key",
    )
    app = CodePilotApp(
        providers=[provider],
        mcp_servers=[],
        worktree_config=WorktreeConfig(),
        sandbox_config=SandboxAppConfig(),
    )

    async with app.run_test(size=(120, 45)) as pilot:
        await pilot.pause()
        assert app.session is not None
        assert app.agent is not None
        old_session_id = app.session.session_id
        app.agent.total_input_tokens = 100
        app.agent.active_skills["old"] = "old state"

        await app._dispatch_command("/clear")

        assert app.session.session_id != old_session_id
        assert app.agent.session_id == app.session.session_id
        assert app.agent.total_input_tokens == 0
        assert app.agent.active_skills == {}
        assert app.agent.file_history._session_dir.name == app.session.session_id
        app.exit()
