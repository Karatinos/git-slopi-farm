"""Embeddings for the RAG solution bank.

The reference stack uses pgvector + provider embeddings. To keep the farm fully
runnable offline (and free) we default to a deterministic local hashing
embedder over character n-grams — good enough for nearest-neighbour few-shot
retrieval of "similar past task". The interface is swappable: point `Embedder`
at an API embedding model later without touching the bank.
"""
from __future__ import annotations

import hashlib
import math
import re
from typing import List, Sequence

import numpy as np

_DIM = 512
_token_re = re.compile(r"[A-Za-zА-Яа-я0-9_]+")


def _char_ngrams(text: str, n: int = 3) -> List[str]:
    text = f"  {text.lower()}  "
    return [text[i:i + n] for i in range(len(text) - n + 1)]


class LocalHashingEmbedder:
    name = "local-hash"
    dim = _DIM

    def embed(self, text: str) -> np.ndarray:
        vec = np.zeros(_DIM, dtype=np.float32)
        feats = _token_re.findall(text.lower()) + _char_ngrams(text)
        for f in feats:
            h = int(hashlib.md5(f.encode()).hexdigest(), 16)
            idx = h % _DIM
            sign = 1.0 if (h >> 20) & 1 else -1.0
            vec[idx] += sign
        norm = np.linalg.norm(vec)
        return vec / norm if norm > 0 else vec

    def embed_many(self, texts: Sequence[str]) -> np.ndarray:
        return np.vstack([self.embed(t) for t in texts]) if texts else np.zeros((0, _DIM))


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    return float(np.dot(a, b) / denom) if denom else 0.0


# Default embedder used across the farm.
DEFAULT_EMBEDDER = LocalHashingEmbedder()
