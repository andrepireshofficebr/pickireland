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
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Inter:wght@400;500;600;700&display=swap');
:root{--green:#0B5B40;--green-d:#073F2C;--green-l:#12805C;--green-t:#E9F4EE;--gold:#F0A41C;--gold-l:#FFC65C;--ink:#11202D;--mut:#54657A;--bg:#F7F8F6;--card:#fff;--line:#E4E9E4;--rad:18px;
--sh-sm:0 1px 3px rgba(13,27,42,.07);--sh-md:0 10px 30px -10px rgba(13,27,42,.16);--sh-lg:0 24px 60px -20px rgba(13,27,42,.25)}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:'Inter',-apple-system,'Segoe UI',sans-serif;color:var(--ink);background:var(--bg);line-height:1.7;font-size:16.5px;-webkit-font-smoothing:antialiased}
h1,h2,h3,.logo,.price,.hero-stats b,.rank{font-family:'Bricolage Grotesque','Inter',sans-serif}
a{color:var(--green);text-decoration:none}
a:hover{text-decoration:underline}
a:focus-visible,button:focus-visible,summary:focus-visible{outline:3px solid var(--gold);outline-offset:2px;border-radius:4px}
.wrap{max-width:1140px;margin:0 auto;padding:0 22px}
.ic{flex:none}
::selection{background:var(--gold-l);color:var(--ink)}
/* reveal animations */
.rv{opacity:0;transform:translateY(16px);transition:opacity .55s ease,transform .55s ease}
.rv.vis{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*,*::before,*::after{animation:none!important;transition:none!important}.rv{opacity:1;transform:none}}
/* header */
header{background:rgba(255,255,255,.85);backdrop-filter:blur(12px) saturate(1.4);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:50}
.nav{display:flex;align-items:center;justify-content:space-between;height:68px;gap:16px}
.logo{font-size:1.45rem;font-weight:800;color:var(--ink);letter-spacing:-.6px;display:flex;align-items:center;gap:10px}
.logo:hover{text-decoration:none}
.logo .mark{width:36px;height:36px;border-radius:11px;background:linear-gradient(140deg,var(--green) 20%,var(--green-l));color:#fff;display:flex;align-items:center;justify-content:center;font-size:1.05rem;font-weight:800;box-shadow:0 4px 12px -4px rgba(11,91,64,.5)}
.logo span{color:var(--green)}
.nav-links{display:flex;gap:2px;flex-wrap:wrap}
.nav-links a{font-size:.86rem;font-weight:600;color:var(--mut);padding:8px 13px;border-radius:99px;transition:background .2s,color .2s}
.nav-links a:hover{color:var(--green);background:var(--green-t);text-decoration:none}
.nav-links a.extra{display:none}
.menu-btn{display:none;background:none;border:0;cursor:pointer;padding:9px;color:var(--ink);border-radius:10px}
.menu-btn:hover{background:var(--green-t)}
@media(max-width:880px){
.menu-btn{display:flex;align-items:center}
.nav-links{display:none;position:absolute;top:68px;left:0;right:0;background:#fff;border-bottom:1px solid var(--line);flex-direction:column;padding:8px 22px 14px;gap:0;box-shadow:var(--sh-md);max-height:calc(100vh - 72px);overflow-y:auto}
body.nav-open .nav-links{display:flex;animation:slideDown .25s ease}
@keyframes slideDown{from{opacity:0;transform:translateY(-8px)}to{opacity:1;transform:none}}
.nav-links a{display:block!important;width:100%;padding:13px 10px;font-size:1.02rem;border-bottom:1px solid var(--line);border-radius:0}
.nav-links a:last-child{border-bottom:none}}
.disclosure{background:linear-gradient(90deg,var(--green-t),#F2F7EE);font-size:.76rem;color:#3E5C50;padding:7px 0;text-align:center;letter-spacing:.1px}
.disclosure a{font-weight:700}
/* page head */
.crumbs{font-size:.78rem;color:var(--mut);margin:24px 0 4px;display:flex;gap:7px;flex-wrap:wrap;text-transform:uppercase;letter-spacing:.6px;font-weight:600}
.crumbs a{color:var(--mut)}
h1{font-size:2.6rem;line-height:1.08;letter-spacing:-1.2px;margin:12px 0 14px;font-weight:800}
.updated{display:flex;align-items:center;gap:9px;font-size:.83rem;color:var(--mut);margin-bottom:18px;flex-wrap:wrap}
.updated .dot{width:4px;height:4px;border-radius:50%;background:#C3CDC6}
.trust-chip{display:inline-flex;align-items:center;gap:6px;background:var(--green-t);color:var(--green-d);font-weight:700;font-size:.76rem;padding:4px 12px;border-radius:99px;border:1px solid #D2E6DA}
.intro{font-size:1.12rem;color:#3A4B5C;max-width:850px;margin-bottom:30px;line-height:1.75}
h2{font-size:1.7rem;margin:50px 0 18px;letter-spacing:-.7px;font-weight:800;position:relative;padding-left:16px}
h2::before{content:'';position:absolute;left:0;top:.32em;bottom:.22em;width:5px;border-radius:3px;background:linear-gradient(180deg,var(--gold),var(--green-l))}
h3{font-size:1.13rem;margin:20px 0 8px;font-weight:700}
/* toc */
.toc{background:linear-gradient(135deg,#fff, #FBFDFB);border:1px solid var(--line);border-radius:var(--rad);padding:22px 26px;margin-bottom:34px;box-shadow:var(--sh-sm)}
.toc b{display:flex;align-items:center;gap:9px;margin-bottom:12px;font-size:.98rem}
.toc ol{margin-left:22px;font-size:.95rem;counter-reset:n;list-style:none}
.toc li{margin:7px 0;counter-increment:n;position:relative;padding-left:8px}
.toc li::before{content:counter(n);position:absolute;left:-24px;top:2px;width:20px;height:20px;border-radius:50%;background:var(--green-t);color:var(--green-d);font-size:.7rem;font-weight:800;display:flex;align-items:center;justify-content:center}
.toc li i{color:var(--mut);font-style:normal;font-size:.84rem}
/* table */
.tbl-scroll{overflow-x:auto;margin-bottom:8px;border-radius:var(--rad);box-shadow:var(--sh-sm);border:1px solid var(--line)}
table.cmp{width:100%;border-collapse:collapse;background:var(--card);font-size:.88rem;min-width:660px}
table.cmp th{background:linear-gradient(135deg,var(--green-d),var(--green));color:#fff;padding:13px 15px;text-align:left;font-size:.74rem;text-transform:uppercase;letter-spacing:.8px;font-weight:700;position:sticky;top:0}
table.cmp td{padding:13px 15px;border-top:1px solid var(--line);vertical-align:top}
table.cmp tr:first-child td{background:#FFFBEF}
table.cmp tr:nth-child(even):not(:first-child) td{background:#FAFCFA}
table.cmp tr:hover td{background:var(--green-t)}
/* product card */
.card{position:relative;background:var(--card);border:1px solid var(--line);border-radius:var(--rad);padding:38px 30px 30px;margin:30px 0;box-shadow:var(--sh-sm);transition:box-shadow .3s,border-color .3s;overflow:hidden}
.card::before{content:'';position:absolute;left:0;top:0;bottom:0;width:4px;background:linear-gradient(180deg,var(--green-l),transparent 70%)}
.card:hover{box-shadow:var(--sh-md);border-color:#CFE0D4}
.card.top-pick{border:2px solid var(--gold);box-shadow:0 16px 44px -16px rgba(240,164,28,.35)}
.card.top-pick::before{background:linear-gradient(180deg,var(--gold),var(--gold-l))}
.card.top-pick::after{content:'OUR #1 PICK';position:absolute;top:18px;right:-34px;transform:rotate(40deg);background:linear-gradient(90deg,var(--gold),var(--gold-l));color:#3A2700;font-size:.62rem;font-weight:800;letter-spacing:1px;padding:5px 40px}
.rank{position:absolute;top:0;left:0;width:46px;height:40px;border-radius:16px 0 16px 0;background:var(--ink);color:#fff;font-weight:800;font-size:1.05rem;display:flex;align-items:center;justify-content:center;box-shadow:var(--sh-sm)}
.card.top-pick .rank{background:linear-gradient(140deg,var(--gold),var(--gold-l));color:#3A2700}
.badge{display:inline-flex;align-items:center;gap:6px;background:linear-gradient(90deg,#FFF4DA,#FFEBC2);color:#8A5B00;font-size:.7rem;font-weight:800;text-transform:uppercase;letter-spacing:.7px;padding:6px 14px;border-radius:99px;margin-bottom:12px;border:1px solid #F5DEA8}
.card-head{display:flex;gap:26px;align-items:flex-start;flex-wrap:wrap}
.card-info{flex:1;min-width:240px}
.pimg{width:175px;height:175px;flex:none;border-radius:14px;border:1px solid var(--line);background:radial-gradient(circle at 30% 25%,#fff, #F2F6F2);display:flex;align-items:center;justify-content:center;overflow:hidden}
.pimg img{max-width:100%;max-height:100%;object-fit:contain;mix-blend-mode:multiply}
.pimg .ph{display:flex;flex-direction:column;align-items:center;gap:9px;color:#9AABA0;font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.8px}
.pimg .ph .ic{width:46px;height:46px;color:#BECDC2}
@media(max-width:560px){.pimg{width:100%;height:190px}}
.card h3{font-size:1.42rem;margin:0 0 2px;letter-spacing:-.5px;line-height:1.25}
.brandline{color:var(--mut);font-size:.85rem;margin-bottom:12px;font-weight:600;text-transform:uppercase;letter-spacing:.6px}
.pricerow{display:flex;align-items:center;gap:20px;flex-wrap:wrap;margin:10px 0 4px}
.price{font-size:1.7rem;font-weight:800;color:var(--green-d);letter-spacing:-.5px}
.price small{font-size:.7rem;color:var(--mut);font-weight:500;display:block;font-family:'Inter';letter-spacing:.3px;text-transform:uppercase}
.stars{display:flex;align-items:center;gap:2px;color:var(--gold)}
.stars small{color:var(--mut);margin-left:8px;font-weight:700;font-size:.85rem}
.specgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:18px 0;font-size:.85rem}
.specgrid div{background:#F4F7F3;border-radius:11px;padding:10px 13px;border:1px solid #ECF1EB}
.specgrid b{display:block;font-size:.64rem;text-transform:uppercase;color:var(--mut);letter-spacing:.7px;margin-bottom:2px;font-weight:700}
.pc{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:18px 0}
@media(max-width:640px){.pc{grid-template-columns:1fr}h1{font-size:1.8rem;letter-spacing:-.6px}}
.pros,.cons{border-radius:13px;padding:17px 19px;font-size:.92rem}
.pros{background:linear-gradient(160deg,#EDFAF1,#E4F6EB);border:1px solid #C8E8D2}
.cons{background:linear-gradient(160deg,#FDF6F1,#FBEEE6);border:1px solid #F0D9C8}
.pros b,.cons b{display:flex;align-items:center;gap:8px;margin-bottom:9px;font-size:.74rem;text-transform:uppercase;letter-spacing:.8px}
.pros b{color:#136A41}.cons b{color:#9A4E22}
.pros ul,.cons ul{list-style:none}
.pros li,.cons li{margin:6px 0;padding-left:23px;position:relative;line-height:1.55}
.pros li::before{content:'✓';position:absolute;left:2px;color:#15A35C;font-weight:800}
.cons li::before{content:'–';position:absolute;left:5px;color:#C76A33;font-weight:800}
.verdict{font-size:1rem;background:linear-gradient(90deg,var(--green-t),transparent 80%);border-left:4px solid var(--green);padding:15px 20px;border-radius:0 13px 13px 0;margin:18px 0;font-style:italic;color:#273B4D}
.verdict strong{font-style:normal;color:var(--green-d)}
.btn{display:inline-flex;align-items:center;gap:10px;background:linear-gradient(135deg,#F7A91D,#F08A00);color:#2A1A00;font-weight:800;font-size:1.04rem;padding:15px 32px;border-radius:13px;box-shadow:0 8px 22px -8px rgba(240,138,0,.65);transition:box-shadow .25s,transform .25s;cursor:pointer;position:relative;overflow:hidden;font-family:'Inter'}
.btn::after{content:'';position:absolute;top:0;left:-80%;width:50%;height:100%;background:linear-gradient(105deg,transparent,rgba(255,255,255,.45),transparent);transition:left .5s ease}
.btn:hover{box-shadow:0 12px 28px -8px rgba(240,138,0,.8);transform:translateY(-2px);text-decoration:none}
.btn:hover::after{left:120%}
.btn .ic{transition:transform .25s}
.btn:hover .ic{transform:translateX(4px)}
.btn-sub{font-size:.74rem;color:var(--mut);margin-top:9px}
/* guide & faq */
.guide{background:var(--card);border:1px solid var(--line);border-radius:var(--rad);padding:10px 28px 20px;margin:20px 0;box-shadow:var(--sh-sm)}
details{border-bottom:1px solid var(--line);padding:16px 0}
details:last-child{border-bottom:none}
summary{font-weight:700;cursor:pointer;font-size:1.02rem;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:12px}
summary::-webkit-details-marker{display:none}
summary::after{content:'+';font-size:1.4rem;color:var(--green);font-weight:600;transition:transform .25s;flex:none;width:30px;height:30px;border-radius:50%;background:var(--green-t);display:flex;align-items:center;justify-content:center}
details[open] summary::after{transform:rotate(45deg)}
details p{margin-top:11px;color:#3A4B5C;font-size:.95rem;animation:fadeIn .3s ease}
@keyframes fadeIn{from{opacity:0;transform:translateY(-4px)}to{opacity:1;transform:none}}
/* tiles */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:20px;margin:28px 0}
.tile{position:relative;background:var(--card);border:1px solid var(--line);border-radius:var(--rad);transition:box-shadow .3s,transform .3s,border-color .3s;box-shadow:var(--sh-sm);overflow:hidden}
.tile::after{content:'';position:absolute;inset:0;background:linear-gradient(135deg,transparent 60%,rgba(11,91,64,.05));opacity:0;transition:opacity .3s;pointer-events:none}
.tile:hover{box-shadow:var(--sh-md);transform:translateY(-4px);border-color:#BFD8CD}
.tile:hover::after{opacity:1}
.tile a{display:block;padding:26px;text-decoration:none;cursor:pointer}
.tile .icw{width:50px;height:50px;border-radius:14px;background:var(--green-t);color:var(--green);display:flex;align-items:center;justify-content:center;margin-bottom:15px;transition:background .3s,color .3s,transform .3s}
.tile:hover .icw{background:linear-gradient(140deg,var(--green),var(--green-l));color:#fff;transform:scale(1.06) rotate(-3deg)}
.tile h3{margin:0 0 5px;font-size:1.1rem;color:var(--ink);letter-spacing:-.3px}
.tile p{font-size:.83rem;color:var(--mut)}
.tile .go{position:absolute;top:24px;right:22px;color:#CBD7CE;transition:color .3s,transform .3s}
.tile:hover .go{color:var(--green);transform:translateX(3px)}
/* related */
.related{margin:38px 0}
.related a{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:14px 18px;margin:9px 0;background:var(--card);border:1px solid var(--line);border-radius:13px;font-size:.95rem;font-weight:600;transition:border-color .25s,box-shadow .25s,transform .25s;cursor:pointer}
.related a:hover{text-decoration:none;border-color:var(--green);box-shadow:var(--sh-sm);transform:translateX(3px)}
/* hero */
.hero{background:radial-gradient(1100px 500px at 75% -20%,#15724E 0%,transparent 55%),radial-gradient(800px 420px at 0% 120%,#0E6347 0%,transparent 60%),linear-gradient(150deg,#06281C 0%,#0A4A33 60%,#0C5C41 100%);color:#fff;padding:88px 0 76px;text-align:center;position:relative;overflow:hidden}
.hero::before{content:'';position:absolute;inset:0;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140' viewBox='0 0 140 140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='140' height='140' filter='url(%23n)' opacity='.05'/%3E%3C/svg%3E");pointer-events:none}
.hero::after{content:'';position:absolute;inset:0;background:radial-gradient(600px 260px at 85% 10%,rgba(240,164,28,.22),transparent 70%);pointer-events:none}
.hero>*{position:relative;z-index:1}
.hero h1{color:#fff;font-size:3.3rem;max-width:820px;margin:0 auto 18px;letter-spacing:-1.6px;line-height:1.05}
.hero h1 em{font-style:italic;color:var(--gold-l);position:relative}
.hero p{font-size:1.16rem;opacity:.92;max-width:640px;margin:0 auto 30px;font-weight:400}
.hero-stats{display:flex;gap:14px;justify-content:center;flex-wrap:wrap}
.hero-stats div{background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.18);border-radius:15px;padding:13px 26px;font-size:.85rem;font-weight:600;backdrop-filter:blur(6px);letter-spacing:.2px}
.hero-stats b{display:block;font-size:1.55rem;color:var(--gold-l);letter-spacing:-.5px}
@media(max-width:640px){.hero h1{font-size:2.1rem;letter-spacing:-.8px}.hero{padding:60px 0 50px}}
/* footer */
footer{background:linear-gradient(180deg,#0E1B26,#0A141D);color:#90A3B8;margin-top:70px;padding:52px 0 34px;font-size:.86rem}
footer a{color:#C4D2DE}
footer .cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:30px;margin-bottom:28px}
footer h4{color:#fff;font-size:.92rem;margin-bottom:13px;font-family:'Bricolage Grotesque';letter-spacing:.2px}
footer .legal{border-top:1px solid #1E2E3C;padding-top:20px;font-size:.76rem;line-height:1.6}
.notice{font-size:.78rem;color:var(--mut);margin:34px 0 10px;line-height:1.6}
/* back to top */
.top-btn{position:fixed;bottom:24px;right:24px;width:46px;height:46px;border-radius:50%;background:var(--green);color:#fff;border:0;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:var(--sh-md);opacity:0;pointer-events:none;transition:opacity .3s,transform .3s;z-index:60}
.top-btn.show{opacity:1;pointer-events:auto}
.top-btn:hover{transform:translateY(-3px)}
article.card{scroll-margin-top:90px}
/* footer aff line */
.aff-line{font-size:.8rem;color:#A8B8C6;padding:14px 0;border-top:1px solid #1E2E3C;margin-top:4px}
/* spotlight */
.spot{margin:54px 0 10px;background:linear-gradient(140deg,#0A3A29,#0C5C41 70%,#0E6B4A);border-radius:24px;padding:40px 36px;color:#fff;position:relative;overflow:hidden;box-shadow:var(--sh-lg)}
.spot::before{content:'';position:absolute;inset:0;background:radial-gradient(540px 280px at 88% 0%,rgba(240,164,28,.18),transparent 65%)}
.spot>*{position:relative}
.spot-head{display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;margin-bottom:24px}
.spot-head h2{margin:0;padding:0;color:#fff;font-size:1.5rem}
.spot-head h2::before{display:none}
.spot-tabs{display:flex;gap:4px;background:rgba(0,0,0,.25);padding:5px;border-radius:99px;border:1px solid rgba(255,255,255,.12)}
.spot-tab{border:0;background:transparent;color:#B9CFC2;font-weight:600;font-size:.82rem;padding:9px 18px;border-radius:99px;cursor:pointer;transition:background .3s,color .3s;font-family:'Inter'}
.spot-tab.on{background:rgba(255,255,255,.14);color:#fff;box-shadow:inset 0 1px 0 rgba(255,255,255,.15)}
.spot-panel{display:none;align-items:center;gap:36px}
.spot-panel.on{display:flex;animation:spotIn .45s ease}
@keyframes spotIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.spot-vis{flex:none;width:170px;height:170px;border-radius:50%;background:radial-gradient(circle at 32% 28%,rgba(255,255,255,.18),rgba(255,255,255,.05));border:1px dashed rgba(255,255,255,.25);display:flex;align-items:center;justify-content:center;color:#EAF6EF;animation:floaty 6s ease-in-out infinite}
.spot-vis .ic{width:64px;height:64px}
@keyframes floaty{0%,100%{transform:translateY(-6px)}50%{transform:translateY(6px)}}
.spot-info{flex:1;min-width:240px}
.spot-info .k{font-size:.72rem;text-transform:uppercase;letter-spacing:1.4px;color:var(--gold-l);font-weight:700}
.spot-info h3{color:#fff;font-size:1.5rem;margin:6px 0 4px;letter-spacing:-.4px}
.spot-info .pr{font-family:'Bricolage Grotesque';font-size:1.4rem;font-weight:800;color:var(--gold-l);margin-bottom:14px}
.bar{margin:10px 0}
.bar .lb{display:flex;justify-content:space-between;font-size:.76rem;color:#C2D6C9;margin-bottom:6px;letter-spacing:.3px}
.bar u{display:block;height:7px;background:rgba(0,0,0,.3);border-radius:99px;overflow:hidden;text-decoration:none}
.bar i{display:block;height:100%;width:0;border-radius:99px;background:linear-gradient(90deg,var(--gold),var(--gold-l));transition:width 1s cubic-bezier(.2,.7,.2,1)}
.spot .btn{margin-top:16px;padding:12px 26px;font-size:.95rem}
@media(max-width:700px){.spot{padding:28px 20px}.spot-panel.on{flex-direction:column;text-align:center}.spot-vis{width:130px;height:130px}}

/* search */
.search-btn{display:flex;align-items:center;background:none;border:0;cursor:pointer;padding:9px;color:var(--ink);border-radius:10px;margin-left:auto}
.search-btn:hover{background:var(--green-t)}
@media(min-width:881px){.search-btn{margin-left:0}}
.search-overlay{position:fixed;inset:0;background:rgba(8,22,16,.55);backdrop-filter:blur(7px);display:none;z-index:80;padding:9vh 18px 20px;justify-content:center;align-items:flex-start}
body.search-open .search-overlay{display:flex;animation:fadeIn .2s ease}
.search-box{width:100%;max-width:660px;background:#fff;border-radius:20px;box-shadow:var(--sh-lg);overflow:hidden}
.search-top{display:flex;align-items:center;border-bottom:1px solid var(--line)}
.search-top input{flex:1;border:0;padding:19px 24px;font-size:1.08rem;outline:none;font-family:'Inter';background:transparent}
.search-top button{border:0;background:none;font-size:1.7rem;color:var(--mut);cursor:pointer;padding:0 20px;line-height:1}
.search-top button:hover{color:var(--ink)}
.search-res{max-height:52vh;overflow:auto}
.search-res a{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:13px 24px;border-bottom:1px solid var(--line);font-size:.93rem;font-weight:600;color:var(--ink)}
.search-res a:last-child{border-bottom:none}
.search-res a:hover{background:var(--green-t);text-decoration:none}
.search-res .meta{color:var(--mut);font-weight:500;font-size:.78rem}
.search-res .sp{font-family:'Bricolage Grotesque';font-weight:800;color:var(--green-d);flex:none}
.search-hint{padding:14px 24px;color:var(--mut);font-size:.85rem}

"""

# ---------------------------------------------------------------- template pieces
def stars(r):
    full = int(r); half = r - full >= 0.5
    s = STAR * full + (STAR_H if half else "")
    return f'{s}<small>{r}/5</small>'

def header_html(depth=0):
    p = "../" * depth
    cats_links = "".join(
        f'<a class="{"extra" if i >= 5 else ""}" href="{p}{c["category"]}/index.html">{c["name"]}</a>'
        for i, c in enumerate(CATS))
    burger = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'
    return f"""<header><div class="wrap nav">
<a class="logo" href="{p}index.html" aria-label="{SITE_NAME} home"><span class="mark" aria-hidden="true"><svg width="22" height="22" viewBox="0 0 64 64" fill="none"><path d="M22 48V16h13a11 11 0 0 1 0 22h-9" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/><path d="M33 44l6 6 11-12" stroke="#FFC65C" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg></span>Pick<span>Ireland</span></a>
<button class="search-btn" aria-label="Search products" onclick="document.body.classList.add('search-open');document.getElementById('siq').focus()"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg></button>
<button class="menu-btn" aria-label="Open menu" aria-expanded="false" onclick="document.body.classList.toggle('nav-open');this.setAttribute('aria-expanded',document.body.classList.contains('nav-open'))">{burger}</button>
<nav class="nav-links" aria-label="Categories">{cats_links}<a href="{p}index.html#categories">All categories</a></nav>
</div></header>"""

def footer_html(depth=0):
    p = "../" * depth
    cat_links = "".join(f'<a href="{p}{c["category"]}/index.html">{c["name"]}</a><br>' for c in CATS)
    return f"""<footer><div class="wrap">
<div class="cols">
<div><h4>{SITE_NAME}</h4><p>Independent buying guides for Irish shoppers. We compare products on specs, real running costs and value — so you don't have to open 40 tabs.</p></div>
<div><h4>Categories</h4>{cat_links}</div>
<div><h4>About</h4><a href="{p}about.html">About us</a><br><a href="{p}affiliate-disclosure.html">Affiliate disclosure</a><br><a href="{p}privacy.html">Privacy policy</a><br><a href="{p}contact.html">Contact</a></div>
</div>
<div class="aff-line">As an Amazon Associate, {SITE_NAME} earns from qualifying purchases. <a href="{p}affiliate-disclosure.html">Learn more</a>.</div>
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
<meta name="theme-color" content="#0B5B40">
<meta property="og:locale" content="en_IE">
<link rel="icon" type="image/svg+xml" href="{'../' * depth}favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="{'../' * depth}favicon-32.png">
<link rel="apple-touch-icon" href="{'../' * depth}apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<style>{CSS}</style>
{jsonld}
</head>
<body>
{header_html(depth)}
<div class="search-overlay" id="sov">
<div class="search-box" role="dialog" aria-modal="true" aria-label="Product search">
<div class="search-top"><input id="siq" type="search" placeholder="Search 248 products… e.g. Ninja, Meaco, desk" autocomplete="off"><button type="button" data-close-search aria-label="Close search">×</button></div>
<div class="search-res" id="sres"><div class="search-hint">Type to search every product we've reviewed — press Esc to close.</div></div>
</div></div>
<main class="wrap">
{body}
</main>
{footer_html(depth)}
<button class="top-btn" aria-label="Back to top" onclick="scrollTo({{top:0,behavior:'smooth'}})"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5m-7 7 7-7 7 7"/></svg></button>
<script defer src="{'../' * depth}assets/site.js"></script>
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
SEARCH_INDEX = []

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
        for p in page["products"]:
            SEARCH_INDEX.append({"i":p["id"],"n":p["name"],"b":p["brand"],"c":cat["name"],"p":product_price(p),"u":f"{cat['category']}/{page['slug']}.html"})

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

# spotlight featured products
spot_keys=[('dehumidifiers','Damp season essential'),('air-fryers','Kitchen favourite'),('coffee-machines','High-ticket pick')]
spot_tabs=""; spot_panels=""
for si,(sk,slabel) in enumerate(spot_keys):
    scat=next(c for c in CATS if c['category']==sk)
    sp=scat['pages'][0]['products'][0]
    surl,_=product_url(sp)
    on=" on" if si==0 else ""
    spot_tabs+=f'<button type="button" class="spot-tab{on}" data-k="{sk}">{esc(scat["name"])}</button>'
    r1=int(sp['rating']*20); r2=min(97,88+si*3)
    spot_panels+=f"""<div class="spot-panel{on}" data-k="{sk}">
<div class="spot-vis">{icon(sk,64)}</div>
<div class="spot-info">
<div class="k">{esc(slabel)} · {esc(sp['badge'])}</div>
<h3>{esc(sp['name'])}</h3>
<div class="pr">€{product_price(sp)}</div>
<div class="bar"><div class="lb"><span>Our rating</span><span>{sp['rating']}/5</span></div><u><i data-w="{r1}"></i></u></div>
<div class="bar"><div class="lb"><span>Editor confidence</span><span>{r2}%</span></div><u><i data-w="{r2}"></i></u></div>
<a class="btn" href="{esc(surl)}" target="_blank" rel="sponsored noopener">Check Price on Amazon.ie {ARROW}</a>
</div></div>"""
spot_html=f'<section class="spot" aria-label="Featured picks"><div class="spot-head"><h2>Editor&#39;s spotlight</h2><div class="spot-tabs">{spot_tabs}</div></div>{spot_panels}</section>'

body_home = f"""
<div class="hero" style="margin:0 -22px"><div class="wrap">
<h1>Buy right the first time, <em>Ireland</em></h1>
<p>Independent comparisons of what Irish homes actually buy — real € prices, running costs on Irish electricity, and verdicts that pick a side. No fluff, no 40 open tabs.</p>
<div class="hero-stats"><div><b>{n_guides}</b>buying guides</div><div><b>{n_prods}</b>products compared</div><div><b>{YEAR}</b>kept updated</div></div>
</div></div>
{spot_html}
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
with open(os.path.join(OUT, "CNAME"), "w") as f:
    f.write("pickireland.best\n")
open(os.path.join(OUT, ".nojekyll"), "w").close()

linked = sum(1 for v in LINKS.values() if v.get("link"))
imgs = sum(1 for v in LINKS.values() if v.get("image"))
print(f"Built {len(all_pages)} pages into {os.path.abspath(OUT)}")
print(f"Affiliate links filled: {linked} / 248 | images filled: {imgs} / 248")

# ---------------------------------------------------------------- assets: js, favicon
os.makedirs(os.path.join(OUT,"assets"),exist_ok=True)
SITE_JS = """(function(){
var rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
if(!rm&&'IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('vis');io.unobserve(e.target)}})},{threshold:.06});
document.querySelectorAll('.card,.tile,.toc,.tbl-scroll,.guide,.related a,.spot').forEach(function(el){el.classList.add('rv');io.observe(el)})}
var tb=document.querySelector('.top-btn');if(tb){addEventListener('scroll',function(){tb.classList.toggle('show',scrollY>700)},{passive:true})}
var spot=document.querySelector('.spot');
if(spot){var tabs=spot.querySelectorAll('.spot-tab'),panels=spot.querySelectorAll('.spot-panel');
function bars(p){p.querySelectorAll('.bar i').forEach(function(b){b.style.width='0%';requestAnimationFrame(function(){requestAnimationFrame(function(){b.style.width=b.dataset.w+'%'})})})}
tabs.forEach(function(t){t.addEventListener('click',function(){
tabs.forEach(function(x){x.classList.remove('on')});t.classList.add('on');
panels.forEach(function(p){p.classList.remove('on')});
var p=spot.querySelector('.spot-panel[data-k=\\"'+t.dataset.k+'\\"]');p.classList.add('on');bars(p)})});
var first=spot.querySelector('.spot-panel.on');if(first)bars(first)}
var sb=document.getElementById('siq');
if(sb){var idx=null,res=document.getElementById('sres'),ov=document.getElementById('sov');
function closeS(){document.body.classList.remove('search-open')}
document.querySelectorAll('[data-close-search]').forEach(function(b){b.addEventListener('click',closeS)});
if(ov){ov.addEventListener('click',function(e){if(e.target===ov)closeS()})}
addEventListener('keydown',function(e){if(e.key==='Escape')closeS();
if(e.key==='/'&&!document.body.classList.contains('search-open')&&!/INPUT|TEXTAREA/.test(document.activeElement.tagName)){e.preventDefault();document.body.classList.add('search-open');sb.focus()}});
function render(){var q=sb.value.trim().toLowerCase();
if(!q){res.innerHTML='<div class=\"search-hint\">Type to search every product we have reviewed — press Esc to close.</div>';return}
var out=idx.filter(function(p){return (p.n+' '+p.b+' '+p.c).toLowerCase().indexOf(q)>-1});
var seen={},uniq=[];out.forEach(function(p){if(!seen[p.n]){seen[p.n]=1;uniq.push(p)}});
res.innerHTML=uniq.slice(0,12).map(function(p){return '<a href=\"/'+p.u+'#'+p.i+'\"><span>'+p.n+'<div class=\"meta\">'+p.c+' · '+p.b+'</div></span><span class=\"sp\">€'+p.p+'</span></a>'}).join('')||'<div class=\"search-hint\">No products found for \u201C'+sb.value+'\u201D</div>'}
sb.addEventListener('input',function(){if(idx){render()}else{fetch('/assets/search.json').then(function(r){return r.json()}).then(function(d){idx=d;render()})}})}
})();"""
with open(os.path.join(OUT,"assets","site.js"),"w",encoding="utf-8") as f:
    f.write(SITE_JS)
with open(os.path.join(OUT,"assets","search.json"),"w",encoding="utf-8") as f:
    json.dump(SEARCH_INDEX,f,ensure_ascii=False)
FAV = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#12805C"/><stop offset="1" stop-color="#073F2C"/></linearGradient></defs><rect width="64" height="64" rx="15" fill="url(#g)"/><path d="M22 48V16h13a11 11 0 0 1 0 22h-9" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" fill="none"/><path d="M33 44l6 6 11-12" stroke="#FFC65C" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>'
with open(os.path.join(OUT,"favicon.svg"),"w",encoding="utf-8") as f:
    f.write(FAV)
try:
    from PIL import Image, ImageDraw
    for size,name in ((180,"apple-touch-icon.png"),(32,"favicon-32.png")):
        img=Image.new("RGBA",(size,size),(0,0,0,0)); d=ImageDraw.Draw(img)
        r=size*15//64
        d.rounded_rectangle([0,0,size-1,size-1],radius=r,fill=(11,80,57,255))
        w=max(2,size*7//64)
        def pt(x,y): return (x*size/64.0,y*size/64.0)
        d.line([pt(22,48),pt(22,16)],fill=(255,255,255,255),width=w)
        d.arc([pt(13,16)[0],pt(13,16)[1],pt(46,38)[0],pt(46,38)[1]],270,90,fill=(255,255,255,255),width=w)
        d.line([pt(22,16),pt(33,16)],fill=(255,255,255,255),width=w)
        d.line([pt(22,38),pt(30,38)],fill=(255,255,255,255),width=w)
        gw=max(2,size*6//64)
        d.line([pt(33,44),pt(39,50)],fill=(255,198,92,255),width=gw)
        d.line([pt(39,50),pt(50,38)],fill=(255,198,92,255),width=gw)
        img.save(os.path.join(OUT,name))
    print("png icons ok")
except Exception as e:
    print("PIL skip:",e)
