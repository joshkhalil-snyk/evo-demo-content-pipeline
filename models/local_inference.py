"""Self-hosted inference for claim similarity and PII redaction.

Moved in-house so draft copy does not leave the VPC before the compliance pass.
"""

from sentence_transformers import SentenceTransformer
from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline

EMBEDDING_MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"
PII_MODEL_ID = "dslim/bert-base-NER"

_embedder = None
_redactor = None


def embedder() -> SentenceTransformer:
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(EMBEDDING_MODEL_ID)
    return _embedder


def redactor():
    global _redactor
    if _redactor is None:
        tokenizer = AutoTokenizer.from_pretrained(PII_MODEL_ID)
        model = AutoModelForTokenClassification.from_pretrained(PII_MODEL_ID)
        _redactor = pipeline("ner", model=model, tokenizer=tokenizer)
    return _redactor


def claim_similarity(claim: str, approved: list[str]) -> float:
    vectors = embedder().encode([claim] + approved)
    import numpy as np

    base, rest = vectors[0], vectors[1:]
    scores = rest @ base / (
        (np.linalg.norm(rest, axis=1) * np.linalg.norm(base)) + 1e-9
    )
    return float(scores.max())
