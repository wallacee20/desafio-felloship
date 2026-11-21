import pandas as pd

from etl.transform import converter_valor
from etl.transform import remover_pedidos_duplicados
from etl.transform import converter_data



# Define a função de teste para verificar se o valor com vírgula é convertido corretamente para número
def test_valor_com_virgula_vira_numero():
    assert converter_valor("125,84") == 125.84

# Define a função de teste para verificar se o valor numérico permanece inalterado
def test_valor_numerico_permanece():
    assert converter_valor(94.34) == 94.34


# Define a função de teste para converter datas no formato ISO
def test_data_iso():
    resultado = converter_data("2024-03-15")

    assert resultado.strftime("%Y-%m-%d") == "2024-03-15"

# Define a função de teste para converter datas no formato brasileiro
def test_data_formato_brasileiro():
    resultado = converter_data("15/03/2024")

    assert resultado.strftime("%Y-%m-%d") == "2024-03-15"


# Define a função de teste para remover pedidos duplicados
def test_remover_pedidos_repetidos():

    df = pd.DataFrame({
        "id": [1001, 1002, 1001],
        "cliente": ["João", "Maria", "João"],
        "valor_total": [250.00, 180.00, 250.00]
    })

    resultado, descartados = remover_pedidos_duplicados(df)

    assert len(resultado) == 2
    assert resultado["id"].tolist() == [1001, 1002]
    assert descartados == 1