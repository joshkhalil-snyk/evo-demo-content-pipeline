"""CrewAI agent definitions for the content pipeline."""

from crewai import Agent

from .tools import COMPLIANCE_TOOLS, CONTENT_TOOLS, PUBLISHING_TOOLS

researcher = Agent(
    role="Research Analyst",
    goal="Gather credible sources on the assigned topic and summarise them",
    backstory=(
        "A meticulous analyst who prefers primary sources and flags anything "
        "that cannot be attributed."
    ),
    llm="gpt-5-2025-08-07",
    tools=CONTENT_TOOLS,
    allow_delegation=False,
    verbose=True,
)

fact_checker = Agent(
    role="Fact Checker",
    goal="Verify every statistic and quotation in the research notes",
    backstory="Distrusts round numbers and anything without a link.",
    llm="deepseek/deepseek-reasoner",
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

translator = Agent(
    role="Translator",
    goal="Localise approved copy for the EMEA and APAC sites",
    backstory="Native-level in six languages, careful with idiom.",
    llm="together_ai/Qwen/Qwen3-235B-A22B-Instruct-2507",
    tools=CONTENT_TOOLS,
    allow_delegation=False,
    verbose=True,
)

social_copywriter = Agent(
    role="Social Copywriter",
    goal="Cut the article down to posts for each social channel",
    backstory="Writes in short lines and knows what each platform rewards.",
    llm="huggingface/moonshotai/Kimi-K2-Instruct",
    tools=PUBLISHING_TOOLS,
    allow_delegation=False,
    verbose=True,
)

compliance_officer = Agent(
    role="Compliance Reviewer",
    goal="Verify every claim maps to the approved messaging list",
    backstory="Cautious by training. Blocks anything unverifiable.",
    llm="together_ai/meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
    tools=COMPLIANCE_TOOLS,
    allow_delegation=False,
    verbose=True,
)

ALL_AGENTS = [
    researcher,
    fact_checker,
    writer,
    editor,
    translator,
    social_copywriter,
    compliance_officer,
]
