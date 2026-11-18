-- Esquema de destino do Desafio Final do Bootcamp (Verdejar, empresa ficticia).
-- Banco: PostgreSQL. Executar uma vez antes da carga. Ajustes sao permitidos se documentados no README do Fellow.
CREATE TABLE IF NOT EXISTS clientes (
    id            INTEGER PRIMARY KEY,
    nome          TEXT NOT NULL,
    email         TEXT,
    cidade        TEXT NOT NULL,
    estado        CHAR(2) NOT NULL,
    cadastro_em   DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS produtos (
    produto_id    INTEGER PRIMARY KEY,
    nome          TEXT NOT NULL,
    categoria     TEXT NOT NULL,
    preco_base    NUMERIC(10,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS pedidos (
    id            INTEGER PRIMARY KEY,
    cliente_id    INTEGER NOT NULL REFERENCES clientes(id),
    data_pedido   DATE NOT NULL,
    status        TEXT NOT NULL,
    valor_total   NUMERIC(12,2) NOT NULL,
    valor_itens   NUMERIC(12,2) NOT NULL,
    divergente    BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS itens_pedido (
    pedido_id       INTEGER NOT NULL REFERENCES pedidos(id),
    linha           INTEGER NOT NULL,
    produto_id      INTEGER NOT NULL REFERENCES produtos(produto_id),
    quantidade      INTEGER NOT NULL,
    preco_unitario  NUMERIC(10,2) NOT NULL,
    PRIMARY KEY (pedido_id, linha)
);
