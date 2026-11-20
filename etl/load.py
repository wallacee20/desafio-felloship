
import os
import pandas as pd
import psycopg2

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import create_engine, URL, text
from dotenv import load_dotenv

# Carregando variáveis de ambiente.
load_dotenv()

# Configurações de conexão com PostgreSQL.

load_dotenv(override=True)

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME
)

engine = create_engine(connection_url)

with engine.connect() as connection:
    result = connection.execute(
        text("SELECT version(), current_database()")
    )

    print(result.fetchone())


# --------------------------------------------------
#  Configuração de caminhos dos arquivos CSV.
# --------------------------------------------------

#  Leitura dos arquivos tratados.
df_produtos = pd.read_csv("../dados-tratados/produtos.csv")
df_clientes = pd.read_csv("../dados-tratados/clientes.csv")
df_pedidos = pd.read_csv("../dados-tratados/pedidos.csv")
df_itens = pd.read_csv("../dados-tratados/itens_pedido.csv")

# Carga dos produtos.

def inserir_sem_duplicar(pd_table, conn, keys, data_iter):
    dados = [dict(zip(keys, row)) for row in data_iter]

    if not dados:
        return 0

    comando = insert(pd_table.table).values(dados)
    comando = comando.on_conflict_do_nothing()

    resultado = conn.execute(comando)

    return resultado.rowcount
# Carga dos produtos.

df_produtos.to_sql(
    "produtos",
    engine,
    if_exists="append",
    index=False,
    method=inserir_sem_duplicar
)

print(f"CARGA: produtos={len(df_produtos)}")


# Inserção dos clientes.
df_clientes.to_sql(
    "clientes",
    engine,
    if_exists="append",
    index=False,
    method=inserir_sem_duplicar
)

print(f"CARGA: clientes={len(df_clientes)}")

# 6. Inserção dos pedidos.
df_pedidos.to_sql(
    "pedidos",
    engine,
    if_exists="append",
    index=False,
    method=inserir_sem_duplicar
)

print(f"CARGA: pedidos={len(df_pedidos)}")

# 7. Inserção dos itens dos pedidos.
df_itens.to_sql(
    "itens_pedido",
    engine,
    if_exists="append",
    index=False,
    method=inserir_sem_duplicar,
    chunksize=500
)
print(f"CARGA: itens={len(df_itens)}")
