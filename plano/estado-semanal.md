# PickIreland — registro semanal do motor

Este arquivo é a memória entre execuções da tarefa agendada de sábado.
**Cada execução lê o bloco mais recente antes de medir, e acrescenta o seu no topo.**

Existe porque na execução de 29/08/2026 as ferramentas `project_memory_read` /
`project_memory_write` não estavam disponíveis na sessão. Um arquivo em `C:\ireland`
não depende de nenhuma ferramenta: o motor sempre alcança essa pasta.

---

## 2026-09-05 (sábado) — Semana 3 da fila

### Números medidos

**GA4 (propriedade 541544668), sessões por canal, 8 de agosto – 4 de setembro de 2026**

| Canal | Sessões | % | Engajamento | Tempo médio |
|---|---|---|---|---|
| Direct | 48 | 40,0% | 22,9% | 3s |
| AI Assistant | 36 | 30,0% | 38,9% | 22s |
| Organic Search | 30 | 25,0% | 40,0% | 47s |
| Unassigned | 6 | 5,0% | 16,7% | 1min17s |
| Referral | 1 | 0,8% | 100% | 1min |
| **Total** | **120** | | 32,5% | 24s |

**GA4 — origem da sessão, mesmos 28 dias** (busca do topo → "top 20 session sources by
sessions last 28 days" → 1ª sugestão; o seletor de dimensão da tabela continua sem responder
a clique automatizado)

(direct) 49 · **chatgpt.com 37** · google 13 · duckduckgo 8 · bing 6 · (not set) 4 ·
perplexity 3 · ecosia.org 2 · (data not available) 1 · **gemini.google.com 1** ·
nl.search.yahoo.com 1 · search.brave.com 1

**Search Console (sc-domain:pickireland.best), 7 de agosto – 3 de setembro**

| Métrica | Valor |
|---|---|
| Cliques | 12 |
| Impressões | 5,69 mil |
| CTR | 0,2% |
| Posição média | 51,9 |
| **Páginas indexadas** | **22** |
| Não indexadas | 52 (45 "detectada, não indexada"; 2 "rastreada, não indexada"; 3 redirect; 2 canônica alternativa) |

### Comparação com 29/08

| Métrica | 29/08 | 05/09 | Δ |
|---|---|---|---|
| Sessões / 28d | 128 | 120 | −8 |
| AI Assistant | 36 | 36 | **0 — estabilizou** |
| chatgpt.com (origem) | 35 | 37 | +2 |
| Organic Search | 28 | 30 | +2 |
| Direct | 59 | 48 | −11 |
| Páginas indexadas | 22 | 22 | **0 — parou** |
| Posição média | 50,3 | 51,9 | −1,6 (pior) |
| Cliques | 11 | 12 | +1 |

**Leitura honesta:** a queda do total é quase toda Direct (−11), o canal com o pior
engajamento (3s de média). Os dois canais que importam não caíram: o ChatGPT subiu de 35 para
37 e a busca orgânica de 28 para 30. **O que preocupa é a indexação parada em 22 há duas
semanas** — a meta de 2 semanas da seção 8 foi batida em 29/08 e desde então não andou.
Apareceu gemini.google.com com 1 sessão (primeira vez). Base pequena; nada aqui é tendência
com dois pontos.

### O que foi produzido

**Semana 3 da fila — o primeiro artigo informacional.**
Nova página: `/dehumidifiers/how-much-does-a-dehumidifier-cost-to-run-ireland.html`
("How much does a dehumidifier cost to run in Ireland?"), ~1.620 palavras.

Por que é uma página separada da tabela da semana 2: a tabela responde "qual modelo custa
quanto" (referência, por modelo); a busca real é uma pergunta única que quer um número e o
raciocínio. Intenções diferentes → páginas diferentes, cada uma linkando para a outra em
prosa para não haver dúvida sobre qual é qual.

