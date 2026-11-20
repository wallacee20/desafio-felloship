import pandas as pd
import json

# ---------------------------------------------------------------------------------------------- #
# ----------------- Leitura dos arquivos JSON e CSV na pasta dados-brutos. --------------------- #
# ---------------------------------------------------------------------------------------------- #

df_clientes = pd.read_json("../dados-brutos/clientes.json")
df_pedidos = pd.read_json("../dados-brutos/pedidos.json")
df_produtos = pd.read_csv("../insumos/dados/produtos.csv")

# ---------------------------------------------------------------------------------------------- #
# ----------------- Substituir valores nulos na coluna "email" por None. ----------------------- #
# ---------------------------------------------------------------------------------------------- #

df_clientes["email"] = df_clientes["email"].where(
    df_clientes["email"].notna(), None
)
email_nulos = df_clientes["email"].isna().sum() # Contando o número de emails nulos

# ---------------------------------------------------------------------------------------------- #
# ----------------- Padronizando a coluna "estado" para letras maiúsculas. --------------------- #
# ---------------------------------------------------------------------------------------------- #

estados_originais = df_clientes["estado"].copy() # Guarda os valores originais para contabilizar as alterações.


df_clientes["estado"] = (  # Remove espaços em branco e converte para maiúsculas.
    df_clientes["estado"]
    .astype("string")
    .str.strip()
    .str.upper()
)


estados_padronizados = (  # Conta quantos estados foram efetivamente padronizados.
    estados_originais.astype("string") != df_clientes["estado"] 
).sum()

# ---------------------------------------------------------------------------------------------- #
# ----------------- Convertendo a coluna "data_pedido" para datetime. -------------------------- #
# ---------------------------------------------------------------------------------------------- #


datas_originais = df_pedidos["data_pedido"].copy()  # guardando a coluna original para contagem de datas convertidas.


df_pedidos["data_pedido"] = pd.to_datetime( # Converte a coluna data_pedido para datetime.
    df_pedidos["data_pedido"],
    format="mixed",
    dayfirst=True
)


datas_convertidas = ( # Cria um avariavel para contar quantas datas foram convertidas.
    datas_originais.str.contains("/", na=False)
).sum()

# ---------------------------------------------------------------------------------------------- #
# ----------------- padronizando a coluna valor_total para float. ------------------------------ #
# ---------------------------------------------------------------------------------------------- #

df_pedidos["valor_total"] = pd.to_numeric(
    df_pedidos["valor_total"].astype(str).str.replace(",", ".", regex=False),
    errors="coerce"
).round(2)

# ---------------------------------------------------------------------------------------------- #
# ----------------- Removendo pedidos duplicados. ---------------------------------------------- #
# ---------------------------------------------------------------------------------------------- #

pedidos_unicos = df_pedidos.drop_duplicates(subset="id", keep="first")

# ---------------------------------------------------------------------------------------------- #
# ----------------- # Criando DataFrame de itens a partir do JSON aninhado. -------------------- #
# ---------------------------------------------------------------------------------------------- #

df_itens = pd.json_normalize( 
    pedidos_unicos.to_dict("records"), record_path="itens", meta=["id"]
).rename(columns={"id": "pedido_id"})

df_itens["linha"] = df_itens.groupby("pedido_id").cumcount() + 1 # Criando sequência dos itens.


# ---------------------------------------------------------------------------------------------- #
# ----------------- Calcular a soma na origem -------------------------------------------------- #
# ---------------------------------------------------------------------------------------------- #

df_itens_origem = df_itens.copy()   # Criando uma cópia do DataFrame de itens original.

 
df_itens_origem["subtotal"] = (     # Cria uma coluna calculada subtotal que é o resultado da multiplicação da quantidade pelo preço unitário.
    df_itens_origem["quantidade"] *
    df_itens_origem["preco_unitario"]
)
soma_valor_itens_origem = df_itens_origem["subtotal"].sum()   # Calcula a soma dos subtotais dos itens da origem.

# ---------------------------------------------------------------------------------------------- #
# ----------------- Calculo da soma na destino --------------------------------------------------#
# ---------------------------------------------------------------------------------------------- #

