# Content Pipeline

Multi-agent pipeline that researches a topic, fact-checks it, drafts marketing
copy, and runs a compliance pass before handing off to a human editor.

> **Intentionally vulnerable demo application.** Used to demonstrate Evo by
> Snyk. It contains deliberate code flaws, vulnerable dependencies and fake
> credentials. Do not deploy it or reuse any of its code.

Model routing goes through LiteLLM so individual crews can pick their own
backend. Cost pressure last quarter pushed several crews onto cheaper or
self-hosted models, and the marketing team has been trialling more.

## Crews
- **research** - gathers sources and summarises
- **fact_check** - verifies statistics against their sources
- **drafting** - produces long-form copy
- **editing** - enforces house style
- **compliance** - checks claims against the approved messaging list
- **localisation** - translates approved copy
- **social** - writes and publishes channel posts

## MCP
`api.py` is a small Flask preview service for editors.
`mcp_server/server.py` exposes the compliance tooling over SSE. `.mcp.json`
lists the third-party servers the crews are allowed to use.
