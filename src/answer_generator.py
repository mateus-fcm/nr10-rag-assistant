from langchain_core.documents import Document
from langchain_ollama import OllamaLLM

from src.config import OLLAMA_BASE_URL, OLLAMA_MODEL


def generate_answer(question: str, context_doc: Document) -> str:
    metadata = context_doc.metadata
    prompt = f"""
Voce e um assistente tecnico para consulta demonstrativa sobre seguranca eletrica.
Responda em portugues, de forma objetiva e profissional, usando somente o trecho fornecido.

Pergunta:
{question}

Trecho recuperado:
Titulo: {metadata.get("titulo", "Sem titulo")}
Secao: {metadata.get("secao", "?")}
Pagina: {metadata.get("pagina", "?")}
Texto: {context_doc.page_content.strip()}

Instrucoes:
- Baseie a resposta exclusivamente no trecho.
- Cite a secao ou identificador quando for util.
- Se o trecho nao for suficiente, diga que a base demonstrativa nao contem informacao bastante.
- Nao apresente esta resposta como parecer tecnico oficial.
""".strip()

    try:
        llm = OllamaLLM(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)
        answer = llm.invoke(prompt).strip()
        if answer:
            return answer
    except Exception as exc:
        return f"Nao foi possivel chamar o modelo local via Ollama: {exc}"

    return "Nao foi possivel gerar uma resposta com o modelo local."


def generate_chat_response(query: str) -> str:
    return (
        "Ola. Sou um assistente demonstrativo para consultas tecnicas em NR10. "
        "Pergunte sobre medidas de controle, desenergizacao, trabalho em proximidade ou profissional autorizado."
    )
