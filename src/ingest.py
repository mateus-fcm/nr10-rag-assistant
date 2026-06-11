import json
from datetime import datetime, timezone

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import (
    CHROMA_DB_DIR,
    CHUNKS_FILE,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    SOURCE_DOCUMENT,
)


def load_source_text() -> str:
    if not SOURCE_DOCUMENT.exists():
        raise FileNotFoundError(f"Source document not found: {SOURCE_DOCUMENT}")
    return SOURCE_DOCUMENT.read_text(encoding="utf-8")


def build_chunks(text: str) -> list[dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=120,
        separators=["\n## ", "\n\n", "\n", ". ", " "],
    )
    documents = splitter.create_documents([text])
    created_at = datetime.now(timezone.utc).isoformat()

    chunks = []
    for index, doc in enumerate(documents, start=1):
        chunks.append(
            {
                "id": f"demo-{index:03d}",
                "titulo": "Documento demonstrativo NR10",
                "secao": f"chunk-{index}",
                "pagina": "demo",
                "texto_original": doc.page_content.strip(),
                "texto_normalizado": doc.page_content.strip(),
                "tema": ["nr10", "seguranca eletrica", "documento demonstrativo"],
                "data_geracao": created_at,
            }
        )
    return chunks


def persist_chunks(chunks: list[dict]) -> None:
    CHUNKS_FILE.parent.mkdir(parents=True, exist_ok=True)
    CHUNKS_FILE.write_text(
        json.dumps(chunks, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def build_vector_store(chunks: list[dict]) -> None:
    if not chunks:
        raise ValueError("No chunks generated from the source document.")

    CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    texts = [chunk["texto_normalizado"] for chunk in chunks]
    metadatas = [
        {
            "id": chunk["id"],
            "titulo": chunk["titulo"],
            "secao": chunk["secao"],
            "pagina": chunk["pagina"],
            "tema": ", ".join(chunk["tema"]),
        }
        for chunk in chunks
    ]

    Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas,
        collection_name=COLLECTION_NAME,
        persist_directory=str(CHROMA_DB_DIR),
    )


def main() -> None:
    text = load_source_text()
    chunks = build_chunks(text)
    persist_chunks(chunks)
    build_vector_store(chunks)

    print(f"Generated {len(chunks)} chunks at {CHUNKS_FILE}")
    print(f"Vector database created at {CHROMA_DB_DIR}")


if __name__ == "__main__":
    main()
