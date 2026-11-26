# -*- coding: utf-8 -*-
"""Gera os dados sinteticos da Verdejar (empresa ficticia) para o Desafio Final do Bootcamp.
Uso: python3 gerar_dados.py [--seed 2026] [--clientes 1000] [--pedidos 5000]
Saida: dados/clientes.json, dados/pedidos.json, dados/produtos.csv
Apenas biblioteca padrao. Determinístico para a mesma seed.
Armadilhas declaradas (ver o documento do desafio, secao Contexto):
 A1 e-mails ausentes (null) em parte dos clientes;
 A2 sigla do estado em caixa alta e caixa baixa;
 A3 datas de pedido em dois formatos (AAAA-MM-DD e DD/MM/AAAA);
 A4 valor_total ora numero, ora texto com virgula decimal;
 A5 pedidos repetidos (mesmo id) entre paginas da API;
 A6 valor_total divergente da soma dos itens em parte dos pedidos.
"""
import argparse, csv, json, os, random

NOMES = ["Ana", "Bruno", "Carla", "Diego", "Elisa", "Fabio", "Gabriela", "Heitor", "Iara", "Joao",
         "Karen", "Lucas", "Marina", "Nelson", "Olivia", "Paulo", "Quezia", "Rafael", "Sofia", "Tiago",
         "Ursula", "Vitor", "Wagner", "Ximena", "Yara", "Zeca"]
SOBRENOMES = ["Silva", "Souza", "Oliveira", "Pereira", "Costa", "Rodrigues", "Almeida", "Nascimento",
              "Lima", "Araujo", "Fernandes", "Carvalho", "Gomes", "Martins", "Rocha", "Ribeiro"]
CIDADES = [("Porto Alegre", "RS"), ("Caxias do Sul", "RS"), ("Passo Fundo", "RS"), ("Florianopolis", "SC"),
           ("Joinville", "SC"), ("Curitiba", "PR"), ("Londrina", "PR"), ("Sao Paulo", "SP"),
           ("Campinas", "SP"), ("Belo Horizonte", "MG")]
PRODUTOS = [  # (id, nome, categoria, preco_base)
    (1, "Alface crespa", "folhas", 3.50), (2, "Rucula", "folhas", 4.20), (3, "Tomate italiano", "legumes", 8.90),
    (4, "Cenoura", "legumes", 5.40), (5, "Batata inglesa", "legumes", 6.80), (6, "Banana prata", "frutas", 7.30),
    (7, "Maca fuji", "frutas", 9.90), (8, "Laranja pera", "frutas", 5.10), (9, "Morango", "frutas", 14.50),
    (10, "Abobora cabotia", "legumes", 4.70), (11, "Couve manteiga", "folhas", 3.90), (12, "Uva niagara", "frutas", 12.00),
]
STATUS = ["entregue", "entregue", "entregue", "cancelado", "em_transporte"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--clientes", type=int, default=1000)
    ap.add_argument("--pedidos", type=int, default=5000)
    ap.add_argument("--saida", default="dados")
    a = ap.parse_args()
    rnd = random.Random(a.seed)
    os.makedirs(a.saida, exist_ok=True)

    clientes = []
    for i in range(1, a.clientes + 1):
        nome = f"{rnd.choice(NOMES)} {rnd.choice(SOBRENOMES)}"
        cidade, uf = rnd.choice(CIDADES)
        email = None if rnd.random() < 0.08 else f"{nome.lower().replace(' ', '.')}{i}@exemplo.com"   # A1
        uf_saida = uf.lower() if rnd.random() < 0.15 else uf                                            # A2
        dia = rnd.randint(1, 28); mes = rnd.randint(1, 12); ano = rnd.choice([2024, 2025])
        clientes.append({"id": i, "nome": nome, "email": email, "cidade": cidade, "estado": uf_saida,
                         "cadastro_em": f"{ano:04d}-{mes:02d}-{dia:02d}"})

    pedidos = []
    for pid in range(1, a.pedidos + 1):
        cid = rnd.randint(1, a.clientes)
        ano = 2026; mes = rnd.randint(1, 10); dia = rnd.randint(1, 28)
        data = f"{dia:02d}/{mes:02d}/{ano}" if rnd.random() < 0.20 else f"{ano}-{mes:02d}-{dia:02d}"   # A3
        itens = []
        for _ in range(rnd.randint(1, 4)):
            p = rnd.choice(PRODUTOS)
            q = rnd.randint(1, 6)
            preco = round(p[3] * rnd.uniform(0.9, 1.1), 2)
            itens.append({"produto_id": p[0], "quantidade": q, "preco_unitario": preco})
        total = round(sum(it["quantidade"] * it["preco_unitario"] for it in itens), 2)
        if rnd.random() < 0.05:                                                                         # A6
            total = round(total + rnd.choice([-5.0, 3.0, 10.0]), 2)
        valor = f"{total:.2f}".replace(".", ",") if rnd.random() < 0.25 else total                       # A4
        pedidos.append({"id": pid, "cliente_id": cid, "data_pedido": data, "status": rnd.choice(STATUS),
                        "valor_total": valor, "itens": itens})
    # A5: repete 2% dos pedidos (mesmo id e conteudo), inseridos em posicoes aleatorias
    repetidos = rnd.sample(pedidos, max(1, int(0.02 * len(pedidos))))
    for r in repetidos:
        pedidos.insert(rnd.randint(0, len(pedidos)), dict(r))

    with open(os.path.join(a.saida, "clientes.json"), "w", encoding="utf-8") as f:
        json.dump(clientes, f, ensure_ascii=False, indent=1)
    with open(os.path.join(a.saida, "pedidos.json"), "w", encoding="utf-8") as f:
        json.dump(pedidos, f, ensure_ascii=False, indent=1)
    with open(os.path.join(a.saida, "produtos.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["produto_id", "nome", "categoria", "preco_base"])
        for p in PRODUTOS:
            w.writerow(p)
    print(f"seed={a.seed} clientes={len(clientes)} pedidos_na_api={len(pedidos)} (com {len(repetidos)} repetidos) produtos={len(PRODUTOS)}")

if __name__ == "__main__":
    main()
