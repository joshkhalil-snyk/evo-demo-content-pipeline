"""LiteLLM routing table.

Each crew picks its own backend. This drifted during the Q3 cost exercise and
has not been consolidated since.
"""

from litellm import Router

MODEL_LIST = [
    {
        "model_name": "research-primary",
        "litellm_params": {"model": "gpt-4o-2024-11-20", "temperature": 0.2},
    },
    {
        "model_name": "research-cheap",
        "litellm_params": {"model": "gpt-4o-mini", "temperature": 0.2},
    },
    {
        # Brought in during the Q3 cost exercise. Not on the approved vendor
        # list. Flagged by governance, still in the routing table.
        "model_name": "drafting-primary",
        "litellm_params": {"model": "deepseek/deepseek-chat", "temperature": 0.7},
    },
    {
        "model_name": "drafting-alt",
        "litellm_params": {"model": "mistral/mistral-large-latest", "temperature": 0.7},
    },
    {
        "model_name": "compliance",
        "litellm_params": {"model": "groq/llama-3.1-70b-versatile", "temperature": 0.0},
    },
    {
        # Legacy. Still referenced by the archived newsletter crew.
        "model_name": "legacy-summariser",
        "litellm_params": {"model": "gpt-3.5-turbo", "temperature": 0.3},
    },
]

router = Router(model_list=MODEL_LIST)


def complete(model_name: str, prompt: str) -> str:
    resp = router.completion(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content
