# Contributing

感谢你帮助改进 CodePilot。请让每个改动保持范围清晰、可验证，并避免把本地运行数据带入提交。

## 开发环境

```bash
uv sync --locked --dev
uv run ruff check codepilot tests
uv run pytest -q
```

## 提交要求

1. 为修复补充能够先复现问题的回归测试。
2. 保持 Python 3.11 和 3.12 兼容。
3. 不提交 `.codepilot/`、`.env`、日志、会话、构建产物或真实凭据。
4. 不通过关闭安全检查、吞掉异常或扩大权限范围来绕过问题。
5. Commit message 使用简洁英文，例如 `fix: keep worktree tool paths in sync`。

## Pull Request

PR 描述应说明问题、根因、改动边界、验证命令与潜在风险。涉及 UI 时请附终端截图；截图前先检查其中没有密钥、用户名、本地绝对路径或私有代码。

本项目采用 [MIT License](LICENSE)。公开贡献前请确认你拥有所提交代码的版权并同意以 MIT 协议授权。
