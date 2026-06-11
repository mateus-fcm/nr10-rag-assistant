# nr10-rag-assistant

Assistente RAG técnico especializado em documentos normativos, desenvolvido inicialmente como projeto acadêmico de inovação com foco na NR10.

O projeto surgiu a partir de um problema prático: normas técnicas extensas, densas e estruturadas em linguagem formal podem ser difíceis de consultar rapidamente. Mesmo quando a informação está presente no documento, encontrar o item correto pode ser cansativo, demorado e sujeito a interpretações incompletas.

Esta versão pública apresenta uma arquitetura demonstrativa de Retrieval-Augmented Generation (RAG), combinando ingestão documental, embeddings, ChromaDB, busca híbrida, normalização de pergunta, reranking com LLM e geração de resposta usando LLM local via Ollama.

> Esta versão pública não inclui bancos vetoriais, chunks gerados, credenciais, caches, logs ou documentos internos. Os dados demonstrativos em `data/exemplo.txt` são fictícios e servem apenas para mostrar o fluxo técnico.

## Problema Identificado

A NR10 é uma norma técnica essencial para segurança em instalações e serviços em eletricidade. Porém, como muitos documentos regulatórios, sua estrutura pode ser densa, extensa e difícil de navegar por linguagem natural.

Durante o desenvolvimento do projeto, o problema identificado foi a dificuldade de localizar rapidamente informações específicas dentro da norma, especialmente quando o usuário não sabe exatamente qual termo técnico, item ou seção procurar.

Esse tipo de dificuldade pode gerar:

* perda de tempo na consulta manual;
* dependência de busca por palavras exatas;
* leitura repetitiva de trechos longos;
* dificuldade para usuários menos familiarizados com a estrutura da norma;
* risco de respostas genéricas quando ferramentas de IA não usam uma base documental controlada.

## Solução Proposta

A solução proposta foi um assistente técnico baseado em RAG, capaz de receber perguntas em linguagem natural, recuperar trechos relevantes da base documental e gerar uma resposta contextualizada com base no conteúdo recuperado.

Diferente de um chatbot genérico, o sistema não responde apenas com conhecimento prévio do modelo. Ele segue um pipeline de recuperação e validação contextual antes da geração da resposta.

A mesma arquitetura pode ser adaptada para outros documentos normativos, manuais técnicos, políticas internas, procedimentos operacionais ou bases de conhecimento especializadas.

## Arquitetura

O pipeline é separado em camadas:

1. **Ingestão documental**: lê um documento texto, quebra em chunks e salva os artefatos gerados localmente.
2. **Embeddings**: transforma cada chunk em vetor usando Sentence Transformers via LangChain.
3. **ChromaDB**: armazena os vetores para busca semântica local.
4. **Normalização da pergunta**: reescreve a pergunta em linguagem técnica para melhorar a recuperação.
5. **Busca híbrida**: combina similaridade semântica com BM25 lexical.
6. **Reranking via LLM**: avalia os candidatos recuperados e seleciona o trecho mais aderente.
7. **Geração de resposta**: usa Ollama local para responder com base no trecho selecionado.
8. **Interface web**: expõe um chat Flask simples para demonstração.

## Fluxo de Processamento

```text
Documento de entrada
  ↓
Divisão em chunks
  ↓
Geração de embeddings
  ↓
Indexação no ChromaDB
  ↓
Pergunta do usuário
  ↓
Detecção de intenção
  ↓
Normalização técnica da pergunta
  ↓
Busca híbrida lexical + semântica
  ↓
Reranking com LLM
  ↓
Geração da resposta com LLM local
```

## Estrutura do Projeto

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

## Componentes Principais

```text
src/ingest.py
  Executa a ingestão documental, gera chunks e prepara a base vetorial local.

src/query.py
  Executa o fluxo principal de pergunta e resposta pelo terminal.

src/hybrid_search.py
  Combina busca semântica com busca lexical BM25.

src/intent_detector.py
  Classifica a entrada do usuário e decide se o fluxo RAG deve ser acionado.

src/query_normalizer.py
  Reescreve a pergunta usando linguagem técnica para melhorar a recuperação.

src/reranker.py
  Usa LLM para selecionar o trecho mais relevante entre os candidatos recuperados.

src/answer_generator.py
  Gera a resposta final com base no contexto selecionado.

src/config.py
  Centraliza configurações, caminhos e variáveis de ambiente.

web/app.py
  Disponibiliza uma interface Flask simples para demonstração.
```

## Tecnologias Utilizadas

* Python
* ChromaDB
* BM25
* Sentence Transformers
* LangChain
* Ollama
* LLM local
* Flask

## Requisitos

* Python 3.10+
* Ollama instalado localmente
* Um modelo disponível no Ollama, por exemplo `mistral`

## Instalação

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Edite `.env` se quiser trocar o modelo ou os caminhos locais.

## Execução

Gere os chunks e o banco vetorial local:

```powershell
python -m src.ingest
```

Faça uma pergunta pelo terminal:

```powershell
python -m src.query
```

Ou rode a interface web:

```powershell
python web/app.py
```

Depois acesse:

```text
http://localhost:5000
```

## Artefatos Gerados

A ingestão cria arquivos locais como:

```text
data/generated_chunks.json
data/chroma_db/
```

Esses arquivos não são versionados porque podem conter conteúdo derivado do documento original, índices vetoriais, metadados sensíveis ou dados grandes gerados em runtime.

Em uma instalação nova, basta executar:

```powershell
python -m src.ingest
```

para recriá-los localmente.

## Uso Demonstrativo

Este projeto não substitui a leitura oficial da NR10, parecer técnico, avaliação jurídica ou decisão de segurança do trabalho.

A versão pública existe para demonstrar a arquitetura e a engenharia de um assistente RAG local aplicado a documentos técnicos, usando dados fictícios e sem conteúdo confidencial.

## Possíveis Aplicações

A arquitetura pode ser adaptada para:

* normas técnicas;
* manuais de engenharia;
* procedimentos operacionais;
* bases de conhecimento internas;
* políticas corporativas;
* documentos regulatórios;
* materiais de treinamento técnico.
