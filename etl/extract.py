import requests
import json

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DADOS_BRUTOS = ROOT_DIR / "dados-brutos"

api_url = "http://127.0.0.1:8000"

#
def buscar_pagina(endpoint: str, page: int, page_size: int) -> dict:
    try:
        resp = requests.get(
            f"{api_url}/{endpoint}",
            params={"page": page, "page_size": page_size},
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.ConnectionError:
        print("Erro: não foi possível conectar à API.")

    except requests.exceptions.Timeout:
        print("Erro: tempo limite de conexão excedido.")

    except requests.exceptions.HTTPError as erro:
        print(f"Erro HTTP: {erro}")

#
def extrair_paginado(endpoint: str, page_size: int = 200) -> tuple[list[dict], int]:
    primeira = buscar_pagina(endpoint, 1, page_size)
    
    if primeira is None:
        return [], 0
    
    itens = list(primeira["items"])
    total_paginas = primeira["total_pages"]
    for page in range(2, total_paginas + 1):
        pagina = buscar_pagina(endpoint, page, page_size)
        
        if pagina is None:
            return [], 0
        
        itens.extend(pagina["items"])
    return itens, total_paginas


def executar_extracao():

    clientes, paginas_clientes = extrair_paginado("clientes")
    pedidos, paginas_pedidos = extrair_paginado("pedidos")

    DADOS_BRUTOS.mkdir(parents=True, exist_ok=True)

    # Escrita dos dados extraídos em arquivos JSON na pasta dados-brutos.
    with open(DADOS_BRUTOS / "clientes.json", "w", encoding="utf-8") as f:
        json.dump(clientes, f, ensure_ascii=False)
    
    with open(DADOS_BRUTOS / "pedidos.json", "w", encoding="utf-8") as f:
        json.dump(pedidos, f, ensure_ascii=False)

    return {    
         "clientes": len(clientes),
         "pedidos": len(pedidos),
         "paginas_clientes": paginas_clientes,
         "paginas_pedidos": paginas_pedidos
         }