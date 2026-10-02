"""
amazon_sync.py — busca imagem e preco dos produtos na Creators API da Amazon.

Uso:  python3 amazon_sync.py            (le amazon_asins.json, gerado pelo build.py)
      python3 amazon_sync.py --dry-run  (so mostra quantos ASINs e lotes seriam pedidos)

Grava amazon_live.json SOMENTE se a API respondeu. Se a conta nao estiver elegivel
(AssociateNotEligible) ou qualquer outra falha, o arquivo antigo fica intacto e o build.py
ignora dados com mais de 24h — o site volta sozinho ao visual sem imagem.

Regras da Amazon que este arquivo respeita:
- dados da API (imagem, preco) nao podem ser usados com mais de 24h -> fetched_at + corte no build
- imagem e usada pela URL da propria Amazon (sem baixar/re-hospedar)
- credenciais vem do .env e nunca sao impressas
"""
import json, os, sys, time, datetime
import requests

BASE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(BASE, "amazon_asins.json")
OUTFILE = os.path.join(BASE, "amazon_live.json")
API = "https://creatorsapi.amazon/catalog/v1/getItems"
TOKEN_URLS = {"2.1": "https://creatorsapi.auth.us-east-1.amazoncognito.com/oauth2/token",
              "2.2": "https://creatorsapi.auth.eu-south-2.amazoncognito.com/oauth2/token",
              "2.3": "https://creatorsapi.auth.us-west-2.amazoncognito.com/oauth2/token",
              "3.1": "https://api.amazon.com/auth/o2/token",
              "3.2": "https://api.amazon.co.uk/auth/o2/token",
              "3.3": "https://api.amazon.co.jp/auth/o2/token"}
RESOURCES_BASE = ["images.primary.large", "offersV2.listings.price",
                  "offersV2.listings.availability", "offersV2.listings.isBuyBoxWinner"]
# fotos extras do anuncio (carrossel do site). Se a API recusar este recurso (HTTP 400),
# o robo refaz SEM ele: o site nunca perde a foto principal por causa do carrossel.
RESOURCES = RESOURCES_BASE + ["images.variants.large"]
GALLERY_MAX = 8


def read_env():
    env = {}
    p = os.path.join(BASE, ".env")
    if os.path.exists(p):
        for l in open(p, encoding="utf-8"):
            l = l.strip()
            if l and not l.startswith("#") and "=" in l:
                k, v = l.split("=", 1)
                env[k.strip()] = v.strip()
    for k in list(env) + [k for k in os.environ if k.startswith("CREATORS_")]:
        if k in os.environ:          # variavel de ambiente (ex.: GitHub Actions) tem prioridade
            env[k] = os.environ[k]
    return env


def get_token(env):
    ver = env["CREATORS_VERSION"]
    d = {"grant_type": "client_credentials", "client_id": env["CREATORS_CREDENTIAL_ID"],
         "client_secret": env["CREATORS_SECRET"]}
    if ver.startswith("3."):
        d["scope"] = "creatorsapi::default"
        r = requests.post(TOKEN_URLS[ver], json=d, timeout=30)
    else:
        d["scope"] = "creatorsapi/default"
        r = requests.post(TOKEN_URLS[ver], data=d, timeout=30)
    if r.status_code != 200:
        raise SystemExit(f"ERRO no login da Creators API (HTTP {r.status_code}). Credenciais erradas ou revogadas?")
    tok = r.json()["access_token"]
    return f"Bearer {tok}" if ver.startswith("3.") else f"Bearer {tok}, Version {ver}"


def pick_listing(listings):
    if not listings:
        return None
    for l in listings:
        if l.get("isBuyBoxWinner"):
            return l
    return listings[0]


def parse_item(it):
    out = {}
    img = (((it.get("images") or {}).get("primary") or {}).get("large") or {})
    if img.get("url"):
        out["image"] = img["url"]
        out["w"], out["h"] = img.get("width"), img.get("height")
        gal = [img["url"]]
        for v in ((it.get("images") or {}).get("variants") or []):
            u = ((v or {}).get("large") or {}).get("url")
            if u and u not in gal:
                gal.append(u)
        if len(gal) > 1:
            out["gallery"] = gal[:GALLERY_MAX]
    l = pick_listing(((it.get("offersV2") or {}).get("listings")) or [])
    money = (((l or {}).get("price") or {}).get("money") or {})
    if money.get("amount") is not None and (money.get("currency") or "EUR") == "EUR":
        out["price"] = float(money["amount"])
        out["currency"] = "EUR"
    av = ((l or {}).get("availability") or {}).get("type")
    if av:
        out["availability"] = av
    return out