Conteúdo: resposta rápida, as três variáveis da conta com a aritmética à vista, tabela de
três cenários (menor consumo / típico / maior), a seção "quando você liga vale tanto quanto
qual você compra", custo por litro, comparação com aquecedor, "o que estes números não são",
5 FAQs, links para a tabela e para as 5 guias comerciais. JSON-LD: `Article` + `WebPage`
(Speakable) + `FAQPage` (5 perguntas) + `BreadcrumbList`.

**Regra que essa página segue:** nenhum número vem de fora dos dados do próprio site. A
comparação com aquecedor usa as potências reais da categoria `electric-heaters` (26 modelos,
moda 2000 W). Não há figura de secadora — e a FAQ sobre secadora diz explicitamente que não
publicamos o número porque não o verificamos, e ensina a conta.

### Conferência adversarial — três afirmações corrigidas antes de publicar

1. **A faixa da resposta rápida começava em €0,01/hora.** Verdade aritmética (o Belaco de
   36 W), mentira prática: é um mini de 0,3 L/dia. Corrigido para a faixa das máquinas de
   tomada (€0,04–€0,13) com o mini declarado à parte.
2. **"Trocar o modelo de 185 W pelo de 101 W economiza €7,66/mês".** Comparação inválida: o
   de 101 W extrai 6 L/dia e o de 185 W extrai 12 — não entregam o mesmo trabalho. Reescrito
   para comparar só dentro do maior grupo de extração igual (7 modelos de 12 L/dia,
   136–210 W, €6,75/mês de diferença) contra a economia de tarifa (€8,88/mês).
3. **"Se sua máquina tem timer — a maioria das nossas tem".** Não temos dado de timer.
   Removido.

### Armadilha encontrada e corrigida (a mesma família de 22/08 e 29/08)

A primeira versão acrescentou `art_link` à lista de hash da página de referência
**incondicionalmente**. Nas 3 categorias sem artigo ele é `""`, mas o separador `"||"` sozinho
mudava o hash: 6 páginas marcadas como modificadas em vez de 3, sendo que o HTML delas era
byte a byte idêntico. Corrigido com `+ ([art_link] if art_link else []) +`.
**Lição, agora pela terceira vez: item opcional nunca entra numa lista de hash como string
vazia; ou entra o valor, ou não entra nada.**

### Mudanças no gerador (`build.py`)

- `RC_ARTICLES`: config dos artigos, ao lado de `RC_REF_PAGES` (fica lá em cima porque o hub
  e a página de referência precisam saber que o artigo existe para linkar).
- `running_cost_article(cat)`: gera o artigo. Escolhe sozinho o grupo de extração igual, o
  modelo mediano, a moda de potência dos aquecedores e a faixa das máquinas de tomada.
- `rc_reference_page()`: `art_link` na lista de guias + no hash (condicional).
- Hub: `hub_art` colado no mesmo `<div>` do `hub_ref` (lição de 29/08).
- `llms.txt`: nova seção "Running costs: reference tables and explainers" — as páginas de
  referência não apareciam no índice para LLMs. `llms-full.txt` também linka o artigo.
- Backup: `generator/build.py.pre-article` e `generator/.page_dates.json.pre-article`.

### Checagens de coerência (todas passaram)

- sitemap `<loc>` ≡ conjunto de canonicals: **70 = 70**, nenhuma sobrando nem faltando.
- `lastmod` = hoje em **3 URLs** e só nelas: o artigo novo, a página de referência de
  desumidificador (ganhou o link) e o hub de desumidificadores.
- Verificação de churn: rebuild da versão anterior num diretório temporário e diff contra o
  build de hoje → **exatamente 7 arquivos diferem** (o artigo novo, a página de referência, o
  hub, `sitemap.xml`, `llms.txt`, `llms-full.txt`, `google-ads-page-feed.csv`). Nenhuma outra
  página, nenhum asset, nenhum favicon.
