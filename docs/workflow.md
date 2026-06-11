# Workflow

Fluxo completo do projeto:

```text
documento -> chunks -> embeddings -> ChromaDB -> pergunta -> normalizacao -> busca hibrida -> reranking -> resposta
```

## Passo a Passo

1. `data/exemplo.txt` fornece o documento demonstrativo.
2. `python -m src.ingest` divide o texto em chunks e cria `data/generated_chunks.json`.
3. Cada chunk e transformado em embedding.
4. Os vetores sao armazenados em `data/chroma_db/`.
5. O usuario envia uma pergunta pelo terminal ou pela interface Flask.
6. `src/query_normalizer.py` reescreve a pergunta em formato tecnico.
7. `src/hybrid_search.py` combina busca vetorial com BM25 lexical.
8. `src/reranker.py` escolhe o melhor trecho entre os candidatos.
9. `src/answer_generator.py` gera a resposta final via Ollama.
