# Contrato de Dados --- Verdejar

**Versão:** 1.0\
**Projeto:** Desafio Final do Bootcamp AI/R Fellowship\
**Domínio:** Comercial / Vendas\
**Banco de dados:** PostgreSQL\
**Responsável:** Wallace Almeida\
**Origem dos dados:** Arquivos CSV\
**Destino:** Banco de dados PostgreSQL

## 1. Objetivo

Estabelecer um padrão para o recebimento, processamento, validação e
armazenamento dos dados de clientes, produtos, pedidos e itens de
pedidos, definindo a estrutura esperada, as regras de integridade e os
critérios mínimos de qualidade.

Este contrato foi elaborado com base no esquema SQL fornecido para o
projeto Verdejar.

## 2. Escopo

O contrato contempla as seguintes entidades:

-   `clientes`
-   `produtos`
-   `pedidos`
-   `itens_pedido`

## 3. Modelo lógico e relacionamentos

-   **Clientes → Pedidos:** relacionamento 1:N. `pedidos.cliente_id`
    referencia `clientes.id`.
-   **Pedidos → Itens de pedido:** relacionamento 1:N.
    `itens_pedido.pedido_id` referencia `pedidos.id`.
-   **Produtos → Itens de pedido:** relacionamento 1:N.
    `itens_pedido.produto_id` referencia `produtos.produto_id`.

A chave primária de `itens_pedido` é composta por `pedido_id` e `linha`.

## 4. Dicionário de dados

### 4.1 Tabela `clientes`

  Campo           Tipo        Obrigatório Regra
  --------------- --------- ------------- -----------------------------
  `id`            INTEGER             Sim Chave primária
  `nome`          TEXT                Sim Não pode ser nulo
  `email`         TEXT                Não Pode ser nulo
  `cidade`        TEXT                Sim Não pode ser nulo
  `estado`        CHAR(2)             Sim Deve conter dois caracteres
  `cadastro_em`   DATE                Sim Data válida

### 4.2 Tabela `produtos`

  Campo          Tipo              Obrigatório Regra
  -------------- --------------- ------------- -------------------
  `produto_id`   INTEGER                   Sim Chave primária
  `nome`         TEXT                      Sim Não pode ser nulo
  `categoria`    TEXT                      Sim Não pode ser nulo
  `preco_base`   NUMERIC(10,2)             Sim Não pode ser nulo

### 4.3 Tabela `pedidos`

  Campo           Tipo              Obrigatório Regra
  --------------- --------------- ------------- --------------------------------------
  `id`            INTEGER                   Sim Chave primária
  `cliente_id`    INTEGER                   Sim Chave estrangeira para `clientes.id`
  `data_pedido`   DATE                      Sim Data válida
  `status`        TEXT                      Sim Não pode ser nulo
  `valor_total`   NUMERIC(12,2)             Sim Não pode ser nulo
  `valor_itens`   NUMERIC(12,2)             Sim Não pode ser nulo
  `divergente`    BOOLEAN                   Sim Padrão `FALSE`

### 4.4 Tabela `itens_pedido`

  ---------------------------------------------------------------------------------
  Campo              Tipo                       Obrigatório Regra
  ------------------ ---------------- --------------------- -----------------------
  `pedido_id`        INTEGER                            Sim Chave estrangeira para
                                                            `pedidos.id` e parte da
                                                            chave primária

  `linha`            INTEGER                            Sim Parte da chave primária

  `produto_id`       INTEGER                            Sim Chave estrangeira para
                                                            `produtos.produto_id`

  `quantidade`       INTEGER                            Sim Não pode ser nulo

  `preco_unitario`   NUMERIC(10,2)                      Sim Não pode ser nulo
  ---------------------------------------------------------------------------------

## 5. Regras de qualidade dos dados

