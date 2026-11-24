-- Total de vendas por mês
SELECT
    DATE_TRUNC('month', data_pedido) AS mes,
    SUM(valor_total) AS total_vendas
FROM pedidos
GROUP BY 1
ORDER BY 1;


-- Quantidade de pedidos por estado
SELECT
    c.estado,
    COUNT(p.id) AS quantidade_pedidos
FROM pedidos p
JOIN clientes c
    ON p.cliente_id = c.id
GROUP BY c.estado
ORDER BY quantidade_pedidos DESC;


-- Pedidos divergentes
SELECT
    p.id,
    p.valor_total,
    SUM(i.quantidade * i.preco_unitario) AS total_itens
FROM pedidos p
JOIN itens_pedido i
    ON p.id = i.pedido_id
GROUP BY p.id, p.valor_total
HAVING ABS(
    p.valor_total -
    SUM(i.quantidade * i.preco_unitario)
) > 0.01;


-- Total geral de vendas
SELECT
    SUM(valor_total) AS total_geral
FROM pedidos;


-- reconciliação
WITH vendas_mensais AS (
    SELECT
        DATE_TRUNC('month', data_pedido) AS mes,
        SUM(valor_total) AS total_vendas
    FROM pedidos
    GROUP BY 1
)
SELECT
    ROUND(SUM(total_vendas)::numeric, 2) AS soma_mensal,
    ROUND(
        (SELECT SUM(valor_total) FROM pedidos)::numeric,
        2
    ) AS total_geral,
    ROUND(
        (SUM(total_vendas) -
        (SELECT SUM(valor_total) FROM pedidos))::numeric,
        2
    ) AS diferenca,
    ABS(
        SUM(total_vendas) -
        (SELECT SUM(valor_total) FROM pedidos)
    ) <= 0.01 AS reconciliacao_aprovada
FROM vendas_mensais;