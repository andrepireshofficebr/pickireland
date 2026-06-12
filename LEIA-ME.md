# PickIreland — Manual de Operação

Site de comparativos para o mercado irlandês: **65 páginas** (50 comparativos "top 5", 10 hubs de categoria, home + 4 institucionais), **250 produtos**, SEO completo (schema.org Product/FAQ/Breadcrumb, sitemap, meta tags, canonical).

## Estrutura

```
pickireland/
├── site/                  ← O SITE PRONTO (suba esta pasta para a hospedagem)
├── generator/
│   ├── build.py           ← gerador: lê os dados + planilha e monta o site
│   ├── affiliate_links.xlsx  ← SUA PLANILHA: cole os links de afiliado aqui
│   └── data/              ← conteúdo das 10 categorias (editável)
└── LEIA-ME.md
```

## Fluxo de trabalho (o ciclo que você vai repetir)

1. Cadastre-se em https://affiliate-program.amazon.ie (receba via Wise/Payoneer em EUR).
2. Abra `generator/affiliate_links.xlsx`. Cada linha tem um link clicável **"abrir produto →"** (coluna H) que abre a busca daquele produto no Amazon.ie. Na página do produto, copie seu link de afiliado pelo SiteStripe e cole na coluna amarela **affiliate_link** (I). Opcional: cole a URL de uma imagem do produto em **image_url** (J) — ela aparece no card; sem imagem, o card mostra um placeholder elegante com a marca. Pode atualizar o preço em **price_eur** também — o site usa o valor da planilha.
3. Rode na pasta `generator`:
   ```
   python build.py
   ```
   (precisa de Python + `pip install openpyxl`)
4. Suba a pasta `site/` para a hospedagem. Pronto: todos os botões "Check Price on Amazon.ie" usam seus links (com `rel="sponsored"`, como o Google exige).

Produtos sem link apontam para a busca do Amazon.ie — o site funciona, mas sem comissão. Priorize preencher as páginas principais (`best-X-ireland`) de cada categoria.

## Publicação — GitHub Pages + domínio pickireland.best (já configurado)

O build já gera `CNAME` e `.nojekyll`, e todo o SEO (canonical/sitemap) já aponta para https://pickireland.best.

1. Em github.com: New repository → nome `pickireland` → Public → Create.
2. "Uploading an existing file" → arraste TUDO que está DENTRO da pasta `site/` (não a pasta em si) → Commit.
3. Settings → Pages → Source: "Deploy from a branch" → Branch `main` / `/ (root)` → Save.
4. Em Pages → Custom domain: digite `pickireland.best` → Save.
5. Na Namecheap (Domain List → Manage → Advanced DNS):
   - 4 registros **A** com Host `@` apontando para: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - 1 registro **CNAME** com Host `www` apontando para `SEU-USUARIO.github.io.`
   - Apague registros A/CNAME antigos de parking que existirem.
6. Aguarde a propagação (minutos a algumas horas) e marque **Enforce HTTPS** no GitHub Pages.

Cada atualização futura: rode `python build.py` e suba os arquivos alterados de novo no repositório (ou use GitHub Desktop pra facilitar).

## Pós-publicação (não pule)

1. **Google Search Console**: adicione o domínio e envie `sitemap.xml`.
2. **Bing Webmaster Tools**: idem (Bing tem tráfego na Irlanda).
3. **Regra das 3 vendas**: a conta Amazon Associates só é confirmada com 3 vendas em 180 dias. Acelere com Pinterest, Reddit (r/ireland com cuidado e transparência) e Google Ads DSA apontando para o site (nunca link direto para a Amazon, nunca bidar em "amazon").
4. Atualize preços na planilha a cada 4–6 semanas e rode o build — "Updated [data]" se renova sozinho.

## Editando conteúdo

Todo o conteúdo está em `generator/data/*.json` (textos, produtos, FAQs). Edite e rode `build.py`. Para adicionar páginas novas, copie o formato de uma página existente dentro de `pages`.

## Importante (honestidade)

- Preços e specs foram preenchidos como valores típicos de mercado — **revise os produtos das páginas que priorizar** contra a página real do Amazon.ie ao colar cada link (2 min por produto). Modelos saem de linha; troque pelo sucessor na planilha/JSON quando notar.
- A linha "As an Amazon Associate..." no topo é exigência contratual da Amazon — não remova.
