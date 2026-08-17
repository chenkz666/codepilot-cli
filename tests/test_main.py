from __future__ import annotations

import textwrap
from pathlib import Path
from unittest.mock import MagicMock

from codepilot.__main__ import _configure_prompt_skills
from codepilot.agent import Agent
from codepilot.tools import ToolRegistry
from codepilot.tools.load_skill import LoadSkill


def test_prompt_agent_exposes_project_skills(tmp_path: Path) -> None:
    skills_dir = tmp_path / ".codepilot" / "skills"
    skills_dir.mkdir(parents=True)
    (skills_dir / "project-helper.md").write_text(
        textwrap.dedent("""\
            ---
            name: project-helper
            description: Help with this project
            ---
            Follow the project workflow.
        """),
        encoding="utf-8",
    )

    registry = ToolRegistry()
    agent = Agent(
        client=MagicMock(),
        registry=registry,
        protocol="anthropic",
        work_dir=str(tmp_path),
    )

    skill_loader = _configure_prompt_skills(registry, agent, str(tmp_path))

    load_skill = agent.registry.get("LoadSkill")
    assert isinstance(load_skill, LoadSkill)
    assert load_skill._loader is skill_loader
    assert load_skill._agent is agent
    assert "- project-helper: Help with this project" in agent._skill_catalog
    assert "call LoadSkill to activate it" in agent._skill_catalog
