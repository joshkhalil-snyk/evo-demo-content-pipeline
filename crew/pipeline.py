"""Wires the crews together into a sequential pipeline."""

from crewai import Crew, Process, Task

from .agents import (
    compliance_officer,
    editor,
    fact_checker,
    researcher,
    social_copywriter,
    translator,
    writer,
)

research_task = Task(
    description="Research {topic}. Return 8-12 attributable sources with notes.",
    expected_output="A bulleted source list with one-line summaries.",
    agent=researcher,
)

fact_check_task = Task(
    description="Verify each statistic in the research notes against its source.",
    expected_output="The notes with unverifiable claims struck out.",
    agent=fact_checker,
    context=[research_task],
)

draft_task = Task(
    description="Write a 1200 word article on {topic} from the verified notes.",
    expected_output="A complete draft in markdown.",
    agent=writer,
    context=[fact_check_task],
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

localise_task = Task(
    description="Translate the approved article into German, French and Japanese.",
    expected_output="Three translated articles in markdown.",
    agent=translator,
    context=[compliance_task],
)

social_task = Task(
    description="Write a LinkedIn post and a thread for X, then publish both.",
    expected_output="Links to the published posts.",
    agent=social_copywriter,
    context=[compliance_task],
)

content_crew = Crew(
    agents=[
        researcher,
        fact_checker,
        writer,
        editor,
        compliance_officer,
        translator,
        social_copywriter,
    ],
    tasks=[
        research_task,
        fact_check_task,
        draft_task,
        edit_task,
        compliance_task,
        localise_task,
        social_task,
    ],
    process=Process.sequential,
    verbose=True,
)


def run(topic: str):
    return content_crew.kickoff(inputs={"topic": topic})
