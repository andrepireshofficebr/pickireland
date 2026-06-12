# Campanha Google Ads DSA — PickIreland
**Objetivo:** gerar as 3 primeiras vendas com o menor gasto possível, aprendendo quais buscas convertem.
**Orçamento:** €5/dia · 14 dias · teto ~€70. Matemática esperada: ~250–300 cliques a €0,20–0,30 → ~80–100 visitas à Amazon → 3–5 pedidos.

---

## Passo 1 — Criar a campanha (ads.google.com)

1. **+ Nova campanha** → objetivo: **"Criar uma campanha sem orientação de meta"** (não escolha "Vendas" — sem histórico de conversão ele desperdiça).
2. Tipo: **Pesquisa**.
3. Resultado: Visitas ao site → `pickireland.best`.

## Passo 2 — Configurações da campanha (onde mora a economia)

| Configuração | Valor | Por quê |
|---|---|---|
| Redes | **DESMARCAR** "Parceiros de pesquisa" e "Display" | Só busca Google pura converte; o resto queima verba |
| Localização | **Irlanda** → em "Opções de local": **"Presença: pessoas em"** (não "interesse") | Brasileiro pesquisando "ireland" não compra na Amazon.ie |
| Idiomas | **Inglês** | |
| Orçamento | **€5/dia** | |
| Lances | **"Maximizar cliques"** com **teto de CPC = €0,30** | Sem teto o Google paga €1+ por clique |
| Programação | **10:00–23:00** | Compra online na Irlanda concentra à noite; corta madrugada |
| Rotação de anúncios | Otimizar | |

## Passo 3 — Grupo de anúncios dinâmico (o coração)

1. Em "Grupos de anúncios", troque o tipo para **"Dinâmico"**.
2. Fonte de segmentação: **"Usar o índice do Google do meu site"** → domínio `pickireland.best`.
3. **NÃO** use "todas as páginas da web". Crie **3 segmentações por URL** (alta intenção + ticket bom + comissão 10%):
   - URL contém: `/dehumidifiers/`
   - URL contém: `/air-fryers/`
   - URL contém: `/coffee-machines/`
4. **Exclusões de segmentação dinâmica** (Campanha → Configurações → Exclusões): URL contém `about`, `privacy`, `contact`, `disclosure`.

*Por que essas 3 categorias:* desumidificador = urgência (casa mofada não espera SEO), air fryer = volume gigante de busca, café = ticket €120–600 com 10% (€12–60/venda).

## Passo 4 — Os anúncios (DSA gera o título; você escreve 2 descrições)

**Descrição 1:**
`Compared for Irish homes: real prices in €, running costs & honest verdicts. See the top 5 before you buy.`

**Descrição 2:**
`Independent buying guides for Ireland. We compare specs, value & Irish factors — pick right in 5 minutes.`

## Passo 5 — Palavras-chave negativas (OBRIGATÓRIO — proteção da conta Amazon)

Campanha → Palavras-chave → Negativas → adicionar como **correspondência ampla**:

```
amazon
kindle
prime
free
cheap second hand
used
repair
parts
manual
instructions
rental
rent
jobs
donedeal
adverts.ie
currys
argos
harvey norman
review youtube
reddit
```

A 1ª (`amazon`) é **regra contratual da Associates** — anúncio seu aparecendo para busca com "amazon" = risco de banimento. As demais cortam curiosos que não compram.

## Passo 6 — Medir conversão de verdade (recomendado, +15 min)

Sem isso você otimiza no escuro. A "conversão" do nosso negócio = **clique no botão "Check Price on Amazon.ie"**.

1. No Google Ads: Ferramentas → **Conversões** → Nova → "Site" → nome `Clique_Amazon` → categoria "Clique de saída" → valor: nenhum → janela 1 dia.
2. Ele te dá um **ID (AW-XXXXXXX) e um rótulo**. **Me manda os dois** → eu insiro o código de rastreamento em todos os botões do site e dou push (5 min do meu lado).
3. Depois de ~30 conversões registradas, mude o lance de "Maximizar cliques" para **"Maximizar conversões"** — aí a campanha fica cirúrgica sozinha.

## Passo 7 — Rotina de piloto (10 min/dia, primeiros 7 dias)

1. Google Ads → Palavras-chave → **Termos de pesquisa**: veja o que acionou seus anúncios.
2. Termo lixo (ex: "air fryer recipes", "fix dehumidifier") → selecionar → **adicionar como negativa**.
3. Termo ouro (ex: "best dehumidifier for damp house") → anote: é candidato a virar página/post novo.
4. Página com CTR > 5% e cliques baratos → considere aumentar o orçamento só dela (duplicando o grupo).

## Avisos finais

- Os primeiros 2–3 dias o Google "aprende" — não mexa em nada antes do dia 4.
- NUNCA linke anúncio direto pra Amazon (banimento), sempre pro seu site — como está configurado aqui.
- Meta da campanha: 3 vendas + relatório de termos. Atingiu as 3 vendas → pode pausar e deixar o SEO trabalhar; o relatório de termos vale o investimento sozinho.
