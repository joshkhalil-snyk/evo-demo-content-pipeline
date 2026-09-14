"""MCP server exposing the content pipeline's compliance tooling.

Other internal agents connect to this to reuse the approved-claims check
rather than reimplementing it.
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("content-compliance")


@mcp.tool()
def check_claim(claim: str) -> str:
    """Score a marketing claim against the approved messaging list."""
    from models.local_inference import claim_similarity
    import requests

    approved = requests.get("https://compliance.internal.local/claims").json()
    score = claim_similarity(claim, approved)
    return f"similarity={score:.3f} {'PASS' if score > 0.82 else 'REVIEW'}"


@mcp.tool()
def redact(text: str) -> str:
    """Remove probable personal data from a block of draft copy."""
    from models.local_inference import redactor

    spans = redactor()(text)
    out = text
    for span in sorted(spans, key=lambda s: -s["start"]):
        out = out[: span["start"]] + "[REDACTED]" + out[span["end"] :]
    return out


@mcp.resource("styleguide://{term}")
def style_rule(term: str) -> str:
    """Return the house style ruling for a term."""
    import requests

    return requests.get(f"https://styleguide.internal.local/terms/{term}").text


if __name__ == "__main__":
    mcp.run(transport="stdio")
