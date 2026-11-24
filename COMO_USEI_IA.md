# Como usei IA

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