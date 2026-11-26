# Entrega --- Desafio ETL Verdejar

## 1. Repositório

**GitHub:** https://github.com/wallacee20/desafio-felloship.git

**Branch de desenvolvimento:** `desafio-final-wallace`

**Pull Request:** \[[PR](https://github.com/wallacee20/desafio-felloship/pull/1)\]

## 2. Resumo da implementação

O projeto implementa um pipeline ETL em Python e PostgreSQL,
contemplando:

-   Extração paginada de clientes e pedidos por meio de uma API REST e
    leitura dos produtos em CSV.
-   Preservação dos dados brutos e geração de arquivos tratados.
-   Transformações e validações de qualidade conforme as regras A1--A6.
-   Carga no PostgreSQL respeitando a ordem das chaves estrangeiras.
-   Tratamento de conflitos com `ON CONFLICT DO NOTHING`.
-   Consultas SQL de validação e reconciliação financeira.
-   Testes automatizados com `pytest`.

## 3. Resultados verificados

  | Indicador                         | Resultado |
|-----------------------------------|----------:|
| Clientes carregados               | 1.000     |
| Produtos carregados               | 12        |
| Pedidos únicos carregados         | 5.000     |
| Itens de pedidos carregados       | 12.455    |
| Pedidos duplicados descartados    | 100       |
| Pedidos com divergência financeira| 238       |
| Diferença na reconciliação        | R$ 0,00   |
| Testes automatizados aprovados    | 8         |

## 4. Vídeo de demonstração

**Link:** \[[vídeo no youtube](https://youtu.be/bYCw5qPCkhs)\]

O vídeo apresentará a estrutura do projeto, a execução do pipeline, os
resultados no PostgreSQL, os testes e as verificações de reconciliação.

## 5. Registro de uso de Inteligência Artificial

Registro do uso de IA no Desafio Final (ETL Verdejar)

- Ferramenta usada: **Claude.ai**

- O que fiz sozinho, sem IA:
**Desenvolvimento, estruturação do projeto e organização dos diretórios.


Execução e acompanhamento do pipeline.



Análise de erros no VS Code.



Execução dos testes e interpretação dos resultados.



Execução das consultas SQL no PostgreSQL.



Verificação dos resultados da reconciliação.**

---

## 1. Sugestões aceitas

### Reconciliação dos valores dos itens

- **Tarefa delegada:**
  Orientação para verificar se os valores calculados na origem correspondiam aos valores persistidos no destino.

- **Trecho pedido:**
  Comparação entre a soma de quantidade × preço unitário na origem e no destino.
  
- **Decisão e justificativa:**
  Implementou a reconciliação com tolerância de um centavo

- **Como validei:**
  Executei a transformação e verificou a diferença entre os valores.

- **Retrabalho:**
  N/A


## 2. Sugestões rejeitadas


### Cálculo do total dos itens dos pedidos

- **Tarefa delegada:** Calcular o valor total dos itens de cada pedido.
- **O que a IA propôs:** Adicionar uma coluna total diretamente ao DataFrame df_itens.
- **Por que estava inadequada (com evidência):** Essa alteração poderia gerar incompatibilidade na etapa de carga, pois a tabela itens_pedido do banco não possui essa coluna no schema.sql.
- **O que fiz no lugar:** Criei uma cópia do DataFrame para adicionar a coluna total, utilizando-a apenas nos cálculos de reconciliação, sem alterar a estrutura dos dados destinados à carga.
- **Como validei:** Executei a transformação e conferi os valores calculados, preservando a estrutura esperada pelo banco de dados.

---

## 3. Falhas e retrabalho

### Chaves estrangeiras invertidas na conversão do brModelo (rascunho: reescrever com minhas palavras)

- **Contexto:** Pedi para validar a modelagem modelagem do banco que eu estava modelando no brModelo.

- **O que a IA orientou:** Na modelegaem de dados, ela recomendou alterar a cardinalidades na notação ((0,n) para clientes e (1,1)
  para pedidos), dizendo que estavam corretas.

- **O que estava errado:** ao converter para o modelo lógico, o brModelo criou as chaves
  estrangeiras nas tabelas pai, apontando para as filhas (por exemplo, `pedido_id` dentro
  de `clientes`).

- **Como encontrei:** ao abrir o diagrama lógico e ver as colunas `fk_itens_pedido_*` em
  `pedidos` e `produtos`.

- **Retrabalho:** apaguei as colunas erradas, recriei as chaves estrangeiras nas tabelas
  filhas e corrigi os tipos (`cliente_id` estava como VARCHAR).


## 4. Conclusão

O uso da IA foi importante durante o desenvolvimento do desafio, principalmente para esclarecer conceitos, analisar problemas e apoiar a implementação das etapas do ETL. Porém, procurei compreender cada sugestão antes de aplicá-la, avaliando sua compatibilidade com a estrutura do projeto e o contrato de dados.

Também optei por não aceitar sugestões que poderiam comprometer etapas posteriores, como a carga no banco de dados. Esse processo reforçou a importância de testar, validar e entender o código produzido.

Mais do que utilizar a IA para escrever código, busquei utilizá-la como uma ferramenta de aprendizado, mantendo a responsabilidade pelas decisões técnicas e pela qualidade da solução desenvolvida.
