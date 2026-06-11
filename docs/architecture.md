# Arquitetura

O `nr10-rag-assistant` usa uma arquitetura RAG em camadas para consultar documentos tecnicos por linguagem natural. A versao publica usa um documento ficticio, mas o desenho e o mesmo para normas, procedimentos e bases tecnicas reais.

## Pipeline

1. **Ingestao**: le o documento fonte configurado por `SOURCE_DOCUMENT`, divide o texto em chunks e gera `data/generated_chunks.json` localmente.
2. **Embeddings**: converte cada chunk em vetor numerico usando `intfloat/multilingual-e5-large` por padrao.
3. **Persistencia vetorial**: salva os vetores no ChromaDB em `data/chroma_db/`.
4. **Normalizacao**: reescreve a pergunta em linguagem tecnica.
5. **Busca hibrida**: combina busca semantica no ChromaDB com BM25 lexical.
6. **Reranking**: um LLM local avalia os candidatos e seleciona o trecho mais aderente.
7. **Resposta**: o LLM local gera uma resposta final baseada no trecho selecionado.

## Separacao de Responsabilidades

- `src/ingest.py`: prepara chunks e banco vetorial.
- `src/hybrid_search.py`: recupera candidatos.
- `src/query_normalizer.py`: melhora a pergunta para busca.
- `src/reranker.py`: escolhe o melhor contexto.
- `src/answer_generator.py`: gera resposta final.
- `src/query.py`: orquestra o pipeline.
- `web/app.py`: interface Flask.

## Por Que Busca Hibrida

Busca semantica captura significado, mas pode perder termos muito especificos, como numeros de secao, siglas e expressoes normativas. BM25 captura correspondencia lexical exata, mas falha quando o usuario faz uma pergunta com palavras diferentes do documento.

A busca hibrida combina os dois sinais. Isso melhora consultas tecnicas em que tanto o significado quanto a literalidade dos termos importam.
