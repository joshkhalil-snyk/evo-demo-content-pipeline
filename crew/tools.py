"""Tools available to the content crews."""

import requests
from crewai.tools import tool


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
    resp = requests.get(url, timeout=30)
    return resp.text[:20000]


@tool("Style Guide Lookup")
def style_guide_lookup(term: str) -> str:
    """Return the house style ruling for a given term or phrase."""
    resp = requests.get(f"https://styleguide.internal.local/terms/{term}")
    return resp.text


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


CONTENT_TOOLS = [web_search, fetch_page, style_guide_lookup]
COMPLIANCE_TOOLS = [check_approved_claim, redact_pii]
