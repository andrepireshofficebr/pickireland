# PickIreland — Plano de Crescimento
**Versão 1 · 15 de agosto de 2026 · aprovado por André Pires**

---

## 1. A meta

**Chegar a 10 vendas qualificadas numa janela móvel de 30 dias.**

Não é um número escolhido por gosto. É o limite exato que a Amazon exige para liberar a
Creators API (sucessora da PA-API), e a API é o **único** canal autorizado para usar imagem
de produto. Hoje o site tem **zero imagens para 304 produtos**.

Cruzar essa linha resolve quatro problemas de uma vez: as imagens entram automáticas e
permanentes, a conversão sobe, os preços passam a se atualizar sozinhos, e o acesso se
mantém enquanto houver venda.

**Toda decisão deste plano se julga por uma pergunta: isso aproxima das 10 vendas em 30 dias?**

### Prazo honesto
Hoje: **150 sessões / 28 dias**, 2 vendas no total (desde o lançamento).
Para 10 vendas mensais a ~3,5% de conversão: entre **1.000 e 1.400 sessões/mês** — sete a
nove vezes o volume atual.

Sem tráfego pago, num domínio de 3 meses com zero backlinks, isso é trabalho de
**3 a 6 meses**. O plano assume esse horizonte. Qualquer promessa de 30 dias seria mentira.

---

## 2. Onde estamos (medido, não estimado)

| Fato | Valor | Fonte |
|---|---|---|
| Sessões (28 dias) | **150** | GA4, propriedade 541544668 |
| Canal nº1 | **AI Assistant — 55 sessões (36,7%)** | GA4, aquisição de tráfego |
| Direct | 67 (44,7%), engajamento 14s — o pior | GA4 |
| Busca do Google | 24 (16%), mas o **melhor** engajamento (58,3%, 39s) | GA4 |
| Cliques no Search Console (90 dias) | 9 | GSC |
| Páginas indexadas | **14 de 65** | GSC |
| Último rastreamento da maioria | **15 de junho de 2026** | GSC, inspeção de URL |
| Backlinks | **zero** | busca por menções à marca |
| Imagens de produto | **zero** para 304 produtos | varredura do HTML |

**A leitura que importa:** o site já funciona — só que por um canal que ninguém estava
olhando. Assistentes de IA trazem mais gente que a Busca do Google, e com engajamento
melhor que o tráfego direto. O trabalho de GEO de julho (robots.txt liberando 14 crawlers,
`llms.txt` de 106 linhas, blocos de resposta rápida, Speakable) era hipótese; virou canal
comprovado.

---

## 3. Restrições — o que NÃO dá para fazer, e por quê

**Imagem de produto só pela API.** Baixar, tirar print ou re-hospedar imagem da Amazon
viola o Operating Agreement, e a pena é perder a conta de afiliado — o que zera a receita
dos 304 links no mesmo instante. O recurso de imagem do SiteStripe foi **desativado em
dezembro de 2023**; ele hoje só dá link de texto. Gerar a foto com IA seria um desenho
parecido, não o produto, e engana o leitor. **Não há atalho.** Detalhe e fontes em
`pickireland-imagens-amazon` na memória do projeto.

**Sem tráfego pago.** Decisão do André. A campanha DSA fica pausada. Isso alonga o prazo,
e está contabilizado no horizonte de 3 a 6 meses.

**Publicar depende de um clique do André.** O `git push` a partir da minha sessão é
recusado pelo proxy (`not in this session's authorized repository set`). Ele publica pelo
GitHub Desktop. **Testar logo, numa sessão nova, se a vinculação que ele fez em 15/08
passou a valer** — se sim, a automação fica muito mais fluida.

**Meu tempo não é o gargalo; o dele é.** Tudo que exigir presença humana com voz própria
(fórum irlandês, relacionamento) fica fora da execução automática e entra como sugestão.

---

## 4. As quatro frentes

### Frente 1 — Amplificar o canal de IA
*A mais barata, a única com vantagem competitiva real, e a que já dá retorno.*

Os varejistas que esmagam o site no Google — Currys, DID, Harvey Norman, Expert.ie —
**não otimizam para IA**. O canal onde o site é fraco é o mais disputado; o canal onde já
ganha é o que ninguém trabalha.

1. **Descobrir qual assistente traz as 55 sessões.** Quebrar `AI Assistant` e `Direct` por
   origem/mídia no GA4. Sem isso, "otimizar para IA" é chute. *(Tentei em 15/08; o seletor
   de dimensão do GA4 não respondeu a clique automatizado três vezes. Tentar pelo relatório
   "Aquisição de usuários" ou por Explorações.)*
