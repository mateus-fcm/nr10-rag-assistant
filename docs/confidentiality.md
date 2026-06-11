# Confidencialidade

Esta versao publica foi preparada para portfolio e nao inclui:

- arquivos `.env`;
- credenciais, tokens ou senhas;
- bancos vetoriais gerados;
- chunks derivados de documentos internos;
- caches Python;
- logs;
- arquivos temporarios;
- backups antigos;
- caminhos locais de desenvolvimento;
- documentos privados ou internos.

## Artefatos Locais

Os seguintes caminhos sao gerados em runtime e ignorados pelo Git:

- `data/chroma_db/`
- `data/*chunks*.json`
- `outputs/`
- `artifacts/`

## Dados Demonstrativos

`data/exemplo.txt` contem texto ficticio e sintetico. Ele serve apenas para demonstrar o pipeline RAG e nao deve ser interpretado como reproducao oficial da NR10.

## Uso Esperado

Para usar documentos reais, coloque o material em ambiente local controlado, ajuste `SOURCE_DOCUMENT` no `.env` e execute a ingestao novamente. Nao publique os chunks ou o banco vetorial se eles forem derivados de material confidencial.
