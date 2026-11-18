# Como usei IA

Registro do uso de IA no Desafio Final (ETL Verdejar)

- Ferramenta usada: **[]**

- O que fiz sozinho, sem IA: **[]**

---

## 1. Sugestões aceitas

### 1.1 [título]

- **Tarefa delegada:**
- **Trecho pedido:**
- **Decisão e justificativa:**
- **Como validei:**
- **Retrabalho:**

### 1.2 [Ptítulo]

- **Tarefa delegada:**
- **Trecho pedido:**
- **Decisão e justificativa:**
- **Como validei:**
- **Retrabalho:**

---

## 2. Sugestões rejeitadas


### 2.1 [título]

- **Tarefa delegada:**
- **O que a IA propôs:**
- **Por que estava inadequada (com evidência):**
- **O que fiz no lugar:**
- **Como validei:**

### 2.2 [título]

- **Tarefa delegada:**
- **O que a IA propôs:**
- **Por que estava inadequada (com evidência):**
- **O que fiz no lugar:**
- **Como validei:**

---

## 3. Falhas e retrabalho

### 3.1 Chaves estrangeiras invertidas na conversão do brModelo (rascunho: reescrever com minhas palavras)

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