As regras abaixo combinam as restrições presentes no esquema SQL com
validações recomendadas para o pipeline. As regras recomendadas devem
ser implementadas e documentadas antes de serem consideradas
obrigatórias no banco.

  -----------------------------------------------------------------------
  Dimensão                Regra                   Origem
  ----------------------- ----------------------- -----------------------
  Completude              Campos definidos como   Schema SQL
                          obrigatórios não podem  
                          ser nulos               

  Unicidade               Chaves primárias devem  Schema SQL
                          ser únicas              

  Integridade referencial Todo pedido deve        Schema SQL
                          referenciar um cliente  
                          existente               

  Integridade referencial Todo item deve          Schema SQL
                          referenciar um pedido   
                          existente               

  Integridade referencial Todo item deve          Schema SQL
                          referenciar um produto  
                          existente               

  Padronização            `estado` deve conter    Tipo `CHAR(2)` no
                          dois caracteres         schema; validar
                                                  domínio/UF no ETL

  Consistência            Valores monetários      Schema SQL
                          devem respeitar a       
                          precisão e escala       
                          definidas               

  Consistência            Quantidade deve ser     Recomendação a
                          maior que zero          implementar

  Consistência            Datas devem ser válidas Recomendação a
                                                  implementar

  Reconciliação           Comparar o valor total  Recomendação a
                          do pedido com a soma    implementar
                          dos itens               
  -----------------------------------------------------------------------

## 6. Regras de processamento ETL

1.  Identificar os arquivos de origem esperados para cada entidade.
2.  Validar a presença das colunas previstas no contrato.
3.  Verificar campos obrigatórios, tipos e formatos.
4.  Identificar registros duplicados e aplicar a regra de deduplicação
    definida pelo projeto.
5.  Validar as referências entre clientes, pedidos, produtos e itens.
6.  Aplicar as transformações e padronizações documentadas no projeto.
7.  Calcular ou validar os valores dos itens e dos pedidos conforme as
    regras de negócio.
8.  Sinalizar pedidos com divergência por meio do campo `divergente`.
9.  Registrar métricas da execução, incluindo registros lidos, válidos,
    rejeitados e carregados.
10. Executar a reconciliação entre origem e destino.

## 7. Estratégia de carga

O pipeline poderá operar com:

-   **Carga full:** reprocessamento do conjunto de dados de origem,
    conforme a estratégia de limpeza e recarga adotada.
-   **Carga incremental:** processamento apenas dos registros novos ou
    alterados, desde que exista um critério confiável de identificação,
    como data de atualização, identificador de lote ou mecanismo de
    comparação.

O esquema fornecido não contém, por si só, campos de controle de
atualização ou de lote. Caso sejam necessários, deverão ser adicionados
e documentados.

## 8. Critérios de aceite

Um lote poderá ser considerado aprovado quando:

-   Os arquivos esperados forem identificados e lidos.
-   A estrutura das colunas estiver de acordo com o contrato.
-   Os campos obrigatórios e os tipos forem validados.
-   As chaves primárias não apresentarem duplicidade.
-   As referências entre as entidades forem válidas.
-   As regras de consistência e reconciliação forem executadas.
-   Os registros rejeitados forem contabilizados e tiverem tratamento
    definido.
-   As métricas da execução forem registradas.
-   A quantidade de registros de origem e destino for reconciliada,
    considerando rejeições e regras de transformação documentadas.

## 9. Versionamento e governança

O contrato deve ser versionado sempre que houver alteração na estrutura,
nos tipos, nas regras de qualidade ou nas regras de negócio.

  Versão   Descrição
  -------- ----------------------------------------------------
  1.0      Contrato inicial baseado no `schema.sql` fornecido

Alterações incompatíveis --- como remoção de colunas, mudança de tipo ou
alteração de significado de campos --- devem gerar uma nova versão
principal e ser comunicadas aos consumidores dos dados.

## 10. Observações e limitações

-   O contrato descreve as quatro tabelas presentes no esquema SQL
    recebido.
-   O esquema não define domínio permitido para `status`.
-   O esquema não estabelece limites mínimos ou máximos para preços e
    valores.
-   O esquema não define uma regra de tolerância para divergências
    financeiras.
-   O esquema não contém campos específicos para auditoria, data de
    atualização ou identificação de lote.
-   Regras adicionais devem ser implementadas no ETL ou incorporadas ao
    banco por meio de alterações documentadas.

## 11. Referência

Documento elaborado a partir do arquivo `schema.sql` do projeto Desafio
Final do Bootcamp AI/R Fellowship --- Verdejar.
