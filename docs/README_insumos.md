# Insumos do Desafio Final do Bootcamp (Verdejar, empresa fictícia)

Versão v2 de 18/11/2026: acrescenta `schema_sqlite.sql` e os três caminhos para o banco, conforme a errata. Os dados, a API e o gerador não mudaram.

Conteúdo 100% sintético, gerado com seed reprodutível (2026). Apenas biblioteca padrão do Python 3; nenhuma dependência externa.

| Arquivo | Função |
|---|---|
| `gerar_dados.py` | Gera `dados/clientes.json`, `dados/pedidos.json` e `dados/produtos.csv`. Use `--seed` para reproduzir; a seed oficial do desafio é 2026. |
| `api_verdejar.py` | Sobe a API HTTP local em `http://127.0.0.1:8000` com as rotas `/clientes`, `/pedidos` (paginadas) e `/saude`. |
| `schema.sql` | Esquema de destino no PostgreSQL (tabelas clientes, produtos, pedidos, itens_pedido), para os caminhos A (PostgreSQL instalado) e B (PostgreSQL em Docker). |
| `schema_sqlite.sql` | O mesmo esquema adaptado ao SQLite, para o caminho C (contingência, sem instalar nada). Publicado com a errata de 18/11/2026. |
| `dados/` | Dados já gerados com a seed 2026, para quem preferir não rodar o gerador. |

## Passos

1. `python3 gerar_dados.py` (opcional; os dados da seed 2026 já acompanham a pasta).
2. `python3 api_verdejar.py` e, em outro terminal, `curl "http://127.0.0.1:8000/saude"`.
3. Subir o banco pelo caminho escolhido na seção 4 do desafio (A: PostgreSQL instalado, recomendado; B: PostgreSQL em Docker, opcional; C: SQLite) e aplicar o esquema correspondente (`schema.sql` ou `schema_sqlite.sql`). Docker não é obrigatório nem avaliado.

## Armadilhas declaradas nos dados

Os dados contêm, de propósito, seis problemas de qualidade que o ETL precisa tratar. Eles estão descritos no documento do desafio (seção Contexto) e no cabeçalho de `gerar_dados.py`: e-mails ausentes, sigla de estado em caixa mista, datas em dois formatos, valor em texto com vírgula, pedidos repetidos entre páginas e valor total divergente da soma dos itens.

Os totais de referência para a correção ficam em arquivo separado, de uso exclusivo da equipe de correção; o Fellow deve calcular os seus próprios totais a partir dos dados e registrá-los no README do projeto.
