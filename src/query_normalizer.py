import re

from langchain_ollama import OllamaLLM

from src.config import OLLAMA_BASE_URL, OLLAMA_MODEL

CANONICAL_TERMS = [
    "zona de risco",
    "zona controlada",
    "zona livre",
    "trabalho em proximidade",
    "desenergizacao",
    "seccionamento",
    "bloqueio e etiquetagem",
    "permissao de trabalho",
    "profissional autorizado",
    "profissional qualificado",
    "responsavel tecnico",
    "medidas de controle",
    "PIE",
    "area classificada",
]


def _looks_like_definition(text: str) -> bool:
    return bool(re.search(r"\b(o que e|oq|oque|defina|conceito|significado)\b", text, re.I))


def normalize_query(question: str) -> str:
    if _looks_like_definition(question):
        fallback = f"Definicao tecnica: {question}"
    else:
        fallback = question

    prompt = f"""
Voce e um normalizador de perguntas para um sistema RAG tecnico.
Reescreva a pergunta em uma unica linha, usando terminologia objetiva e adequada para busca em documentos de seguranca eletrica.

Termos de referencia:
{", ".join(CANONICAL_TERMS)}

Regras:
- Preserve o sentido original.
- Nao responda a pergunta.
- Nao adicione explicacoes.
- Se houver numero de item ou secao, preserve o numero.

Pergunta original:
{question}

Pergunta normalizada:
""".strip()

    try:
        llm = OllamaLLM(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)
        normalized = llm.invoke(prompt).strip()
        return normalized or fallback
    except Exception:
        return fallback
