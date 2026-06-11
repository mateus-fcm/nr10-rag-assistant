import re

from langchain_core.documents import Document
from langchain_ollama import OllamaLLM

from src.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from src.query_normalizer import CANONICAL_TERMS


def rerank_results(question: str, results: list[Document]) -> Document | None:
    if not results:
        return None
    if len(results) == 1:
        return results[0]

    context = []
    for index, result in enumerate(results, start=1):
        metadata = result.metadata
        context.append(
            f"[{index}] {metadata.get('titulo', 'Sem titulo')} - "
            f"Secao {metadata.get('secao', '?')} (pagina {metadata.get('pagina', '?')})\n"
            f"{result.page_content.strip()}"
        )

    prompt = f"""
Voce atua como reranqueador de um sistema RAG tecnico.
Escolha exatamente um trecho que melhor responda a pergunta.

Pergunta:
{question}

Termos tecnicos de referencia:
{", ".join(CANONICAL_TERMS)}

Trechos:
{chr(10).join(context)}

Responda apenas com o numero do melhor trecho.
""".strip()

    try:
        llm = OllamaLLM(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)
        response = llm.invoke(prompt).strip()
        match = re.search(r"\d+", response)
        if match:
            selected = int(match.group(0)) - 1
            if 0 <= selected < len(results):
                return results[selected]
    except Exception:
        pass

    return results[0]