2. **Gráficos de dados em todas as guias.** Custo de operação em €/hora, extração por litro,
   peso vs autonomia — gerados por código a partir das specs de 295 produtos e da tarifa
   SEAI de €0,38/kWh. Mesmo mecanismo que já gera as 10 imagens OG de categoria.
   **É o único ativo visual possível hoje**, e resolve dois problemas: conversão (o site não
   tem imagem nenhuma) e citabilidade (IA cita número com fonte).
3. **Blocos de fato extraíveis.** Ampliar o padrão de `.quick-answer` e `Speakable` para que
   cada guia ofereça uma resposta autocontida por pergunta, no formato que um motor
   generativo consegue levantar inteiro.
4. **`llms.txt` vivo.** Passar a incluir os números de custo por produto, não só a descrição
   das guias.

### Frente 2 — Destravar o Google
*Necessária, mas é o caminho lento. Não esperar retorno antes de 8 semanas.*

1. **Terminar os pedidos de indexação.** Cota de ~10 URLs/dia. Faltam 3 hubs
   (`/electric-scooters/`, `/home-office/`, `/robot-lawn-mowers/`) e as 40 sub-guias.
   **Sempre a URL canônica** — pedir `/categoria/`, nunca `/categoria/index.html`.
2. **Auditoria de coerência canônica, recorrente.** O bug de 15/08 (sitemap declarando
   `/cat/index.html` contra canonical `/cat/`) só apareceu porque comparei os dois conjuntos.
   Virou checagem permanente: *o conjunto de `<loc>` do sitemap tem de ser idêntico ao
   conjunto de canonicals das páginas.*
3. **Conteúdo informacional.** Onde varejista não compete: "how much does a dehumidifier cost
   to run in Ireland", "e-scooter law Ireland 2026", "Cycle to Work e-bike 2026",
   "why is my house so damp in Ireland". Ranqueiam mais fácil, constroem autoridade tópica e
   apontam para as páginas comerciais.

### Frente 3 — Sinais externos
*Ataca o zero backlinks, que é o input que falta para o Google voltar a rastrear.*

1. **O ativo linkável.** Tabela pública do custo real de operação em €/hora dos ~30
   desumidificadores comparados, com metodologia aberta e a tarifa SEAI citada.
   Ninguém linka para "os 5 melhores desumidificadores"; muita gente linka para
   "quanto custa rodar um desumidificador na Irlanda, com os números".
2. **Perfis de marca.** Pinterest (funciona bem para conteúdo comparativo com imagem —
   e agora haverá gráficos), Facebook, X, LinkedIn. São links nofollow, mas são sinais de
   entidade: dizem ao Google que existe uma marca por trás do domínio.
3. **Comunidades irlandesas — depende do André.** boards.ie, r/ireland, r/AskIreland.
   Participação real, linkando só quando o link for a melhor resposta. **Não posso fazer
   isso por ele**; fica como sugestão, não como tarefa.

### Frente 4 — A máquina de conteúdo
*Como as 10 categorias no máximo se tornam viáveis.*

Pipeline de agentes em paralelo, por artigo:
**pesquisa → redação → conferência de cada número contra a fonte → revisão de voz → publicação.**

A conferência é a etapa crítica e precisa ser adversarial, não complacente: cada afirmação
numérica é checada contra o dado de origem, e cada afirmação factual contra a fonte primária
(SEAI, irishstatutebook.ie, Met Éireann, site do fabricante).

**André decidiu que os agentes publicam direto, sem leitura dele.** Registrado na seção de
riscos com a ressalva devida.

---

## 5. Automação

### Tarefa semanal — sábado de manhã
O motor do plano. Cada execução, na ordem:

1. Lê GA4 e Search Console e **compara com a semana anterior**: sessões por canal,
   páginas indexadas, posição média, contagem de vendas rumo às 10.
