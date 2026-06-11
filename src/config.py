from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _path_from_env(name: str, default: str) -> Path:
    raw = os.getenv(name, default)
    path = Path(raw)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path.resolve()


OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "intfloat/multilingual-e5-large")

SOURCE_DOCUMENT = _path_from_env("SOURCE_DOCUMENT", "data/exemplo.txt")
CHUNKS_FILE = _path_from_env("CHUNKS_FILE", "data/generated_chunks.json")
CHROMA_DB_DIR = _path_from_env("CHROMA_DB_DIR", "data/chroma_db")

COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "nr10_demo")
