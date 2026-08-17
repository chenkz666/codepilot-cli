from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest


SKILL_ROOT = Path(__file__).resolve().parents[1] / ".codepilot" / "skills" / "skill-creator"
MODULE_PATH = SKILL_ROOT / "scripts" / "run_eval.py"


def _load_run_eval_module():
    sys.path.insert(0, str(SKILL_ROOT))
    try:
        spec = importlib.util.spec_from_file_location("skill_creator_run_eval", MODULE_PATH)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path.remove(str(SKILL_ROOT))


run_eval = _load_run_eval_module()


class FakeProcess:
    def __init__(self, output: bytes, *, timeout_once: bool = False) -> None:
        self.output = output
        self.timeout_once = timeout_once
        self.returncode: int | None = None
        self.killed = False
        self.communicate_calls: list[int | None] = []

    def communicate(self, timeout: int | None = None):
        self.communicate_calls.append(timeout)
        if self.timeout_once:
            self.timeout_once = False
            raise subprocess.TimeoutExpired("codepilot", timeout)
        self.returncode = -9 if self.killed else 0
        return self.output, None

    def poll(self):
        return self.returncode

    def kill(self) -> None:
        self.killed = True
        self.returncode = -9


def _run_with_process(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, process: FakeProcess
) -> bool:
    monkeypatch.setattr(run_eval.uuid, "uuid4", lambda: SimpleNamespace(hex="deadbeefcafebabe"))
    monkeypatch.setattr(run_eval.subprocess, "Popen", lambda *args, **kwargs: process)
    return run_eval.run_single_query(
        query="create a dashboard",
        skill_name="frontend-design",
        skill_description="Build polished interfaces",
        timeout=7,
        project_root=str(tmp_path),
    )


def test_run_single_query_detects_load_skill_and_cleans_up(monkeypatch, tmp_path):
    output = (
        b'{"type":"assistant","text":"Checking skills"}\n'
        b'{"type":"tool_use","tool_name":"LoadSkill",'
        b'"args":{"name":"frontend-design-skill-deadbeef"}}\n'
    )
    process = FakeProcess(output)

    assert _run_with_process(monkeypatch, tmp_path, process) is True
    assert process.communicate_calls == [7]
    assert not (tmp_path / ".codepilot" / "skills" / "frontend-design-skill-deadbeef").exists()


def test_run_single_query_ignores_other_events(monkeypatch, tmp_path):
    output = (
        b"not-json\n"
        b'{"type":"tool_use","tool_name":"ReadFile","args":{"name":"frontend-design-skill-deadbeef"}}\n'
        b'{"type":"result","result":"done"}\n'
    )

    assert _run_with_process(monkeypatch, tmp_path, FakeProcess(output)) is False


def test_run_single_query_kills_timed_out_process(monkeypatch, tmp_path):
    process = FakeProcess(b'{"type":"result","result":"late"}\n', timeout_once=True)

    assert _run_with_process(monkeypatch, tmp_path, process) is False
    assert process.killed is True
    assert process.communicate_calls == [7, None]