2. Produz o entregável da semana, seguindo a fila da seção 7 (nunca "o que parecer
   melhor na hora" — a ordem está definida).
3. Roda a auditoria de coerência (sitemap vs canonicals, IndexNow, `lastmod`).
4. Deixa tudo pronto em `C:\ireland` e envia um resumo curto: o que mudou, o que foi
   produzido, e **os passos exatos para publicar**.

### Tarefa diária — dias úteis, temporária
Só os pedidos de indexação, respeitando a cota de ~10/dia. Esvazia a fila de 45 páginas em
cerca de uma semana. **Depois disso, apagar a tarefa.**

### Degradação graciosa
Ambas dependem do computador do André ligado com o app aberto (o acesso ao GA4, ao GSC e
aos arquivos passa por ali). Se estiver offline, a tarefa **faz o que consegue sem o
navegador, e diz explicitamente o que ficou faltando** — nunca finge que rodou inteira.

---

## 6. Riscos registrados

| Risco | Gravidade | Postura |
|---|---|---|
| **Prazo real de 3-6 meses**, não 30 dias | Alta | Declarado. Medir por sessões e indexação, não por vendas, nos 2 primeiros meses. |
| **Agentes publicam sem revisão humana** | Alta | Decisão do André. Este projeto já teve **três** rodadas em que a validação automática passou 100% limpa com conteúdo factualmente errado. Mitigação: conferência adversarial de cada número contra a fonte, e o resumo semanal sempre diz o que foi publicado, para dar chance de desfazer. **A mitigação reduz o risco; não o elimina.** |
| **10 categorias no máximo dilui o esforço** | Média | Decisão do André, contra minha recomendação de concentrar em 2-3. Documentado. Reavaliar em 3 meses com dado na mão: se nenhuma categoria emergir, concentrar. |
| **Sem tráfego pago, a meta pode não ser atingida** | Média | Aceito. Se em 3 meses o volume não estiver em trajetória, reabrir a conversa sobre a DSA. |
| **Publicação depende de clique do André** | Média | Testar a vinculação do repositório numa sessão nova. Se falhar de novo, o GitHub Desktop continua sendo o caminho. |
| **Automação depende do PC ligado** | Baixa | Degradação graciosa e aviso explícito do que faltou. |

---

## 7. Ordem de execução — as primeiras seis semanas

A fila é fixa. Cada sábado consome o próximo item. Se uma semana render mais, adianta a fila;
não substitui itens por improviso.

**Semana 0 (sessão de execução, não é sábado)**
- Testar se o `git push` funciona numa sessão nova. Isso define se a publicação continua
  dependendo do GitHub Desktop.
- Criar as duas tarefas agendadas.
- Descobrir qual assistente de IA traz as 55 sessões. **É pré-requisito da Frente 1** —
  sem esse dado, as semanas 2 e 3 são chute.

**Semana 1** — Gráficos de custo de operação para dehumidifiers (a categoria com tração
comprovada). Serve de molde para as outras nove.

**Semana 2** — O ativo linkável: tabela pública de custo €/hora dos ~30 desumidificadores,
com metodologia aberta e fonte SEAI citada. É o item da Frente 3 que ataca o zero backlinks.

**Semana 3** — Primeiro artigo informacional: *"How much does a dehumidifier cost to run in
Ireland"*. Usa os dados da semana 2, linka para as 5 guias comerciais de desumidificador.
**É também o teste do pipeline de agentes** — se a conferência de fatos falhar aqui, corrigir
o pipeline antes de escalar.

**Semana 4** — Gráficos para electric-heaters e air-fryers (mesmo ângulo de conta de luz).

**Semana 5** — Segundo artigo informacional: *"E-scooter law Ireland 2026"* (o S.I. 199/2024
já está verificado no site) ou *"Cycle to Work scheme e-bike 2026"*.

**Semana 6** — Perfis de marca (Pinterest primeiro, agora que há gráficos para publicar) e
primeira reavaliação com dado: o Google voltou a rastrear?

Depois da semana 6, a fila continua alternando **gráficos de categoria** e **artigo
informacional**, até cobrir as 10 categorias.

---

## 8. Como saber se está funcionando

| Janela | Métrica | Sinal de sucesso |
|---|---|---|
| 2 semanas | Páginas conhecidas no GSC | Sair de 20. Se não sair, o problema é mais profundo que atraso de rastreamento. |
| 4 semanas | Data do último rastreamento | Passar de 15/06 para algo recente. É a confirmação de que o Google voltou. |
| 8 semanas | Sessões por canal no GA4 | Total acima de 300/28 dias. Posição média caindo de 49,5. |
| 12 semanas | Sessões e vendas | 600+ sessões/28 dias e vendas em trajetória para 10/mês. |
| 3 meses | Decisão | Reavaliar concentração de categorias e a questão do tráfego pago, com dado real. |

**Não medir por impressões.** Elas oscilam e podem cair justamente quando o Google
reavalia o site. A métrica que importa nesta fase é **sessões por canal no GA4** —
o Search Console mede 16% do negócio.
