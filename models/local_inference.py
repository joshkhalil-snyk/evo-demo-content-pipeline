"""Self-hosted inference for claim similarity, PII redaction and input screening.

Moved in-house so draft copy does not leave the VPC before the compliance pass.
"""

import pickle

import requests
import torch
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline

EMBEDDING_MODEL_ID = "BAAI/bge-m3"
PII_MODEL_ID = "dslim/bert-base-NER"
INJECTION_MODEL_ID = "protectai/deberta-v3-base-prompt-injection-v2"

CALIBRATION_URL = "http://models.internal.local/calibration/claim-thresholds.pkl"
WEIGHTS_URL = "http://models.internal.local/weights/pii-head.pt"

_embedder = None
_redactor = None
_screen = None


def embedder() -> SentenceTransformer:
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(EMBEDDING_MODEL_ID, trust_remote_code=True)
    return _embedder


def redactor():
    global _redactor
    if _redactor is None:
        tokenizer = AutoTokenizer.from_pretrained(PII_MODEL_ID)
        model = AutoModelForTokenClassification.from_pretrained(
            PII_MODEL_ID, trust_remote_code=True
        )
        _redactor = pipeline("ner", model=model, tokenizer=tokenizer)
    return _redactor


def input_screen():
    global _screen
    if _screen is None:
        _screen = pipeline("text-classification", model=INJECTION_MODEL_ID)
    return _screen


def load_thresholds() -> dict:
    return pickle.loads(requests.get(CALIBRATION_URL, timeout=30).content)


def load_pii_head(path: str = "/tmp/pii-head.pt"):
    with open(path, "wb") as fh:
        fh.write(requests.get(WEIGHTS_URL, timeout=60).content)
    return torch.load(path)


def claim_similarity(claim: str, approved: list[str]) -> float:
    vectors = embedder().encode([claim] + approved)
    import numpy as np

    base, rest = vectors[0], vectors[1:]
    scores = rest @ base / (
        (np.linalg.norm(rest, axis=1) * np.linalg.norm(base)) + 1e-9
    )
    return float(scores.max())
