def executar_carga():
    
    import os
    import pandas as pd
    import psycopg2

    from sqlalchemy.dialects.postgresql import insert
    from sqlalchemy import create_engine, URL, text
    from dotenv import load_dotenv

    from pathlib import Path

    # Diretório raiz do projeto
    ROOT_DIR = Path(__file__).resolve().parents[1]

    # Diretório dos dados tratados
    DADOS_TRATADOS = ROOT_DIR / "dados-tratados"

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


# --------------------------------------------------
#  Configuração de caminhos dos arquivos CSV.
# --------------------------------------------------

    df_produtos = pd.read_csv(DADOS_TRATADOS / "produtos.csv")
    df_clientes = pd.read_csv(DADOS_TRATADOS / "clientes.csv")
    df_pedidos = pd.read_csv(DADOS_TRATADOS / "pedidos.csv")
    df_itens = pd.read_csv(DADOS_TRATADOS / "itens_pedido.csv")

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


    # Inserção dos clientes.
    df_clientes.to_sql(
        "clientes",
        engine,
        if_exists="append",
        index=False,
        method=inserir_sem_duplicar
    )

    # 6. Inserção dos pedidos.
    df_pedidos.to_sql(
        "pedidos",
        engine,
        if_exists="append",
        index=False,
        method=inserir_sem_duplicar
    )

    # 7. Inserção dos itens dos pedidos.
    df_itens.to_sql(
        "itens_pedido",
        engine,
        if_exists="append",
        index=False,
        method=inserir_sem_duplicar,
        chunksize=500
    )
    
    
    return {
        "produtos": len(df_produtos),
        "clientes": len(df_clientes),
        "pedidos": len(df_pedidos),
        "itens": len(df_itens)
    }