- IndexNow: 70 URLs, **zero** terminando em `index.html`. Um único arquivo de chave.
- JSON-LD do artigo: `Article`, `WebPage`, `FAQPage` (5), `BreadcrumbList` — todos parseiam.
- Title 52 caracteres, description 140 — dentro dos limites; nenhum aviso `[SEO]` na build.

### Descoberta importante: o clone do OneDrive estava 2 commits atrás do site

O `main` no GitHub tem dois commits de **01/09** que **não existem** no clone
`C:\Users\andre\OneDrive\Documentos\GitHub\pickireland`:
`llms-full.txt: corpus completo em texto puro para agentes de IA` (a3900f7) e
`Custo de operacao: 74 cards novos + 3 paginas de referencia` (756aa8a).
Ambos estão **no ar** (confirmado: `/air-fryers/air-fryer-running-costs-ireland.html`
responde e a tabela de desumidificador ainda mostra a versão antiga, de 7 modelos com
potência). Ou seja, houve uma sessão em 01/09 que produziu e publicou por outro caminho e
**não atualizou este clone nem este arquivo de estado**.

Consequência prática: ao copiar o build de hoje para o clone, o GitHub Desktop vai mostrar
~60 arquivos alterados (os 55 do trabalho de 01/09 + os 7 de hoje). O conteúdo copiado é
superconjunto do que está no `main`, então **em caso de conflito a versão certa é sempre a
do computador dele**.

### Entrega

Copiado para `C:\Users\andre\OneDrive\Documentos\GitHub\pickireland`: `docs/` inteiro,
`generator/build.py`, `generator/.page_dates.json`, `generator/indexnow_submit.py`,
`generator/data/`. Verificado por diff: origem e clone idênticos. `.env` e `.github_token`
**não** foram copiados. **Nenhum comando git foi executado no clone.**

Nota: existe um diretório duplicado `generator/data/data/` no clone desde 15/08. Não foi
criado hoje e não foi mexido — vale limpar numa próxima sessão.

### Estado da fila (seção 7 do plano)

- Semana 1 (gráficos de custo, dehumidifiers) — feita 22/08, **publicada**
- Semana 2 (ativo linkável €/hora) — feita 29/08, **publicada**
- Semana 4 (gráficos heaters + air-fryers, e ainda air-purifiers) — feita **fora de ordem**
  em 01/09, **publicada**. A pesquisa de potência fechou a lacuna: 74 cards ganharam watts.
- Semana 3 (artigo informacional) — **feita em 05/09, aguardando publicação**
- **Próxima: Semana 5** — segundo artigo informacional: *"E-scooter law Ireland 2026"*
  (S.I. 199/2024, já verificado no site) ou *"Cycle to Work scheme e-bike 2026"*.
  Depois, Semana 6: perfis de marca + reavaliação.

### Pendências

- **Indexação parada em 22 há duas semanas.** É o sinal para investigar na próxima execução:
  as 45 URLs "detectada, mas não indexada" nunca foram rastreadas. A tarefa diária de pedidos
  de indexação (seção 5 do plano) foi criada? Está rodando?
- IndexNow **não foi disparado** — a página ainda não está no ar. Depois do push:
  `python3 generator/indexnow_submit.py --all`.
- `project_memory_read` / `project_memory_write` e `device_list_dir` /
  `mcp__claude-code-remote__send_later`: **continuam não existindo** nesta sessão. O acesso ao
  PC funcionou pelos arquivos e pelo shell. Este arquivo segue sendo a memória.

---

## 2026-08-29 (sábado) — Semana 2 da fila

### Números medidos

**GA4 (propriedade 541544668), sessões por canal, 1–28 de agosto de 2026**

| Canal | Sessões | % | Engajamento | Tempo médio |
|---|---|---|---|---|
| Direct | 59 | 46,1% | 35,6% | 14s |
| AI Assistant | 36 | 28,1% | 38,9% | 18s |
| Organic Search | 28 | 21,9% | 46,4% | 55s |
| Unassigned | 5 | 3,9% | 20% | 10s |
| Referral | 1 | 0,8% | 100% | 1min |
| **Total** | **128** | | 39,1% | 24s |

