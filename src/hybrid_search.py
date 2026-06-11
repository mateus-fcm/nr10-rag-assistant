import json
import re

import numpy as np
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from rank_bm25 import BM25Okapi

from src.config import CHROMA_DB_DIR, CHUNKS_FILE, COLLECTION_NAME, EMBEDDING_MODEL


def _load_chunks() -> list[dict]:
    if not CHUNKS_FILE.exists():
        raise FileNotFoundError(
            f"Chunks file not found: {CHUNKS_FILE}. Run `python -m src.ingest` first."
        )

    data = json.loads(CHUNKS_FILE.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        for key in ("conteudo", "chunks", "items", "data"):
            if isinstance(data.get(key), list):
                data = data[key]
                break
    return [item for item in data if isinstance(item, dict)]


def _tokenize(text: str) -> list[str]:
    return re.findall(r"\d+\.\d+(?:\.\d+)?|\w+", text.lower())


def _bm25(chunks: list[dict]) -> tuple[BM25Okapi, list[str]]:
    corpus = [
        " ".join(
            [
                str(item.get("secao", "")),
                str(item.get("titulo", "")),
                str(item.get("texto_normalizado") or item.get("texto_original") or ""),
            ]
        ).strip()
        for item in chunks
    ]
    return BM25Okapi([_tokenize(text) for text in corpus]), corpus


def _direct_section_match(query: str, chunks: list[dict], k: int) -> list[Document]:
    match = re.search(r"\b\d{1,2}\.\d+(?:\.\d+)?[a-z]?\b", query)
    if not match:
        return []

    section = match.group(0)
    docs = []
    for item in chunks:
        hierarchy = " ".join(map(str, item.get("hierarquia", [])))
        if str(item.get("secao", "")).startswith(section) or section in hierarchy:
            docs.append(
                Document(
                    page_content=item.get("texto_normalizado") or item.get("texto_original", ""),
                    metadata=item,
                )
            )
    return docs[:k]


def hybrid_search(query: str, k: int = 3, alpha: float = 0.7) -> list[Document]:
    chunks = _load_chunks()

    direct_matches = _direct_section_match(query, chunks, k)
    if direct_matches:
        return direct_matches

    bm25, corpus = _bm25(chunks)
    lexical_scores = bm25.get_scores(_tokenize(query))
    lexical_max = float(np.max(lexical_scores)) if len(lexical_scores) else 0.0

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    db = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=str(CHROMA_DB_DIR),
        embedding_function=embeddings,
    )
    vector_results = db.similarity_search_with_score(query, k=k * 3)

    combined = []
    for doc, vector_distance in vector_results:
        try:
            index = corpus.index(doc.page_content)
        except ValueError:
            index = -1

        lexical_score = 0.0 if index < 0 or lexical_max == 0 else lexical_scores[index] / lexical_max
        semantic_score = 1.0 / (1.0 + float(vector_distance))
        combined_score = (alpha * semantic_score) + ((1 - alpha) * lexical_score)
        combined.append((doc, combined_score))

    combined.sort(key=lambda item: item[1], reverse=True)
    return [doc for doc, _ in combined[:k]]
