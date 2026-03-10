import os
import pickle
from dataclasses import dataclass
from typing import List

import numpy as np


INDEX_DIR = os.path.join(os.path.dirname(__file__), "data", "docs_index")
INDEX_PATH = os.path.join(INDEX_DIR, "faiss.index")
META_PATH = os.path.join(INDEX_DIR, "meta.pkl")
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@dataclass
class RagHit:
    score: float
    text: str
    source: str
    chunk_id: int


_model = None
_index = None
_meta = None


def _get_model():
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
        except Exception as e:
            raise RuntimeError("sentence-transformers not installed") from e
        _model = SentenceTransformer(MODEL_NAME, local_files_only=True)
    return _model


def _load_index():
    global _index, _meta
    if _index is not None and _meta is not None:
        return _index, _meta
    try:
        import faiss
    except Exception as e:
        raise RuntimeError("faiss not installed") from e
    if not (os.path.exists(INDEX_PATH) and os.path.exists(META_PATH)):
        return None, None
    _index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "rb") as f:
        _meta = pickle.load(f)
    return _index, _meta


def search(query: str, top_k: int = 4) -> List[RagHit]:
    if not query:
        return []
    index, meta = _load_index()
    if index is None or meta is None:
        return []
    model = _get_model()
    emb = model.encode([query], normalize_embeddings=True)
    scores, idxs = index.search(np.array(emb, dtype=np.float32), top_k)
    hits = []
    for score, idx in zip(scores[0], idxs[0]):
        if idx < 0 or idx >= len(meta):
            continue
        item = meta[idx]
        hits.append(RagHit(score=float(score), text=item["text"], source=item["source"], chunk_id=item["chunk_id"]))
    return hits