**GA4 — origem da sessão, 1–28 de agosto (resolve o pré-requisito da Frente 1)**

(direct) 61 · **chatgpt.com 35** · google 12 · bing 8 · (not set) 4 · duckduckgo 4 ·
perplexity 3 · ecosia.org 2 · claude.ai 1 · nl.search.yahoo.com 1 · search.brave.com 1 ·
uk.search.yahoo.com 1

→ **O canal de IA é o ChatGPT.** 35 das 36 sessões de "AI Assistant". Perplexity (3) e
claude.ai (1) são residuais. O ChatGPT Search se alimenta do índice do Bing — o que
justifica manter o IndexNow ligado e o robots.txt liberando OAI-SearchBot/GPTBot.
Método que funcionou: busca do topo do GA4 → "top 20 session sources by sessions last 28
days" → 1ª sugestão. O seletor de dimensão da tabela continua não respondendo a clique.

**Search Console (sc-domain:pickireland.best)**

| Métrica | 28 dias (30/07–26/08) |
|---|---|
| Cliques | 11 |
| Impressões | 4.910 |
| CTR | 0,2% |
| Posição média | 50,3 |
| **Páginas indexadas** | **22** |
| Não indexadas | 52 (45 "detectada, não indexada"; 2 "rastreada, não indexada"; 3 redirect; 2 canônica alternativa) |

### Comparação com a linha de base do plano (15/08/2026)

| Métrica | 15/08 | 29/08 | Δ |
|---|---|---|---|
| Sessões / 28d | 150 | 128 | **−22 (−15%)** |
| AI Assistant | 55 | 36 | **−19** |
| Organic Search | 24 | 28 | **+4** |
| Direct | 67 | 59 | −8 |
| Páginas indexadas | 14 | **22** | **+8** |
| Posição média | 49,5 | 50,3 | −0,8 (pior) |

**Leitura honesta:** a indexação está funcionando (+8 páginas, meta de 2 semanas da seção 8
batida). O tráfego caiu, puxado pelo canal de IA. Não há explicação medida para a queda —
pode ser sazonalidade, mudança no ChatGPT Search, ou ruído em base pequena. **Não tratar
como tendência antes de mais um ou dois pontos.**

### O que foi produzido

**Semana 2 da fila — o ativo linkável.**
Nova página: `/dehumidifiers/dehumidifier-running-costs-ireland.html`
("What a dehumidifier actually costs to run in Ireland").

- Tabela com os **7 desumidificadores que publicam potência**: W, €/hora dia (€0,38/kWh),
  €/hora noite (€0,18/kWh), €/mês a 8h/dia, extração nominal, **€/litro removido**.
  Faixa: €0,04–€0,13/hora; €9,21–€30,10/mês.
- Segunda tabela com os **10 modelos sem potência publicada**, declarados como tal.
  Nunca estimados.
- Metodologia aberta em 5 passos com a aritmética à vista, tarifa citada (SEAI + tarifas
  padrão de fornecedores, julho/2026), e três ressalvas: é teto e não conta; extração é
  número de laboratório (30 °C / 80% HR) logo o €/litro real é pior; não inclui taxa fixa.
- Convite explícito a citar com link — é isso que ataca o zero backlinks.
- JSON-LD `Dataset` + `WebPage` (com Speakable) + `BreadcrumbList`.
- Ponte interna: as 4 guias com gráfico e o hub linkam para ela.

**Descoberta importante sobre os dados:** o plano falava em "~30 desumidificadores".
São **17 modelos únicos** — os 34 registros incluem o mesmo aparelho repetido em guias
diferentes com ids diferentes. A página deduplica por nome. Só 7 dos 17 publicam potência.
**Fechar essa lacuna (buscar a potência dos 10 na documentação do fabricante) é o maior
ganho disponível para esta página** e é candidato natural a item de fila.