soma_valor_itens_destino = (     # Cria uma variavel que armazena a soma do valor dos itens no destino.
    df_itens["quantidade"] * df_itens["preco_unitario"]
).sum()

# ---------------------------------------------------------------------------------------------- #
# ----------------- Calcular a diferença ------------------------------------------------------- #
# ---------------------------------------------------------------------------------------------- #

diferenca = round(      # Calcula a diferença entre a soma dos itens da origem e a soma dos itens do destino.
    soma_valor_itens_origem - soma_valor_itens_destino,
    2
)

# ---------------------------------------------------------------------------------------------- #
# ----------------- contabilizar os registros descartados. ------------------------------------- #
# ---------------------------------------------------------------------------------------------- #

total_pedidos = len(df_pedidos)  # Quantidade de pedidos antes da remoção.


total_pedidos_unicos = len(pedidos_unicos)  # Quantidade de pedidos após a remoção.


repetidos_descartados = total_pedidos - total_pedidos_unicos # Quantidade de duplicados descartados.

# ---------------------------------------------------------------------------------------------- #
# ----------------- Removendo a coluna "itens" do DataFrame de pedidos. ------------------------ #
# ---------------------------------------------------------------------------------------------- #

pedidos_unicos = pedidos_unicos.drop(columns=["itens"])

# ---------------------------------------------------------------------------------------------- #
# ----------------- Calculando o total de cada item (quantidade * preço unitário). ------------- #
# ---------------------------------------------------------------------------------------------- #

df_itens_total = df_itens.copy() # DataFrame auxiliar para consolidação dos valores.

df_itens_total["total"] = (
    df_itens_total["quantidade"] *
    df_itens_total["preco_unitario"]
)

# ---------------------------------------------------------------------------------------------- #
# ----------------- Cria uma variavel que armazena o total de cada item agrupado por pedido_id.  #
# ---------------------------------------------------------------------------------------------- #

valor_itens = (
    df_itens_total.groupby("pedido_id")["total"]
    .sum()
    .round(2)
)

# ---------------------------------------------------------------------------------------------- #
# ----------------- Cria a coluna calculada valor_itens. --------------------------------------  #
# ---------------------------------------------------------------------------------------------- #

pedidos_unicos["valor_itens"] = (
    pedidos_unicos["id"].map(valor_itens)
)

# ---------------------------------------------------------------------------------------------- #
# ------ Identificando divergência entre o valor total do pedido e a soma dos valores dos itens. #
# ---------------------------------------------------------------------------------------------- #

pedidos_unicos["divergente"] = (
    pedidos_unicos["valor_total"].round(2) !=
    pedidos_unicos["valor_itens"].round(2)
)
divergentes = pedidos_unicos["divergente"].sum() # Contando o número de pedidos divergentes

# ---------------------------------------------------------------------------------------------- #
# ------- Escrevendo os DataFrames tratados em arquivos CSV na pasta dados-tratados. ---------   #  
# ---------------------------------------------------------------------------------------------- #

df_clientes.to_csv("../dados-tratados/clientes.csv", index=False, encoding="utf-8")
df_produtos.to_csv("../dados-tratados/produtos.csv", index=False, encoding="utf-8")
df_itens.to_csv("../dados-tratados/itens_pedido.csv", index=False, encoding="utf-8")
pedidos_unicos.to_csv("../dados-tratados/pedidos.csv", index=False, encoding="utf-8")

print(
    f"transformacao: pedidos_unicos={len(pedidos_unicos)} "
    f"transformacao: repetidos_descartados={repetidos_descartados}"
)

print(
    f"transformacao: emails_nulos={email_nulos} "
    f"transformacao: estados_padronizados={estados_padronizados} "
    f"transformacao: datas_convertidas={datas_convertidas} "
)

print(
    f"reconciliacao: "
    f"soma_valor_itens_origem={soma_valor_itens_origem:.2f} "
    f"soma_valor_itens_destino={soma_valor_itens_destino:.2f} "
    f"diferenca={diferenca:.2f} "
)

print(    
    f"divergentes: divergentes={divergentes} "
)

print(f"CLIENTES: {len(df_clientes)}")
print(f"PRODUTOS: {len(df_produtos)}")
print(f"ITENS: {len(df_itens)}")
print(f"PEDIDOS: {len(pedidos_unicos)}")