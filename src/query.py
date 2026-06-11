from src.answer_generator import generate_answer, generate_chat_response
from src.hybrid_search import hybrid_search
from src.intent_detector import detect_intent
from src.query_normalizer import normalize_query
from src.reranker import rerank_results


def answer_question(question: str) -> str:
    question = question.strip()
    if not question:
        return "Envie uma pergunta para consultar a base demonstrativa."

    if detect_intent(question) == "chat":
        return generate_chat_response(question)

    normalized = normalize_query(question)
    results = hybrid_search(normalized, k=3)
    best_result = rerank_results(normalized, results)

    if best_result is None:
        return "Nenhum trecho relevante foi encontrado na base demonstrativa."

    return generate_answer(question, best_result)


def main() -> None:
    print("nr10-rag-assistant - consulta local. Digite 'sair' para encerrar.")
    while True:
        question = input("Pergunta: ").strip()
        if question.lower() in {"sair", "exit", "quit"}:
            break
        print(answer_question(question))
        print()


if __name__ == "__main__":
    main()
