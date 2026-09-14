"""CrewAI agent definitions for the content pipeline."""

from crewai import Agent

from .tools import CONTENT_TOOLS, COMPLIANCE_TOOLS

researcher = Agent(
    role="Research Analyst",
    goal="Gather credible sources on the assigned topic and summarise them",
    backstory=(
        "A meticulous analyst who prefers primary sources and flags anything "
        "that cannot be attributed."
    ),
    llm="gpt-4o-2024-11-20",
    tools=CONTENT_TOOLS,
    allow_delegation=False,
    verbose=True,
)

writer = Agent(
    role="Content Writer",
    goal="Turn research notes into publishable long-form copy",
    backstory="A copywriter who writes plainly and avoids marketing filler.",
    llm="deepseek/deepseek-chat",
    tools=CONTENT_TOOLS,
    allow_delegation=False,
    verbose=True,
)

editor = Agent(
    role="Editor",
    goal="Tighten the draft and enforce house style",
    backstory="A former newsroom editor with no patience for padding.",
    llm="mistral/mistral-large-latest",
    tools=CONTENT_TOOLS,
    allow_delegation=True,
    verbose=True,
)

compliance_officer = Agent(
    role="Compliance Reviewer",
    goal="Verify every claim maps to the approved messaging list",
    backstory="Cautious by training. Blocks anything unverifiable.",
    llm="groq/llama-3.1-70b-versatile",
    tools=COMPLIANCE_TOOLS,
    allow_delegation=False,
    verbose=True,
)

ALL_AGENTS = [researcher, writer, editor, compliance_officer]
