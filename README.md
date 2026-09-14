# Content Pipeline

Multi-agent pipeline that researches a topic, drafts marketing copy, and runs
a compliance pass before handing off to a human editor.

Model routing goes through LiteLLM so individual crews can pick their own
backend. Cost pressure last quarter pushed several crews onto cheaper or
self-hosted models.

## Crews
- **research** — gathers sources and summarises
- **drafting** — produces long-form copy
- **compliance** — checks claims against the approved messaging list
