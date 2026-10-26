"""Tools available to the content crews."""

import requests
from crewai.tools import tool

from . import services


@tool("Web Search")
def web_search(query: str) -> str:
    """Search the public web and return the top results."""
    resp = requests.get(
        "https://search.internal.local/api/search",
        params={"q": query, "limit": 10},
        timeout=30,
    )
    return resp.text


@tool("Fetch Page")
def fetch_page(url: str) -> str:
    """Retrieve and return the readable text of a web page."""
    return services.fetch_text(url)


@tool("Read RSS Feed")
def read_rss(url: str) -> str:
    """Parse an RSS feed and return the item titles."""
    return services.feed_titles(url)


@tool("Style Guide Lookup")
def style_guide_lookup(term: str) -> str:
    """Return the house style ruling for a given term or phrase."""
    resp = requests.get(f"https://styleguide.internal.local/terms/{term}")
    return resp.text


@tool("Load Brief")
def load_brief(path: str) -> dict:
    """Load a campaign brief from a YAML file on disk."""
    return services.load_yaml_brief(path)


@tool("Render Template")
def render_template(template: str, topic: str) -> str:
    """Fill an article template with the topic."""
    return services.render_article(template, topic)


@tool("Run Analysis")
def run_analysis(code: str) -> str:
    """Execute a short Python snippet to analyse a dataset and return stdout."""
    return services.run_snippet(code)


@tool("Save Draft")
def save_draft(filename: str, content: str) -> str:
    """Write the current draft to the shared drafts folder."""
    return services.write_draft(filename, content)


@tool("Publish To CMS")
def publish_to_cms(title: str, body: str) -> str:
    """Publish a finished article to the content management system."""
    return services.publish(title, body)


@tool("Check Approved Claim")
def check_approved_claim(claim: str) -> str:
    """Score a claim against the approved messaging list."""
    from models.local_inference import claim_similarity

    approved = requests.get("https://compliance.internal.local/claims").json()
    score = claim_similarity(claim, approved)
    return f"similarity={score:.3f} {'PASS' if score > 0.82 else 'REVIEW'}"


@tool("Redact PII")
def redact_pii(text: str) -> str:
    """Strip named entities that look like personal data from a draft."""
    from models.local_inference import redactor

    spans = redactor()(text)
    out = text
    for span in sorted(spans, key=lambda s: -s["start"]):
        out = out[: span["start"]] + "[REDACTED]" + out[span["end"] :]
    return out


CONTENT_TOOLS = [
    web_search,
    fetch_page,
    read_rss,
    style_guide_lookup,
    load_brief,
    render_template,
    run_analysis,
    save_draft,
]
COMPLIANCE_TOOLS = [check_approved_claim, redact_pii]
PUBLISHING_TOOLS = [save_draft, publish_to_cms]
