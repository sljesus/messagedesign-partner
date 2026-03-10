import os
import pickle
from typing import List

import numpy as np

try:
    import faiss
except Exception:
    faiss = None

try:
    from sentence_transformers import SentenceTransformer
except Exception:
    SentenceTransformer = None


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
INDEX_DIR = os.path.join(BASE_DIR, "data", "docs_index")
INDEX_PATH = os.path.join(INDEX_DIR, "faiss.index")
META_PATH = os.path.join(INDEX_DIR, "meta.pkl")
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def _read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def _iter_chunks(text: str, chunk_size: int = 1000, overlap: int = 150):
    if not text:
        return
    start = 0
    text_len = len(text)
    # Safety guard to avoid infinite loops in case of bad params.
    max_iters = (text_len // max(1, chunk_size - overlap)) + 2
    iters = 0
    while start < text_len and iters < max_iters:
        end = min(text_len, start + chunk_size)
        chunk = text[start:end].strip()
        if chunk:
            yield chunk
        if end >= text_len:
            break
        start = max(0, end - overlap)
        iters += 1


def build_index():
    if SentenceTransformer is None:
        raise RuntimeError("sentence-transformers not installed")
    if faiss is None:
        raise RuntimeError("faiss not installed")

    try:
        model = SentenceTransformer(MODEL_NAME, local_files_only=True)
    except Exception as e:
        raise RuntimeError(
            "sentence-transformers model not available locally. "
            "Run once with internet access to cache the model."
        ) from e

    files = []
    for root, _, filenames in os.walk(DOCS_DIR):
        for name in filenames:
            if name.lower().endswith(".md"):
                files.append(os.path.join(root, name))

    batch_texts = []
    batch_meta = []
    meta = []
    index = None
    for path in files:
        text = _read_text(path)
        for i, chunk in enumerate(_iter_chunks(text)):
            batch_texts.append(chunk)
            batch_meta.append({"source": os.path.relpath(path, BASE_DIR), "chunk_id": i, "text": chunk})
            if len(batch_texts) >= 32:
                embeddings = model.encode(batch_texts, batch_size=32, normalize_embeddings=True)
                embeddings = np.array(embeddings, dtype=np.float32)
                if index is None:
                    index = faiss.IndexFlatIP(embeddings.shape[1])
                index.add(embeddings)
                meta.extend(batch_meta)
                batch_texts.clear()
                batch_meta.clear()

    if batch_texts:
        embeddings = model.encode(batch_texts, batch_size=32, normalize_embeddings=True)
        embeddings = np.array(embeddings, dtype=np.float32)
        if index is None:
            index = faiss.IndexFlatIP(embeddings.shape[1])
        index.add(embeddings)
        meta.extend(batch_meta)

    if index is None or not meta:
        raise RuntimeError("no docs found to index")

    os.makedirs(INDEX_DIR, exist_ok=True)
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(meta, f)

    print(f"Indexed {len(meta)} chunks from {len(files)} files")


if __name__ == "__main__":
    build_index()
