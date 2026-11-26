# Entrega --- Desafio ETL Verdejar

## 1. Repositório

**GitHub:** https://github.com/wallacee20/desafio-felloship.git

**Branch de desenvolvimento:** `desafio-final-wallace`

**Pull Request:** \[[inserir link](https://github.com/wallacee20/desafio-felloship/pull/1)\]

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

  Indicador                              Resultado
  ------------------------------------ -----------
  Clientes carregados                        1.000
  Produtos carregados                           12
  Pedidos únicos carregados                  5.000
  Itens de pedidos carregados               12.455
  Pedidos duplicados descartados               100
  Pedidos com divergência financeira           238
  Diferença na reconciliação              R\$ 0,00
  Testes automatizados aprovados                 8

## 4. Vídeo de demonstração

**Link:** \[[inserir link público do vídeo](https://youtu.be/bYCw5qPCkhs)\]

O vídeo apresentará a estrutura do projeto, a execução do pipeline, os
resultados no PostgreSQL, os testes e as verificações de reconciliação.

## 5. Registro de uso de Inteligência Artificial

### 5.1 Contexto

Durante o desenvolvimento do ETL Verdejar, utilizei o ChatGPT como
ferramenta de apoio e par de programação com escopo limitado, conforme
as orientações do desafio.

A IA auxiliou na compreensão dos requisitos, na organização de funções
específicas, na elaboração de testes e na investigação de erros. As
tarefas foram delimitadas por funcionalidade, como conversão de valores
monetários, remoção de pedidos duplicados, validação das regras de
transformação e implementação da carga no PostgreSQL.

Fiquei responsável por executar os comandos, analisar os resultados,
corrigir problemas e decidir quais sugestões aceitar, adaptar ou
rejeitar. O desenvolvimento foi realizado progressivamente, validando
cada etapa antes de avançar.

### 5.2 Sugestões aceitas

  -----------------------------------------------------------------------
  Sugestão                            Justificativa e validação
  ----------------------------------- -----------------------------------
  Utilizar `Decimal` para valores     Aceitei `Decimal` para tratar
  monetários                          valores monetários e reduzir
                                      problemas de precisão. Validei os
                                      resultados com os testes e a
                                      reconciliação financeira, cuja
                                      diferença final foi de R\$ 0,00.

  Criar testes automatizados com      Os testes permitiram verificar as
  `pytest`                            regras de transformação e a geração
                                      do relatório de qualidade.

  Utilizar `ON CONFLICT DO NOTHING`   O teste com
  na carga                            `to_sql(..., if_exists="append")`
                                      apresentou conflito de chave
                                      primária na segunda execução.
                                      Adotei `ON CONFLICT DO NOTHING`
                                      para ignorar registros cuja chave
                                      já existe. Validei a estratégia
                                      reexecutando a carga e conferindo
                                      as quantidades no PostgreSQL.

  Separar regras de transformação em  A separação das regras A1--A6
  funções e módulos                   facilitou a organização e a
                                      validação. As alterações foram
                                      verificadas com testes e execução
                                      do ETL.

  Gerar um relatório de qualidade     Aceitei um módulo próprio para
                                      gerar relatório por execução, com
                                      data, hora e contadores A1--A6.
                                      Validei com dados fictícios e
                                      reais.
  -----------------------------------------------------------------------

### 5.3 Sugestões rejeitadas ou adaptadas

  -----------------------------------------------------------------------
  Sugestão                            Motivo da decisão
  ----------------------------------- -----------------------------------
  Adiar a separação das funções de    Adaptei a recomendação e organizei
  transformação                       as regras antes da entrega para
                                      facilitar leitura, testes e
                                      manutenção.

  Criar um arquivo separado apenas    Rejeitei o arquivo adicional e
  para testar A6                      mantive a validação permanente em
                                      `tests/test_transformacao.py`.

  Utilizar apenas                     A reexecução demonstrou erro de
  `to_sql(..., if_exists="append")`   chave primária duplicada; adaptei a
                                      carga para
                                      `ON CONFLICT DO NOTHING`.

  Repetir um comando sem investigar a Conferi a estrutura dos arquivos e
  falha                               o ambiente antes de repetir
                                      comandos, buscando corrigir a causa
                                      do problema.
  -----------------------------------------------------------------------

### 5.4 Falhas e retrabalho

#### Extração da API

A extração precisou ser revisada para tratar falhas de conexão e
respostas HTTP inválidas. Foram verificadas uma conexão recusada e uma
rota inexistente, que retornou HTTP 404.

#### Consulta SQL no pgAdmin

Uma consulta anterior permaneceu no editor e provocou um erro de sintaxe
relacionado ao `ORDER BY`:

``` text
SQL state: 42601
```

Resolvi o problema removendo a consulta anterior antes de executar o
novo SQL. Na validação de vendas, comparei a soma mensal com o total
geral: ambos resultaram em R\$ 311.228,75, com diferença de R\$ 0,00.

#### Carga no PostgreSQL

Inicialmente, utilizei `to_sql` com `if_exists="append"`. A primeira
execução inseriu os produtos, mas a segunda apresentou erro de chave
primária duplicada. Adotei `ON CONFLICT DO NOTHING` para ignorar
registros com chave já existente, sem atualizar os dados previamente
carregados.

#### Ambiente de testes

O comando `python -m pytest` apresentou `No module named pytest` porque
o terminal utilizava um interpretador Python sem o pacote instalado. A
validação final deve ser feita com o ambiente virtual do projeto ativo e
o `pytest` instalado nele.

#### Organização do código de transformação

Durante a revisão das funções A1--A6, os testes identificaram:

``` text
NameError: name 'A1' is not defined
```

O identificador de uma seção estava sem `#` e foi interpretado como
código Python. Após corrigir o comentário, executei novamente os testes.

### 5.5 Evidências de validação

  Verificação                         Resultado
  ----------------------------------- --------------------------------------
  Pedidos duplicados removidos        100
  Pedidos divergentes identificados   238
  Pedidos carregados                  5.000
  Reconciliação financeira            Diferença de R\$ 0,00
  Idempotência da carga               Quantidades mantidas após reexecução
  Suíte de testes                     8 testes aprovados

**Decisão sobre arquivo adicional:**

> Eu não vou criar um arquivo novo somente para o A6; vou fazer a
> validação no conjunto de testes.

**Erro encontrado no pgAdmin:**

``` text
ERROR: erro de sintaxe em ou próximo a "ORDER"
SQL state: 42601
```

**Resultados registrados do pytest:** - Antes do teste do relatório de
qualidade: `7 passed`. - Suíte completa, incluindo o teste do relatório
de qualidade: `8 passed`.

### 5.6 Stretch 3 --- Relatório de Qualidade

**Objetivo:** gerar um relatório automático com data, hora e contadores
das seis regras A1--A6.

**Sugestão da IA:** criar `etl/relatorio_qualidade.py`, gerar arquivos
`.txt` com `datetime` e `pathlib` e integrar a geração ao `pipeline.py`
após a carga.

**Decisão:** aceitei o módulo separado e a geração de um arquivo por
execução. A pasta `relatorios/` foi adicionada ao `.gitignore` para não
versionar arquivos gerados automaticamente.

**Validação:** verifiquei a sintaxe com `py_compile`, gerei um relatório
com dados fictícios e conferi seu conteúdo. Na execução com dados reais,
confirmei: A1 = 81, A2 = 151, A3 = 6.000, A4 = 17.467, A5 = 100 e A6 =
238. Depois, executei a suíte completa, obtendo 8 testes aprovados.

**Limitação identificada:** A4 contabiliza os campos monetários
preparados para carga, e não necessariamente cada chamada da função de
conversão.

### 5.7 Conclusão sobre o uso de IA

A IA contribuiu para esclarecer dúvidas, sugerir soluções pontuais e
investigar erros. Algumas sugestões foram adaptadas e outras rejeitadas
após avaliar sua necessidade e adequação. Executar os comandos, corrigir
problemas e validar resultados foi fundamental para compreender o ETL e
garantir a consistência dos dados.

## 6. Reflexão sobre o desenvolvimento

### 6.1 Qual foi a decisão mais difícil do ETL e por quê?

Minha maior dificuldade foi organizar o projeto e compreender como cada
etapa se conectava. Como ainda estou aprendendo, tive dúvidas sobre a
estrutura dos arquivos, a configuração do ambiente e a ordem das
atividades. Desenvolver aos poucos e testar cada etapa antes de avançar
me ajudou a compreender melhor o funcionamento do ETL.

### 6.2 O que você delegou à IA e o que fez questão de fazer sozinho?

Utilizei a IA para esclarecer dúvidas, entender requisitos e receber
orientações sobre a organização do projeto. Também pedi apoio em funções
específicas, testes e investigação de erros. Fiz questão de executar os
comandos, conferir os resultados e questionar sugestões que não faziam
sentido ou apresentavam problemas.

### 6.3 Se tivesse mais uma semana, o que mudaria primeiro?

Dedicaria mais tempo para compreender cada etapa e revisar o código,
identificando partes que poderiam ser simplificadas ou processos
desnecessários. Meu objetivo seria deixar o ETL mais organizado, fácil
de entender e manter, além de ampliar as validações e a documentação.

## 7. Considerações finais

Este desafio reforçou que Engenharia de Dados vai além de extrair,
transformar e carregar informações. É necessário compreender o negócio,
definir regras, validar resultados e garantir que os dados sejam
confiáveis.

A inteligência artificial foi uma ferramenta de apoio durante o
desenvolvimento, mas compreender o código, executar as validações e
assumir as decisões técnicas continuaram sendo minha responsabilidade.
