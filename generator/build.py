# -*- coding: utf-8 -*-
"""
PickIreland site generator v2 (Trust & Authority design system).
Usage:  python build.py
Reads:  data/*.json  +  affiliate_links.xlsx
Writes: ../site/

Spreadsheet columns used: id, price_eur, affiliate_link, image_url.
Fill them, run this script, the whole site updates.
"""
import json, os, re, html, datetime, csv

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
OUT  = os.path.join(BASE, "..", "docs")
SITE_NAME = "PickIreland"
DOMAIN = "https://pickireland.best"   # change when you buy the domain
YEAR = datetime.date.today().year
TODAY = datetime.date.today().strftime("%d %B %Y")

# ---------------------------------------------------------------- affiliate links
def load_links():
    links = {}
    xlsx = os.path.join(BASE, "affiliate_links.xlsx")
    csvf = os.path.join(BASE, "affiliate_links.csv")
    if os.path.exists(xlsx):
        try:
            from openpyxl import load_workbook
            wb = load_workbook(xlsx, read_only=True)
            ws = wb["Affiliate Links"] if "Affiliate Links" in wb.sheetnames else wb.active
            headers = [str(c.value).strip().lower() if c.value else "" for c in next(ws.iter_rows(min_row=1, max_row=1))]
            def col(name):
                return headers.index(name) if name in headers else None
            id_i, link_i = col("id"), col("affiliate_link")
            price_i, img_i = col("price_eur"), col("image_url")
            for row in ws.iter_rows(min_row=2, values_only=True):
                if not row or id_i is None or not row[id_i]:
                    continue
                pid = str(row[id_i]).strip()
                def val(i):
                    if i is None or row[i] is None: return ""
                    return str(row[i]).strip()
                links[pid] = {"link": val(link_i), "price": row[price_i] if price_i is not None else None, "image": val(img_i)}
            return links
        except Exception as e:
            print("! Could not read affiliate_links.xlsx:", e)
    if os.path.exists(csvf):
        with open(csvf, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                links[row["id"].strip()] = {"link": row.get("affiliate_link", "").strip(),
                                            "price": row.get("price_eur"), "image": row.get("image_url", "").strip()}
    return links

LINKS = load_links()

def amazon_search_url(p):
    q = re.sub(r"[^A-Za-z0-9 ]", "", p["name"]).replace(" ", "+")
    return f"https://www.amazon.ie/s?k={q}"

def product_url(p):
    info = LINKS.get(p["id"], {})
    if info.get("link"):
        return info["link"], True
    return amazon_search_url(p), False

def product_price(p):
    info = LINKS.get(p["id"], {})
    if info.get("price"):
        try: return int(float(info["price"]))
        except (TypeError, ValueError): pass
    return p["price"]

def product_image(p):
    return LINKS.get(p["id"], {}).get("image", "")

def esc(s): return html.escape(str(s), quote=True)

# ---------------------------------------------------------------- svg icons (lucide-style, 24x24)
ICONS = {
"electric-scooters": '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
"electric-bikes": '<circle cx="5.5" cy="17.5" r="3.5"/><circle cx="18.5" cy="17.5" r="3.5"/><path d="M15 6a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm-3 11.5V14l-3-3 4-3 2 3h2"/>',
"dehumidifiers": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/>',
"air-fryers": '<path d="M3 8h18v9a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4z"/><path d="M7 4v2m5-2v2m5-2v2"/>',
"electric-heaters": '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>',
"air-purifiers": '<path d="M17.7 7.7a2.5 2.5 0 1 1 1.8 4.3H2"/><path d="M9.6 4.6A2 2 0 1 1 11 8H2"/><path d="M12.6 19.4A2 2 0 1 0 14 16H2"/>',
"robot-vacuums": '<circle cx="12" cy="12" r="9"/><path d="M8 12h8m-4-4v.01"/>',
"robot-lawn-mowers": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>',
"home-office": '<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8m-4-4v4"/>',
"coffee-machines": '<path d="M17 8h1a4 4 0 1 1 0 8h-1"/><path d="M3 8h14v9a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4z"/><path d="M7 2v3m4-3v3m4-3v3"/>',
}
def icon(cat_key, size=24, cls="ic"):
    path = ICONS.get(cat_key, '<circle cx="12" cy="12" r="9"/>')
    return f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{path}</svg>'

CHECK = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>'
CROSS = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg>'
STAR  = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" stroke="none" aria-hidden="true"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01z"/></svg>'
STAR_H = '<svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true"><defs><linearGradient id="hg"><stop offset="50%" stop-color="currentColor"/><stop offset="50%" stop-color="#D8DEE6"/></linearGradient></defs><path fill="url(#hg)" d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01z"/></svg>'
ARROW = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6"/></svg>'
SHIELD = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>'

# ---------------------------------------------------------------- css
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;600;700;800&family=Rubik:wght@500;600;700;800&display=swap');
:root{--green:#0E6B4A;--green-d:#0A5238;--green-t:#E7F2ED;--gold:#F59E0B;--gold-d:#B45309;--ink:#0F172A;--mut:#475569;--bg:#F6F8F7;--card:#FFFFFF;--line:#E2E8F0;--rad:16px;
--sh-sm:0 1px 2px rgba(15,23,42,.06);--sh-md:0 4px 16px rgba(15,23,42,.08);--sh-lg:0 12px 32px rgba(15,23,42,.12)}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*,*::before,*::after{animation:none!important;transition:none!important}}
body{font-family:'Nunito Sans',-apple-system,'Segoe UI',sans-serif;color:var(--ink);background:var(--bg);line-height:1.7;font-size:17px}
h1,h2,h3,.logo,.btn,.price{font-family:'Rubik','Nunito Sans',sans-serif}
a{color:var(--green);text-decoration:none}
a:hover{text-decoration:underline}
a:focus-visible,button:focus-visible,summary:focus-visible{outline:3px solid var(--gold);outline-offset:2px;border-radius:4px}
.wrap{max-width:1120px;margin:0 auto;padding:0 22px}
.ic{flex:none}
/* header */
header{background:rgba(255,255,255,.94);backdrop-filter:blur(8px);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:50}
.nav{display:flex;align-items:center;justify-content:space-between;height:66px;gap:16px}
.logo{font-size:1.4rem;font-weight:800;color:var(--ink);letter-spacing:-.5px;display:flex;align-items:center;gap:9px}
.logo:hover{text-decoration:none}
.logo .mark{width:34px;height:34px;border-radius:10px;background:linear-gradient(135deg,var(--green),#16916a);color:#fff;display:flex;align-items:center;justify-content:center;font-size:1rem;font-weight:800}
.logo span{color:var(--green)}
.nav-links{display:flex;gap:4px;flex-wrap:wrap}
.nav-links a{font-size:.88rem;font-weight:700;color:var(--mut);padding:8px 12px;border-radius:9px;transition:background .2s,color .2s}
.nav-links a:hover{color:var(--green);background:var(--green-t);text-decoration:none}
@media(max-width:860px){.nav-links a:nth-child(n+4):not(:last-child){display:none}}
.disclosure{background:var(--green-t);font-size:.78rem;color:#33524a;padding:7px 0;text-align:center}
.disclosure a{font-weight:700}
/* page head */
.crumbs{font-size:.8rem;color:var(--mut);margin:22px 0 4px;display:flex;gap:6px;flex-wrap:wrap}
.crumbs a{color:var(--mut)}
h1{font-size:2.3rem;line-height:1.15;letter-spacing:-.6px;margin:10px 0 12px;font-weight:800}
.updated{display:flex;align-items:center;gap:8px;font-size:.84rem;color:var(--mut);margin-bottom:16px;flex-wrap:wrap}
.updated .dot{width:4px;height:4px;border-radius:50%;background:#CBD5E1}
.trust-chip{display:inline-flex;align-items:center;gap:5px;background:var(--green-t);color:var(--green-d);font-weight:700;font-size:.78rem;padding:3px 10px;border-radius:99px}
.intro{font-size:1.08rem;color:#334155;max-width:840px;margin-bottom:28px}
h2{font-size:1.55rem;margin:44px 0 16px;letter-spacing:-.4px;font-weight:700}
h3{font-size:1.12rem;margin:20px 0 8px;font-weight:700}
/* toc */
.toc{background:var(--card);border:1px solid var(--line);border-radius:var(--rad);padding:20px 24px;margin-bottom:32px;box-shadow:var(--sh-sm)}
.toc b{display:flex;align-items:center;gap:8px;margin-bottom:10px;font-size:.95rem}
.toc ol{margin-left:22px;font-size:.95rem}
.toc li{margin:6px 0}
.toc li i{color:var(--mut);font-style:normal;font-size:.85rem}
/* table */
.tbl-scroll{overflow-x:auto;margin-bottom:8px;border-radius:var(--rad);box-shadow:var(--sh-sm);border:1px solid var(--line)}
table.cmp{width:100%;border-collapse:collapse;background:var(--card);font-size:.89rem;min-width:640px}
table.cmp th{background:linear-gradient(135deg,var(--green),var(--green-d));color:#fff;padding:12px 14px;text-align:left;font-size:.8rem;text-transform:uppercase;letter-spacing:.5px;font-weight:700}
table.cmp td{padding:12px 14px;border-top:1px solid var(--line);vertical-align:top}
table.cmp tr:nth-child(even) td{background:#FAFCFB}
table.cmp tr:hover td{background:var(--green-t)}
/* product card */
.card{position:relative;background:var(--card);border:1px solid var(--line);border-radius:var(--rad);padding:28px;margin:26px 0;box-shadow:var(--sh-sm);transition:box-shadow .25s,transform .25s}
.card:hover{box-shadow:var(--sh-md)}
.card.top-pick{border:2px solid var(--gold);box-shadow:0 4px 24px rgba(245,158,11,.16)}
.rank{position:absolute;top:-14px;left:24px;width:34px;height:34px;border-radius:50%;background:var(--ink);color:#fff;font-weight:800;font-size:.95rem;display:flex;align-items:center;justify-content:center;font-family:'Rubik';box-shadow:var(--sh-sm)}
.card.top-pick .rank{background:var(--gold);color:#3B2300}
.badge{display:inline-flex;align-items:center;gap:6px;background:#FEF3C7;color:#92400E;font-size:.72rem;font-weight:800;text-transform:uppercase;letter-spacing:.5px;padding:5px 12px;border-radius:99px;margin-bottom:10px}
.card-head{display:flex;gap:24px;align-items:flex-start;flex-wrap:wrap}
.card-info{flex:1;min-width:240px}
.pimg{width:170px;height:170px;flex:none;border-radius:12px;border:1px solid var(--line);background:#fff;display:flex;align-items:center;justify-content:center;overflow:hidden}
.pimg img{max-width:100%;max-height:100%;object-fit:contain}
.pimg .ph{display:flex;flex-direction:column;align-items:center;gap:8px;color:#94A3B8;font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.5px}
.pimg .ph .ic{width:44px;height:44px;color:#CBD5E1}
@media(max-width:560px){.pimg{width:100%;height:180px}}
.card h3{font-size:1.35rem;margin:0 0 2px;letter-spacing:-.3px}
.brandline{color:var(--mut);font-size:.87rem;margin-bottom:10px;font-weight:600}
.pricerow{display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin:10px 0 4px}
.price{font-size:1.55rem;font-weight:800;color:var(--ink)}
.price small{font-size:.72rem;color:var(--mut);font-weight:600;display:block;font-family:'Nunito Sans'}
.stars{display:flex;align-items:center;gap:2px;color:var(--gold)}
.stars small{color:var(--mut);margin-left:7px;font-weight:700;font-size:.84rem}
.specgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(155px,1fr));gap:9px;margin:16px 0;font-size:.86rem}
.specgrid div{background:#F1F5F4;border-radius:10px;padding:9px 12px}
.specgrid b{display:block;font-size:.68rem;text-transform:uppercase;color:var(--mut);letter-spacing:.5px;margin-bottom:1px}
.pc{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:16px 0}
@media(max-width:640px){.pc{grid-template-columns:1fr}h1{font-size:1.65rem}}
.pros,.cons{border-radius:12px;padding:16px 18px;font-size:.92rem}
.pros{background:#ECFDF3;border:1px solid #BBE5C8}
.cons{background:#FEF6F3;border:1px solid #F5D5C8}
.pros b,.cons b{display:flex;align-items:center;gap:7px;margin-bottom:8px;font-size:.78rem;text-transform:uppercase;letter-spacing:.5px}
.pros b{color:#15693B}.cons b{color:#9A3F22}
.pros ul,.cons ul{list-style:none}
.pros li,.cons li{margin:5px 0;padding-left:22px;position:relative}
.pros li::before{content:'✓';position:absolute;left:2px;color:#16A34A;font-weight:800}
.cons li::before{content:'–';position:absolute;left:4px;color:#C2552F;font-weight:800}
.verdict{font-size:.97rem;background:linear-gradient(90deg,var(--green-t),transparent);border-left:4px solid var(--green);padding:14px 18px;border-radius:0 12px 12px 0;margin:16px 0}
.btn{display:inline-flex;align-items:center;gap:9px;background:linear-gradient(135deg,#F59E0B,#F08A00);color:#2A1A00;font-weight:800;font-size:1.02rem;padding:14px 30px;border-radius:12px;box-shadow:0 4px 14px rgba(245,158,11,.35);transition:box-shadow .2s,transform .2s;cursor:pointer}
.btn:hover{box-shadow:0 6px 20px rgba(245,158,11,.5);transform:translateY(-1px);text-decoration:none}
.btn .ic{transition:transform .2s}
.btn:hover .ic{transform:translateX(3px)}
.btn-sub{font-size:.75rem;color:var(--mut);margin-top:8px}
/* guide & faq */
.guide{background:var(--card);border:1px solid var(--line);border-radius:var(--rad);padding:10px 28px 20px;margin:20px 0;box-shadow:var(--sh-sm)}
details{border-bottom:1px solid var(--line);padding:15px 0}
details:last-child{border-bottom:none}
summary{font-weight:700;cursor:pointer;font-size:1rem;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:12px}
summary::-webkit-details-marker{display:none}
summary::after{content:'+';font-size:1.3rem;color:var(--green);font-weight:700;transition:transform .2s}
details[open] summary::after{transform:rotate(45deg)}
details p{margin-top:10px;color:#334155;font-size:.95rem}
/* tiles */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(245px,1fr));gap:18px;margin:26px 0}
.tile{position:relative;background:var(--card);border:1px solid var(--line);border-radius:var(--rad);transition:box-shadow .25s,transform .25s,border-color .25s;box-shadow:var(--sh-sm)}
.tile:hover{box-shadow:var(--sh-md);transform:translateY(-3px);border-color:#BFD8CD}
.tile a{display:block;padding:24px;text-decoration:none;cursor:pointer}
.tile .icw{width:46px;height:46px;border-radius:12px;background:var(--green-t);color:var(--green);display:flex;align-items:center;justify-content:center;margin-bottom:14px;transition:background .25s,color .25s}
.tile:hover .icw{background:var(--green);color:#fff}
.tile h3{margin:0 0 4px;font-size:1.06rem;color:var(--ink)}
.tile p{font-size:.84rem;color:var(--mut)}
.tile .go{position:absolute;top:22px;right:20px;color:#CBD5E1;transition:color .25s,transform .25s}
.tile:hover .go{color:var(--green);transform:translateX(2px)}
/* related */
.related{margin:36px 0}
.related a{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:13px 16px;margin:8px 0;background:var(--card);border:1px solid var(--line);border-radius:12px;font-size:.95rem;font-weight:700;transition:border-color .2s,box-shadow .2s;cursor:pointer}
.related a:hover{text-decoration:none;border-color:var(--green);box-shadow:var(--sh-sm)}
/* hero */
.hero{background:linear-gradient(135deg,#0A5238 0%,#0E6B4A 55%,#11815A 100%);color:#fff;padding:74px 0 66px;text-align:center;position:relative;overflow:hidden}
.hero::after{content:'';position:absolute;inset:0;background:radial-gradient(700px 300px at 80% -10%,rgba(245,158,11,.18),transparent),radial-gradient(500px 260px at 10% 110%,rgba(255,255,255,.08),transparent)}
.hero>*{position:relative;z-index:1}
.hero h1{color:#fff;font-size:2.7rem;max-width:780px;margin:0 auto 16px}
.hero p{font-size:1.14rem;opacity:.94;max-width:660px;margin:0 auto 26px}
.hero-stats{display:flex;gap:14px;justify-content:center;flex-wrap:wrap}
.hero-stats div{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.22);border-radius:12px;padding:10px 20px;font-size:.9rem;font-weight:700;backdrop-filter:blur(4px)}
.hero-stats b{display:block;font-size:1.3rem;font-family:'Rubik'}
/* footer */
footer{background:var(--ink);color:#94A3B8;margin-top:64px;padding:46px 0 32px;font-size:.87rem}
footer a{color:#CBD5E1}
footer .cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:28px;margin-bottom:26px}
footer h4{color:#fff;font-size:.93rem;margin-bottom:12px;font-family:'Rubik'}
footer .legal{border-top:1px solid #243244;padding-top:18px;font-size:.77rem;line-height:1.6}
.notice{font-size:.79rem;color:var(--mut);margin:32px 0 10px;line-height:1.6}
"""

# ---------------------------------------------------------------- template pieces
def stars(r):
    full = int(r); half = r - full >= 0.5
    s = STAR * full + (STAR_H if half else "")
    return f'{s}<small>{r}/5</small>'

def header_html(depth=0):
    p = "../" * depth
    cats_links = "".join(f'<a href="{p}{c["category"]}/index.html">{c["name"]}</a>' for c in CATS[:5])
    return f"""<header><div class="wrap nav">
<a class="logo" href="{p}index.html" aria-label="{SITE_NAME} home"><span class="mark">P</span>Pick<span>Ireland</span></a>
<nav class="nav-links" aria-label="Categories">{cats_links}<a href="{p}index.html#categories">All categories</a></nav>
</div></header>
<div class="disclosure">As an Amazon Associate, {SITE_NAME} earns from qualifying purchases. <a href="{p}affiliate-disclosure.html">Learn more</a></div>"""

def footer_html(depth=0):
    p = "../" * depth
    cat_links = "".join(f'<a href="{p}{c["category"]}/index.html">{c["name"]}</a><br>' for c in CATS)
    return f"""<footer><div class="wrap">
<div class="cols">
<div><h4>{SITE_NAME}</h4><p>Independent buying guides for Irish shoppers. We compare products on specs, real running costs and value — so you don't have to open 40 tabs.</p></div>
<div><h4>Categories</h4>{cat_links}</div>
<div><h4>About</h4><a href="{p}about.html">About us</a><br><a href="{p}affiliate-disclosure.html">Affiliate disclosure</a><br><a href="{p}privacy.html">Privacy policy</a><br><a href="{p}contact.html">Contact</a></div>
</div>
<div class="legal">© {YEAR} {SITE_NAME}. Prices shown are typical/indicative in EUR and change frequently — always check the current price at the retailer. As an Amazon Associate we earn from qualifying purchases.</div>
</div></footer>"""

def page_shell(title, desc, canonical, body, depth=0, jsonld=""):
    return f"""<!DOCTYPE html>
<html lang="en-IE">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="article">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{SITE_NAME}">
<meta name="twitter:card" content="summary">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<style>{CSS}</style>
{jsonld}
</head>
<body>
{header_html(depth)}
<main class="wrap">
{body}
</main>
{footer_html(depth)}
</body>
</html>"""

def product_card(p, rank, cat_key):
    url, has_aff = product_url(p)
    price = product_price(p)
    img = product_image(p)
    rel = 'sponsored noopener' if has_aff else 'nofollow noopener'
    if img:
        img_html = f'<img src="{esc(img)}" alt="{esc(p["name"])}" loading="lazy" width="170" height="170">'
    else:
        img_html = f'<div class="ph">{icon(cat_key, 44)}<span>{esc(p["brand"])}</span></div>'
    specs = "".join(f"<div><b>{esc(k)}</b>{esc(v)}</div>" for k, v in p["specs"].items())
    pros = "".join(f"<li>{esc(x)}</li>" for x in p["pros"])
    cons = "".join(f"<li>{esc(x)}</li>" for x in p["cons"])
    top = " top-pick" if rank == 1 else ""
    return f"""<article class="card{top}" id="{p['id']}">
<div class="rank" aria-label="Rank {rank}">{rank}</div>
<span class="badge">{esc(p['badge'])}</span>
<div class="card-head">
  <div class="pimg">{img_html}</div>
  <div class="card-info">
    <h3>{esc(p['name'])}</h3>
    <div class="brandline">by {esc(p['brand'])}</div>
    <div class="pricerow">
      <div class="price">€{price}<small>typical price</small></div>
      <div class="stars" aria-label="Rated {p['rating']} out of 5">{stars(p['rating'])}</div>
    </div>
  </div>
</div>
<div class="specgrid">{specs}</div>
<div class="pc">
  <div class="pros"><b>{CHECK} Pros</b><ul>{pros}</ul></div>
  <div class="cons"><b>{CROSS} Cons</b><ul>{cons}</ul></div>
</div>
<p class="verdict"><strong>Our verdict:</strong> {esc(p['verdict'])}</p>
<a class="btn" href="{esc(url)}" target="_blank" rel="{rel}">Check Price on Amazon.ie {ARROW}</a>
<div class="btn-sub">Price and availability accurate as of publishing; subject to change.</div>
</article>"""

def comparison_table(products):
    spec_keys = []
    for p in products:
        for k in p["specs"]:
            if k not in spec_keys:
                spec_keys.append(k)
    spec_keys = spec_keys[:4]
    head = "<tr><th>Product</th><th>Best for</th><th>Price</th>" + "".join(f"<th>{esc(k)}</th>" for k in spec_keys) + "<th>Rating</th></tr>"
    rows = ""
    for p in products:
        cells = "".join(f"<td>{esc(p['specs'].get(k, '—'))}</td>" for k in spec_keys)
        rows += f"""<tr><td><a href="#{p['id']}"><b>{esc(p['name'])}</b></a></td><td>{esc(p['badge'])}</td><td><b>€{product_price(p)}</b></td>{cells}<td><b>{p['rating']}</b>/5</td></tr>"""
    return f'<div class="tbl-scroll"><table class="cmp">{head}{rows}</table></div>'

def faq_html(faqs):
    items = "".join(f"<details><summary>{esc(f['q'])}</summary><p>{esc(f['a'])}</p></details>" for f in faqs)
    return f'<div class="guide">{items}</div>'

def jsonld_page(page, cat, faqs):
    canonical = f"{DOMAIN}/{cat['category']}/{page['slug']}.html"
    items = []
    for i, p in enumerate(page["products"]):
        prod = {"@type": "Product", "name": p["name"], "brand": {"@type": "Brand", "name": p["brand"]},
                "offers": {"@type": "Offer", "price": str(product_price(p)), "priceCurrency": "EUR",
                           "availability": "https://schema.org/InStock", "url": product_url(p)[0]},
                "aggregateRating": {"@type": "AggregateRating", "ratingValue": str(p["rating"]), "reviewCount": "1", "bestRating": "5"},
                "review": {"@type": "Review", "reviewBody": p["verdict"],
                           "author": {"@type": "Organization", "name": SITE_NAME},
                           "reviewRating": {"@type": "Rating", "ratingValue": str(p["rating"]), "bestRating": "5"}}}
        if product_image(p):
            prod["image"] = product_image(p)
        items.append({"@type": "ListItem", "position": i + 1, "item": prod})
    data = [
        {"@context": "https://schema.org", "@type": "ItemList", "name": page["h1"], "itemListElement": items},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in faqs]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
            {"@type": "ListItem", "position": 2, "name": cat["name"], "item": f"{DOMAIN}/{cat['category']}/"},
            {"@type": "ListItem", "position": 3, "name": page["h1"], "item": canonical}]}
    ]
    return "".join(f'<script type="application/ld+json">{json.dumps(d, ensure_ascii=False)}</script>' for d in data)

# ---------------------------------------------------------------- load data
CATS = []
for fn in sorted(os.listdir(DATA)):
    if fn.endswith(".json"):
        with open(os.path.join(DATA, fn), encoding="utf-8") as f:
            CATS.append(json.load(f))

os.makedirs(OUT, exist_ok=True)
all_pages = []

# ---------------------------------------------------------------- comparison pages
for cat in CATS:
    cdir = os.path.join(OUT, cat["category"])
    os.makedirs(cdir, exist_ok=True)
    for page in cat["pages"]:
        faqs = [cat["faqs"][i] for i in page["faq_idx"]]
        canonical = f"{DOMAIN}/{cat['category']}/{page['slug']}.html"
        toc = "".join(f'<li><a href="#{p["id"]}">{esc(p["name"])}</a> <i>— {esc(p["badge"])}</i></li>' for p in page["products"])
        cards = "".join(product_card(p, i + 1, cat["category"]) for i, p in enumerate(page["products"]))
        guide = "".join(f"<h3>{esc(h)}</h3><p>{esc(t)}</p>" for h, t in cat["guide"])
        others = [pg for pg in cat["pages"] if pg["slug"] != page["slug"]]
        related = "".join(f'<a href="{pg["slug"]}.html">{esc(pg["h1"])} {ARROW}</a>' for pg in others)
        body = f"""
<nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a> › <a href="index.html">{esc(cat['name'])}</a> › {esc(page['h1'])}</nav>
<h1>{esc(page['h1'])}</h1>
<div class="updated"><span class="trust-chip">{SHIELD} Independently researched</span><span class="dot"></span><span>Updated {TODAY}</span><span class="dot"></span><a href="../affiliate-disclosure.html">How we make money</a></div>
<p class="intro">{esc(page['intro'])}</p>
<div class="toc"><b>{icon(cat['category'], 18)} Our top 5 at a glance</b><ol>{toc}</ol></div>
<h2>Quick comparison</h2>
{comparison_table(page['products'])}
<h2>The picks, reviewed</h2>
{cards}
<h2>Buying guide: how to choose</h2>
<div class="guide" style="padding:18px 28px">{guide}</div>
<h2>Frequently asked questions</h2>
{faq_html(faqs)}
<div class="related"><h2>More {esc(cat['name'].lower())} guides</h2>{related}</div>
<p class="notice">{SITE_NAME} is reader-supported. When you buy through links on our site, we may earn an affiliate commission at no extra cost to you. Prices are indicative, in EUR, and fluctuate — always confirm the live price. We select products based on specifications, owner feedback and value analysis.</p>
"""
        out = page_shell(page["title"], page["desc"], canonical, body, depth=1, jsonld=jsonld_page(page, cat, faqs))
        with open(os.path.join(cdir, page["slug"] + ".html"), "w", encoding="utf-8") as f:
            f.write(out)
        all_pages.append(f"{cat['category']}/{page['slug']}.html")

    tiles = "".join(f"""<div class="tile"><a href="{pg['slug']}.html"><span class="go">{ARROW}</span><div class="icw">{icon(cat['category'], 24)}</div><h3>{esc(pg['h1'])}</h3><p>{esc(pg['desc'][:110])}…</p></a></div>""" for pg in cat["pages"])
    hub_faq = faq_html(cat["faqs"])
    body = f"""
<nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a> › {esc(cat['name'])}</nav>
<h1>Best {esc(cat['name'])} in Ireland — All Guides</h1>
<p class="intro">{esc(cat['hub_intro'])}</p>
<div class="grid">{tiles}</div>
<h2>{esc(cat['name'])}: frequently asked questions</h2>
{hub_faq}
"""
    out = page_shell(f"Best {cat['name']} in Ireland 2026 — Guides & Comparisons | {SITE_NAME}",
                     cat["hub_intro"][:155], f"{DOMAIN}/{cat['category']}/", body, depth=1)
    with open(os.path.join(cdir, "index.html"), "w", encoding="utf-8") as f:
        f.write(out)
    all_pages.append(f"{cat['category']}/index.html")

# ---------------------------------------------------------------- homepage
tiles = ""
for cat in CATS:
    tiles += f"""<div class="tile"><a href="{cat['category']}/index.html"><span class="go">{ARROW}</span><div class="icw">{icon(cat['category'], 24)}</div><h3>{esc(cat['name'])}</h3><p>{len(cat['pages'])} buying guides · {sum(len(p['products']) for p in cat['pages'])} products compared</p></a></div>"""
featured = ""
for cat in CATS:
    pg = cat["pages"][0]
    featured += f'<a href="{cat["category"]}/{pg["slug"]}.html"><span style="display:flex;align-items:center;gap:10px"><span class="icw" style="width:34px;height:34px;border-radius:9px;background:var(--green-t);color:var(--green);display:inline-flex;align-items:center;justify-content:center">{icon(cat["category"], 18)}</span>{esc(pg["h1"])}</span>{ARROW}</a>'
n_guides = sum(len(c["pages"]) for c in CATS)
n_prods = sum(len(p["products"]) for c in CATS for p in c["pages"])
body_home = f"""
<div class="hero" style="margin:0 -22px"><div class="wrap">
<h1>Ireland's honest buying guides</h1>
<p>We compare the products Irish shoppers actually buy — specs, running costs at Irish prices, and real trade-offs. No fluff, no 40 open tabs.</p>
<div class="hero-stats"><div><b>{n_guides}</b>buying guides</div><div><b>{n_prods}</b>products compared</div><div><b>{YEAR}</b>kept updated</div></div>
</div></div>
<h2 id="categories">Browse by category</h2>
<div class="grid">{tiles}</div>
<h2>Featured guides</h2>
<div class="related">{featured}</div>
<h2>How {SITE_NAME} works</h2>
<p>Every guide compares five carefully selected products using manufacturer specifications, verified owner feedback and Irish-specific factors — electricity rates, weather, legal rules and local availability. When you buy through our links we may earn a commission from Amazon.ie or other retailers, at no cost to you. That's the entire business model: useful guides, honest picks. <a href="affiliate-disclosure.html">Full disclosure here</a>.</p>
"""
home_jsonld = '<script type="application/ld+json">' + json.dumps({
    "@context": "https://schema.org", "@type": "WebSite", "name": SITE_NAME, "url": DOMAIN,
    "description": "Independent product comparison guides for Irish shoppers."}) + "</script>"
with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
    f.write(page_shell(f"{SITE_NAME} — Ireland's Honest Product Comparison Guides 2026",
                       "Independent buying guides for Irish shoppers: e-scooters, e-bikes, dehumidifiers, air fryers, heaters and more. Compared for Irish prices, weather and rules.",
                       DOMAIN + "/", body_home, depth=0, jsonld=home_jsonld))
all_pages.append("index.html")

# ---------------------------------------------------------------- legal & info pages
def simple_page(fname, title, body_html):
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        f.write(page_shell(f"{title} | {SITE_NAME}", title, f"{DOMAIN}/{fname}",
                           f"<h1 style='margin-top:28px'>{title}</h1>{body_html}", depth=0))
    all_pages.append(fname)

simple_page("affiliate-disclosure.html", "Affiliate Disclosure", f"""
<p><strong>As an Amazon Associate, {SITE_NAME} earns from qualifying purchases.</strong></p>
<p>{SITE_NAME} is a reader-supported website. When you click a link on our site and buy something from a retailer such as Amazon.ie, we may receive a small commission. This never costs you anything extra — the price is identical whether you use our link or not.</p>
<p>Commissions never influence our rankings. Products are selected and ordered based on specifications, verified owner feedback, running-cost analysis at Irish prices, and suitability for Irish conditions. We frequently recommend cheaper products over more expensive ones (which would earn us more) because they're the better buy.</p>
<p>Prices shown on this site are typical/indicative prices in EUR at time of writing. Prices change constantly — always check the live price on the retailer's page before buying.</p>""")

simple_page("about.html", "About PickIreland", f"""
<p>{SITE_NAME} exists because buying decisions in Ireland are different: our electricity is among Europe's priciest, our weather is wet, our houses are damp, our e-scooter laws are specific, and most "best of" lists online are written for the UK or US market.</p>
<p>Every guide on this site compares five products per use-case with Irish running costs, Irish rules and Irish weather factored in. We keep guides updated as prices and models change.</p>
<p>Got a correction or a product suggestion? See our <a href="contact.html">contact page</a>.</p>""")

simple_page("privacy.html", "Privacy Policy", f"""
<p>{SITE_NAME} respects your privacy. We do not require accounts, collect names, or store personal data submitted by visitors.</p>
<p><strong>Analytics:</strong> We may use privacy-respecting analytics to understand which guides are useful (page views, approximate region, device type). No personally identifying information is collected.</p>
<p><strong>Affiliate links:</strong> When you click an affiliate link, the retailer (e.g. Amazon) may set cookies to attribute the sale. Those cookies are governed by the retailer's own privacy policy.</p>
<p><strong>Contact:</strong> If you email us, we use your address only to reply.</p>""")

simple_page("contact.html", "Contact", """
<p>Spotted an error? Price changed? Have a product we should look at?</p>
<p>Email us: <strong>hello@pickireland.best</strong> (set this up with your domain provider).</p>""")

# ---------------------------------------------------------------- sitemap & robots
urls = "".join(f"<url><loc>{DOMAIN}/{p if p != 'index.html' else ''}</loc><lastmod>{datetime.date.today()}</lastmod></url>" for p in all_pages)
with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")

linked = sum(1 for v in LINKS.values() if v.get("link"))
imgs = sum(1 for v in LINKS.values() if v.get("image"))
print(f"Built {len(all_pages)} pages into {os.path.abspath(OUT)}")
print(f"Affiliate links filled: {linked} / 250 | images filled: {imgs} / 250")

# CNAME for GitHub Pages custom domain
with open(os.path.join(OUT, "CNAME"), "w") as f:
    f.write("pickireland.best\n")
# .nojekyll prevents GitHub Pages from running Jekyll processing
open(os.path.join(OUT, ".nojekyll"), "w").close()
