#!/usr/bin/env python3
"""
Envia ao IndexNow as URLs que mudaram neste deploy.

Por que existe: o IndexNow avisa Bing e Yandex no instante em que uma pagina muda,
em vez de esperar o rastreamento espontaneo. O indice do Bing alimenta o ChatGPT
Search e o Copilot — que, pelo GA4 de agosto/2026, sao a maior fonte de trafego
do PickIreland. Avisar rapido vale mais aqui do que no Google.

A chave NAO e segredo: o protocolo exige que ela fique publica em
https://pickireland.best/<chave>.txt. E esse arquivo que prova posse do dominio.
Por isso este script nao precisa de nenhuma credencial.

Uso:
    python3 indexnow_submit.py --changed docs/a.html docs/b.html
    python3 indexnow_submit.py --all                 # todas as URLs do sitemap
    python3 indexnow_submit.py --all --dry-run       # so mostra o que enviaria
"""
import argparse, json, os, re, sys, urllib.error, urllib.request

BASE   = os.path.dirname(os.path.abspath(__file__))
DOCS   = os.path.join(BASE, "..", "docs")
HOST   = "pickireland.best"
DOMAIN = f"https://{HOST}"
ENDPOINT = "https://api.indexnow.org/indexnow"
MAX_URLS = 10000          # limite do protocolo por requisicao


def find_key():
    """A chave e o proprio nome do arquivo publicado em docs/ — nao lemos o .env aqui,
    porque o que vale para o buscador e o que esta publicado no site."""
    for name in sorted(os.listdir(DOCS)):
        if re.fullmatch(r"[a-f0-9]{32}\.txt", name):
            key = name[:-4]
            body = open(os.path.join(DOCS, name), encoding="utf-8").read().strip()
            if body != key:
                sys.exit(f"ERRO: {name} deveria conter exatamente '{key}', contem '{body[:40]}'")
            return key
    sys.exit("ERRO: nenhum arquivo de chave IndexNow em docs/. Rode build.py primeiro.")


def path_to_url(p):
    """docs/foo/bar.html -> https://pickireland.best/foo/bar.html
       docs/index.html   -> https://pickireland.best/          (igual ao sitemap)"""
    rel = p.replace("\\", "/")
    rel = rel[rel.index("docs/") + 5:] if "docs/" in rel else rel.lstrip("/")
    if rel == "index.html":
        return f"{DOMAIN}/"
    if rel.endswith("/index.html"):
        # hub de categoria: a canonica e o diretorio, sem "index.html"
        return f"{DOMAIN}/{rel[:-len('index.html')]}"
    return f"{DOMAIN}/{rel}"


def urls_from_sitemap():
    sm = os.path.join(DOCS, "sitemap.xml")
    if not os.path.exists(sm):
        sys.exit("ERRO: docs/sitemap.xml nao encontrado.")
    return re.findall(r"<loc>([^<]+)</loc>", open(sm, encoding="utf-8").read())


def submit(urls, key, dry_run=False):
    payload = {
        "host": HOST,
        "key": key,
        "keyLocation": f"{DOMAIN}/{key}.txt",
        "urlList": urls[:MAX_URLS],
    }
    if dry_run:
        print(f"[dry-run] POST {ENDPOINT}")
        print(f"[dry-run] host={HOST} keyLocation={payload['keyLocation']}")
        print(f"[dry-run] {len(payload['urlList'])} URLs:")
        for u in payload["urlList"]:
            print(f"          {u}")
        return 0

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT, data=data, method="POST",
        headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"IndexNow: HTTP {r.status} — {len(payload['urlList'])} URLs enviadas")
            return 0
    except urllib.error.HTTPError as e:
        detail = {
            400: "requisicao invalida (JSON malformado)",
            403: "chave invalida ou nao encontrada em keyLocation",
            422: "as URLs nao pertencem ao host declarado",
            429: "requisicoes demais — tente mais tarde",
        }.get(e.code, "")
        print(f"IndexNow: HTTP {e.code} {detail}", file=sys.stderr)
        # 429 nao e falha de deploy; nao derruba o pipeline
        return 0 if e.code == 429 else 1
    except Exception as e:
        print(f"IndexNow: falha de rede ({type(e).__name__}: {e})", file=sys.stderr)
        return 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--changed", nargs="*", default=None,
                    help="caminhos alterados (ex: docs/foo/bar.html)")
    ap.add_argument("--all", action="store_true", help="enviar todas as URLs do sitemap")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if a.all:
        urls = urls_from_sitemap()
    elif a.changed is not None:
        html = [p for p in a.changed if p.strip().endswith(".html")]
        urls = sorted({path_to_url(p) for p in html})
    else:
        ap.error("use --changed ou --all")

    if not urls:
        print("IndexNow: nenhuma pagina HTML mudou — nada a enviar.")
        return 0

    key = find_key()
    return submit(urls, key, a.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
