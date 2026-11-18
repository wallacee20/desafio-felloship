# -*- coding: utf-8 -*-
"""API HTTP local e sintetica da Verdejar (empresa ficticia) para o Desafio Final do Bootcamp.
Uso: python3 api_verdejar.py [--porta 8000] [--dados dados]
Rotas (JSON):
  GET /clientes?page=N&page_size=50
  GET /pedidos?page=N&page_size=50
  GET /saude
Resposta: {"page": N, "page_size": S, "total_items": T, "total_pages": P, "items": [...]}
Paginas fora do intervalo retornam 404. Apenas biblioteca padrao; nao usar em producao.
"""
import argparse, json, os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

DADOS = {}

class Handler(BaseHTTPRequestHandler):
    def _json(self, code, obj):
        corpo = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def do_GET(self):
        u = urlparse(self.path)
        rota = u.path.strip("/")
        if rota == "saude":
            return self._json(200, {"status": "ok"})
        if rota not in DADOS:
            return self._json(404, {"erro": "rota inexistente", "rotas": ["/clientes", "/pedidos", "/saude"]})
        q = parse_qs(u.query)
        try:
            page = int(q.get("page", ["1"])[0]); size = int(q.get("page_size", ["50"])[0])
        except ValueError:
            return self._json(400, {"erro": "page e page_size devem ser inteiros"})
        if page < 1 or size < 1 or size > 200:
            return self._json(400, {"erro": "page maior ou igual a 1; page_size entre 1 e 200"})
        itens = DADOS[rota]
        total = len(itens); paginas = (total + size - 1) // size
        if page > paginas:
            return self._json(404, {"erro": "pagina inexistente", "total_pages": paginas})
        ini = (page - 1) * size
        self._json(200, {"page": page, "page_size": size, "total_items": total, "total_pages": paginas,
                         "items": itens[ini:ini + size]})

    def log_message(self, fmt, *args):
        print("%s %s" % (self.address_string(), fmt % args))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--porta", type=int, default=8000)
    ap.add_argument("--dados", default="dados")
    a = ap.parse_args()
    for nome in ("clientes", "pedidos"):
        with open(os.path.join(a.dados, f"{nome}.json"), encoding="utf-8") as f:
            DADOS[nome] = json.load(f)
    print(f"API Verdejar em http://127.0.0.1:{a.porta}  (clientes={len(DADOS['clientes'])}, pedidos={len(DADOS['pedidos'])})")
    HTTPServer(("127.0.0.1", a.porta), Handler).serve_forever()

if __name__ == "__main__":
    main()
