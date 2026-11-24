import logging
from pathlib import Path

import pandas as pd


# Diretório raiz do projeto
ROOT_DIR = Path(__file__).resolve().parents[1]

# Diretórios de entrada e saída
DADOS_BRUTOS = ROOT_DIR / "dados-brutos"
DADOS_TRATADOS = ROOT_DIR / "dados-tratados"
INSUMOS_DADOS = ROOT_DIR / "insumos" / "dados"

#  ============================================================================================= #
#  ============= Funções de Transformação. ===================================================== #
#  ============================================================================================= #

def tratar_email(cliente):  # Trata e-mails nulos dos clientes.
        cliente = cliente.copy()
        if pd.isna(cliente["email"]):
            cliente["email"] = None
        return cliente

def padronizar_estado(cliente):  # Padroniza os estados, removendo espaços e convertendo para maiúsculas.
    cliente = cliente.copy()

    cliente["estado"] = (
        str(cliente["estado"]).strip().upper()
    )

    return cliente

def converter_valor(valor):  # Converte valores monetários para números com duas casas decimais.
    valor_convertido = pd.to_numeric(
        str(valor).replace(",", "."),
        errors="coerce"
    )

    return round(valor_convertido, 2) if pd.notna(valor_convertido) else float("nan")

def converter_data(valor):  # Converte valores para o formato de data.
    return pd.to_datetime(
        valor,
        format="mixed",
        dayfirst=True,
        errors="coerce"
    )

def remover_pedidos_duplicados(df_pedidos):   # Remove pedidos duplicados, mantendo a primeira ocorrência.

    pedidos_unicos = df_pedidos.drop_duplicates(
        subset="id",
        keep="first"
    ).copy()

    repetidos_descartados = (
        len(df_pedidos) - len(pedidos_unicos)
    )

    return pedidos_unicos, repetidos_descartados

#  ============================================================================================= #
#  ============= Leitura dos arquivos JSON e CSV na pasta dados-brutos. ======================== #
#  ============================================================================================= #

def executar_transformacao():

    logging.info("Iniciando transformação dos dados")

    df_clientes = pd.read_json(
        DADOS_BRUTOS / "clientes.json"
    )

    df_pedidos = pd.read_json(
        DADOS_BRUTOS / "pedidos.json"
    )

    df_produtos = pd.read_csv(
        INSUMOS_DADOS / "produtos.csv"
    )

#  ============================================================================================= #
#  ============= TRATAMENTO DE E-MAILS NULOS 
#  ============================================================================================= #

    df_clientes = df_clientes.apply(tratar_email, axis=1)
    email_nulos = int(df_clientes["email"].isna().sum())

#  ============================================================================================= #
    # 3. PADRONIZAÇÃO DOS ESTADOS
#  ============================================================================================= #

    estados_originais = df_clientes["estado"].copy()

    df_clientes = df_clientes.apply(
        padronizar_estado,
        axis=1
    )

    estados_padronizados = int(
        (
            estados_originais.astype("string")
            != df_clientes["estado"].astype("string")
        ).sum()
    )

#  ============================================================================================= #
    # 4. CONVERSÃO DAS DATAS
#  ============================================================================================= #

    df_pedidos["data_pedido"] = (
    df_pedidos["data_pedido"]
    .apply(converter_data)
    )

    datas_convertidas = int(
    df_pedidos["data_pedido"].notna().sum()
)

#  ============================================================================================= #
    # 5. CONVERSÃO DOS VALORES MONETÁRIOS
#  ============================================================================================= #

    df_pedidos["valor_total"] = (
    df_pedidos["valor_total"]
    .apply(converter_valor)
    )

#  ============================================================================================= #
    # 6. REMOÇÃO DE PEDIDOS DUPLICADOS
#  ============================================================================================= #

    pedidos_unicos, repetidos_descartados = (
    remover_pedidos_duplicados(df_pedidos)
    )

    total_pedidos = len(df_pedidos)
    total_pedidos_unicos = len(pedidos_unicos)

    repetidos_descartados = (
        total_pedidos - total_pedidos_unicos
    )

