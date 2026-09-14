"""Wires the crews together into a sequential pipeline."""

from crewai import Crew, Process, Task

from .agents import compliance_officer, editor, researcher, writer

research_task = Task(
    description="Research {topic}. Return 8-12 attributable sources with notes.",
    expected_output="A bulleted source list with one-line summaries.",
    agent=researcher,
)

draft_task = Task(
    description="Write a 1200 word article on {topic} from the research notes.",
    expected_output="A complete draft in markdown.",
    agent=writer,
    context=[research_task],
)

edit_task = Task(
    description="Tighten the draft. Cut filler. Enforce house style.",
    expected_output="A revised draft.",
    agent=editor,
    context=[draft_task],
)

compliance_task = Task(
    description="Check every factual claim against the approved list.",
    expected_output="PASS or REVIEW with a per-claim breakdown.",
    agent=compliance_officer,
    context=[edit_task],
)

content_crew = Crew(
    agents=[researcher, writer, editor, compliance_officer],
    tasks=[research_task, draft_task, edit_task, compliance_task],
    process=Process.sequential,
    verbose=True,
)


def run(topic: str):
    return content_crew.kickoff(inputs={"topic": topic})