def main():
    dry = "--dry-run" in sys.argv
    if not os.path.exists(MANIFEST):
        raise SystemExit("amazon_asins.json nao existe: rode o build.py uma vez antes.")
    asins = sorted(json.load(open(MANIFEST, encoding="utf-8")).keys())
    batches = [asins[i:i + 10] for i in range(0, len(asins), 10)]
    print(f"{len(asins)} ASINs em {len(batches)} lotes de ate 10")
    if dry:
        return
    env = read_env()
    for k in ("CREATORS_CREDENTIAL_ID", "CREATORS_SECRET", "CREATORS_VERSION", "CREATORS_PARTNER_TAG"):
        if not env.get(k):
            raise SystemExit(f"Falta {k} no .env")
    mk = env.get("CREATORS_MARKETPLACE") or "www.amazon.ie"
    auth = get_token(env)
    items, missing = {}, []
    resources = list(RESOURCES)
    for n, b in enumerate(batches, 1):
        def ask(res):
            body = {"itemIds": b, "itemIdType": "ASIN", "marketplace": mk,
                    "partnerTag": env["CREATORS_PARTNER_TAG"], "resources": res}
            for attempt in range(4):
                rr = requests.post(API, json=body, timeout=30, headers={
                    "Authorization": auth, "Content-Type": "application/json", "x-marketplace": mk})
                if rr.status_code == 429:       # limite de taxa: espera e tenta de novo
                    time.sleep(2 * (attempt + 1)); continue
                return rr
            return rr
        r = ask(resources)
        if r.status_code == 400 and resources != RESOURCES_BASE:
            print("! API recusou as fotos extras (HTTP 400): seguindo so com a foto principal.")
            resources = list(RESOURCES_BASE)
            r = ask(resources)
        try:
            data = r.json()
        except ValueError:
            data = {}
        if r.status_code == 403 and data.get("reason") == "AssociateNotEligible":
            print("NAO ELEGIVEL: a Amazon ainda nao liberou a API (regra: 10 vendas ENVIADAS em 30 dias).")
            print("Nada foi alterado; o site continua sem imagem ate liberar.")
            sys.exit(2)
        if r.status_code != 200:
            print(f"ERRO no lote {n}: HTTP {r.status_code} {data.get('reason') or ''}. Nada foi gravado.")
            sys.exit(1)
        for it in ((data.get("itemsResult") or {}).get("items")) or []:
            parsed = parse_item(it)
            if parsed:
                items[it["asin"]] = parsed
        for e in data.get("errors") or []:
            missing.append(e.get("message") or e.get("code") or str(e))
        time.sleep(1.1)                        # ~1 pedido por segundo
    if not items:
        print("A API respondeu mas sem nenhum item aproveitavel. Nada foi gravado.")
        sys.exit(1)
    now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    payload = {"fetched_at": now.isoformat(), "marketplace": mk, "items": items}
    tmp = OUTFILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=1, sort_keys=True)
    os.replace(tmp, OUTFILE)
    n_img = sum(1 for v in items.values() if v.get("image"))
    n_pr = sum(1 for v in items.values() if v.get("price") is not None)
    n_gal = sum(1 for v in items.values() if v.get("gallery"))
    print(f"OK: {len(items)}/{len(asins)} ASINs | {n_img} com imagem | {n_gal} com carrossel | "
          f"{n_pr} com preco | {len(missing)} com erro")
    for m in missing[:15]:
        print("  -", m)
    # relatorio para o resumo da execucao no GitHub: ASIN que a Amazon nao devolveu, ou que
    # voltou sem foto/preco/estoque = candidato a troca de produto. Le-se na pagina da execucao.
    manifest = json.load(open(MANIFEST, encoding="utf-8"))
    falhas = []
    for a in asins:
        v = items.get(a)
        if not v:
            motivo = "nao devolvido pela Amazon (anuncio removido ou ASIN errado)"
        elif not v.get("image"):
            motivo = "sem foto"
        elif v.get("price") is None:
            motivo = "sem preco (provavelmente sem estoque)"
        elif v.get("availability") and v["availability"] not in ("IN_STOCK", "IN_STOCK_SCARCE", "AVAILABLE_DATE", "PREORDER"):
            motivo = f"disponibilidade {v['availability']}"
        else:
            continue
        falhas.append(f"{a} ({', '.join(manifest.get(a, []))}): {motivo}")
    summ = os.environ.get("GITHUB_STEP_SUMMARY")
    if summ:
        with open(summ, "a", encoding="utf-8") as f:
            f.write(f"### Amazon: {len(items)}/{len(asins)} ASINs, {n_img} com foto, {n_gal} com carrossel\n\n")
            if falhas:
                f.write("**Produtos para revisar:**\n\n" + "\n".join(f"- {x}" for x in falhas) + "\n")
            else:
                f.write("Nenhum produto com problema.\n")
    for x in falhas:
        print("  REVISAR:", x)


if __name__ == "__main__":
    main()
