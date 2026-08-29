# PickIreland — registro semanal do motor

Este arquivo é a memória entre execuções da tarefa agendada de sábado.
**Cada execução lê o bloco mais recente antes de medir, e acrescenta o seu no topo.**

Existe porque na execução de 29/08/2026 as ferramentas `project_memory_read` /
`project_memory_write` não estavam disponíveis na sessão. Um arquivo em `C:\ireland`
não depende de nenhuma ferramenta: o motor sempre alcança essa pasta.

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
