# nr10-rag-assistant

Assistente RAG tecnico especializado em NR10, criado como projeto demonstrativo de portfolio. O sistema combina ingestao documental, embeddings, ChromaDB, busca hibrida, normalizacao de pergunta, reranking com LLM e geracao de resposta usando LLM local via Ollama.

> Esta versao publica nao inclui bancos vetoriais, chunks gerados, credenciais, caches, logs ou documentos internos. Os dados demonstrativos em `data/exemplo.txt` sao ficticios e servem apenas para mostrar o fluxo.

## Problema Resolvido

Normas tecnicas e documentos regulatorios costumam ser extensos, densos e dificeis de consultar por linguagem natural. Este projeto demonstra uma arquitetura RAG para responder perguntas tecnicas com base em trechos documentais recuperados, reduzindo respostas genericas e mantendo rastreabilidade para o texto de origem.

A mesma arquitetura pode ser adaptada para outros documentos normativos, manuais tecnicos, politicas internas, procedimentos operacionais ou bases de conhecimento especializadas.

## Arquitetura

O pipeline e separado em camadas:

1. **Ingestao documental**: le um documento texto, quebra em chunks e salva os artefatos gerados localmente.
2. **Embeddings**: transforma cada chunk em vetor usando Sentence Transformers via LangChain.
3. **ChromaDB**: armazena os vetores para busca semantica local.
4. **Normalizacao da pergunta**: reescreve a pergunta em linguagem tecnica para melhorar recuperacao.
5. **Busca hibrida**: combina similaridade semantica com BM25 lexical.
6. **Reranking via LLM**: escolhe o trecho mais aderente entre os candidatos recuperados.
7. **Geracao de resposta**: usa Ollama local para responder com base no trecho selecionado.
8. **Interface web**: expoe um chat Flask simples para demonstracao.

## Estrutura

```text
README.md
.gitignore
.env.example
requirements.txt
data/
  exemplo.txt
src/
  ingest.py
  query.py
  hybrid_search.py
  intent_detector.py
  query_normalizer.py
  reranker.py
  answer_generator.py
  config.py
web/
  app.py
  templates/
    index.html
docs/
  architecture.md
  workflow.md
  confidentiality.md
examples/
  sample_questions.md
  sample_outputs.md
```

## Requisitos

- Python 3.10+
- Ollama instalado localmente
- Um modelo disponivel no Ollama, por exemplo `mistral`

## Instalacao

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Edite `.env` se quiser trocar o modelo ou os caminhos locais.

## Execucao

1. Gere os chunks e o banco vetorial local:

```powershell
python -m src.ingest
```

2. Faca uma pergunta pelo terminal:

```powershell
python -m src.query
```

3. Ou rode a interface web:

```powershell
python web/app.py
```

Depois acesse `http://localhost:5000`.

## Artefatos Gerados

A ingestao cria arquivos locais como:

- `data/generated_chunks.json`
- `data/chroma_db/`

Esses arquivos nao sao versionados porque podem conter conteudo derivado do documento original, indices vetoriais, metadados sensiveis ou dados grandes gerados em runtime. Em uma instalacao nova, basta executar `python -m src.ingest` para recria-los.

## Uso Demonstrativo

Este projeto nao substitui leitura oficial da NR10, parecer tecnico, avaliacao juridica ou decisao de seguranca do trabalho. A versao publica existe para demonstrar arquitetura e engenharia de um assistente RAG local, com dados ficticios e sem conteudo confidencial.