### Mudanças no gerador (`build.py`)

- `RC_REF_PAGES`: config por categoria da página de referência. Semana 4 (heaters,
  air-fryers) é só acrescentar uma entrada — **incluindo `ceiling_note` e `unit_note`
  próprios**, porque a física da categoria muda (o erro de 22/08 foi texto único).
- `_extraction_lpd()` (parser de L/dia, aceita ml/dia, nunca chuta) e `_unique_products()`
  (dedupe por nome).
- `KWH_RATE_NIGHT = 0.18`, `RC_REF_HOURS_DAY = 8`.
- `running_cost_chart()` ganhou `more_href`/`more_text`.
- Backup: `generator/build.py.pre-refpage`.

### Armadilha encontrada e corrigida nesta execução

A primeira versão colocou `{hub_ref}` **em linha própria** no template do hub. Nas 9
categorias sem página de referência ele rendia string vazia — mas **a quebra de linha
sobrava** e mudava o hash das 9 páginas: 15 páginas marcadas como modificadas em vez de 6.
Frescor falso, exatamente o que o mecanismo de `lastmod` existe para impedir. Corrigido
colando `{hub_ref}` na mesma linha do `</div>` anterior. **Lição: qualquer bloco opcional
no template tem de ser colado, nunca em linha própria.**

### Checagens de coerência (todas passaram)

- sitemap `<loc>` ≡ conjunto de canonicals: **66 = 66**, nenhuma faltando.
- `lastmod` = hoje em **6 URLs**, e só nelas: 4 guias de desumidificador (a 5ª,
  bedroom, tem só 2 produtos com potência, abaixo do mínimo de 3 do gráfico, então não
  mudou — correto), o hub e a página nova.
- IndexNow: 66 URLs, **zero** terminando em `index.html`. Um único arquivo de chave.
- JSON-LD da página nova: `Dataset`, `WebPage`, `BreadcrumbList` — todos parseiam.
- Links internos da página nova: nenhum quebrado.
- Imagens OG e favicons: **byte a byte idênticos** (build no Linux não gerou churn).

### Entrega

Copiado para `C:\Users\andre\OneDrive\Documentos\GitHub\pickireland`: `docs/` inteiro,
`generator/build.py`, `generator/.page_dates.json`, `generator/indexnow_submit.py`,
`generator/data/`. Verificado: origem e clone idênticos. `.env` e `.github_token` **não**
foram copiados. **Nenhum comando git foi executado no clone.**

Confirmado no ar antes de copiar: o trabalho de 22/08 (gráficos de custo) **está publicado**
— `.rcbars` presente em pickireland.best. Ou seja, André publicou a semana 1.

### Estado da fila (seção 7 do plano)

- Semana 1 (gráficos de custo, dehumidifiers) — **feita em 22/08, publicada**
- Semana 2 (ativo linkável €/hora) — **feita em 29/08, aguardando publicação**
- Semana 3 (artigo "How much does a dehumidifier cost to run in Ireland") — **próxima**.
  Usa os dados desta página e linka para as 5 guias comerciais. É o teste do pipeline
  de agentes.

### Pendências e ferramentas que faltaram

- `project_memory_read` / `project_memory_write`: **não existem nesta sessão**. Por isso
  este arquivo. A tarefa agendada deveria ser atualizada para ler
  `C:\ireland\plano\estado-semanal.md` no PASSO 0.
- `device_list_dir` / `mcp__claude-code-remote__send_later`: **não existem nesta sessão**.
  O acesso ao PC funcionou pelas ferramentas de arquivo e pelo shell (C:\ireland montado),
  então a execução seguiu normalmente. Se um dia o acesso a `C:\ireland` falhar, não haverá
  ferramenta de reagendamento — o motor deve apenas relatar e parar.
- IndexNow **não foi disparado** — a página ainda não está no ar. Disparar depois do push:
  `python3 generator/indexnow_submit.py --all` (ou sem `--all` para só as alteradas).