#  ============================================================================================= #
    # 7. NORMALIZAÇÃO DOS ITENS DOS PEDIDOS
#  ============================================================================================= #

    df_itens = pd.json_normalize(
        pedidos_unicos.to_dict("records"),
        record_path="itens",
        meta=["id"]
    ).rename(
        columns={"id": "pedido_id"}
    )

    df_itens["linha"] = (
        df_itens.groupby("pedido_id").cumcount() + 1
    )

#  ============================================================================================= #
    # 8. RECONCILIAÇÃO DOS VALORES DOS ITENS
#  ============================================================================================= #

    df_itens_origem = df_itens.copy()

    df_itens_origem["subtotal"] = (
        df_itens_origem["quantidade"]
        * df_itens_origem["preco_unitario"]
    )

    soma_valor_itens_origem = (
        df_itens_origem["subtotal"].sum()
    )

    soma_valor_itens_destino = (
        df_itens["quantidade"]
        * df_itens["preco_unitario"]
    ).sum()

    diferenca = round(
        soma_valor_itens_origem - soma_valor_itens_destino,
        2
    )
    
    reconciliacao_aprovada = bool(abs(diferenca) <= 0.01)

#  ============================================================================================= #
    # 9. CÁLCULO DO TOTAL DOS ITENS POR PEDIDO
#  ============================================================================================= #

    pedidos_unicos = pedidos_unicos.drop(
        columns=["itens"]
    )

    df_itens_total = df_itens.copy()

    df_itens_total["total"] = (
        df_itens_total["quantidade"]
        * df_itens_total["preco_unitario"]
    )

    valor_itens = (
        df_itens_total.groupby("pedido_id")["total"]
        .sum()
        .round(2)
    )

    pedidos_unicos["valor_itens"] = (
        pedidos_unicos["id"].map(valor_itens)
    )

#  ============================================================================================= #
    # 10. IDENTIFICAÇÃO DE PEDIDOS DIVERGENTES
#  ============================================================================================= #

    pedidos_unicos["divergente"] = (
        pedidos_unicos["valor_total"].round(2)
        != pedidos_unicos["valor_itens"].round(2)
    )

    divergentes = int(
        pedidos_unicos["divergente"].sum()
    )

#  ============================================================================================= #
    # 11. GRAVAÇÃO DOS DADOS TRATADOS
#  ============================================================================================= #

    DADOS_TRATADOS.mkdir(
        parents=True,
        exist_ok=True
    )

    df_clientes.to_csv(
        DADOS_TRATADOS / "clientes.csv",
        index=False,
        encoding="utf-8"
    )

    df_produtos.to_csv(
        DADOS_TRATADOS / "produtos.csv",
        index=False,
        encoding="utf-8"
    )

    df_itens.to_csv(
        DADOS_TRATADOS / "itens_pedido.csv",
        index=False,
        encoding="utf-8"
    )

    pedidos_unicos.to_csv(
        DADOS_TRATADOS / "pedidos.csv",
        index=False,
        encoding="utf-8"
    )

#  ============================================================================================= #
    # 12. RETORNO DAS MÉTRICAS DA TRANSFORMAÇÃO
#  ============================================================================================= #

    resultado = {
        "clientes": len(df_clientes),
        "produtos": len(df_produtos),
        "itens": len(df_itens),
        "pedidos": len(pedidos_unicos),
        "emails_nulos": email_nulos,
        "estados_padronizados": estados_padronizados,
        "datas_convertidas": datas_convertidas,
        "repetidos_descartados": repetidos_descartados,
        "divergentes": divergentes,
        "soma_valor_itens_origem": round(
            float(soma_valor_itens_origem), 2
        ),
        "soma_valor_itens_destino": round(
            float(soma_valor_itens_destino), 2
        ),
        "diferenca": round(float(diferenca), 2)
        ,
        "reconciliacao_aprovada": reconciliacao_aprovada
    }
    return resultado


