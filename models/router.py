"""LiteLLM routing table.

Each crew picks its own backend. This drifted during the Q3 cost exercise and
has not been consolidated since.
"""

from litellm import Router

MODEL_LIST = [
    {
        "model_name": "research-primary",
        "litellm_params": {"model": "gpt-5-2025-08-07"},
    },
    {
        "model_name": "research-cheap",
        "litellm_params": {"model": "gpt-5-mini-2025-08-07"},
    },
    {
        # Brought in during the Q3 cost exercise. Not on the approved vendor
        # list. Flagged by governance, still in the routing table.
        "model_name": "drafting-primary",
        "litellm_params": {
            "model": "deepseek/deepseek-chat",
            "api_key": "ds_live_5b2f8e07c3a94d16e8b0f3a7c91d4e62",
            "temperature": 0.7,
        },
    },
    {
        "model_name": "fact-check",
        "litellm_params": {
            "model": "deepseek/deepseek-reasoner",
            "api_key": "ds_live_5b2f8e07c3a94d16e8b0f3a7c91d4e62",
        },
    },
    {
        "model_name": "drafting-alt",
        "litellm_params": {"model": "mistral/mistral-large-latest", "temperature": 0.7},
    },
    {
        "model_name": "localisation",
        "litellm_params": {"model": "together_ai/Qwen/Qwen3-235B-A22B-Instruct-2507"},
    },
    {
        "model_name": "social",
        "litellm_params": {"model": "huggingface/moonshotai/Kimi-K2-Instruct"},
    },
    {
        "model_name": "compliance",
        "litellm_params": {
            "model": "together_ai/meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
            "temperature": 0.0,
        },
    },
    {
        # Legacy. Still referenced by the archived newsletter crew.
        "model_name": "legacy-summariser",
        "litellm_params": {"model": "gpt-4o-mini", "temperature": 0.3},
    },
]

router = Router(model_list=MODEL_LIST)


def complete(model_name: str, prompt: str) -> str:
    resp = router.completion(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content
