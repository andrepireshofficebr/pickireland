# O que mudou em 19/09/2026 e como publicar

Tudo já está construído em `C:\ireland\docs` **e já copiado** para o seu clone
`C:\Users\andre\OneDrive\Documentos\GitHub\pickireland`. Falta só o commit e o push.

## Como publicar (GitHub Desktop)

1. Abra o **GitHub Desktop**. Ele deve mostrar os arquivos alterados na lista da esquerda
   (pode aparecer mais do que as 11 mudanças de hoje — explicação no fim desta página).
2. No canto **inferior esquerdo** há dois campos. Escreva no de **cima**, o campo curto
   chamado **Summary**:
   `Corrige limite legal de 25 para 20 km/h e publica a pagina da lei do patinete`
   — se escrever só no campo de baixo (**Description**), o botão azul não habilita.
3. Clique no botão azul **Commit to main**, logo abaixo desses campos.
4. Olhe para o **topo da janela**. O botão que antes dizia outra coisa agora diz
   **Push origin**. **Clique nele.** Commit e push são dois passos separados — sem o
   push nada vai para o ar.
5. Espere 1–2 minutos e abra:
   https://pickireland.best/electric-scooters/e-scooter-law-ireland-2026.html

## Depois de publicar, olhe uma coisa que eu não consigo ver

`github.com/andrepireshofficebr/pickireland` → aba **Actions** → workflow **IndexNow**.
Ele dispara sozinho neste push e avisa o Bing das 7 páginas alteradas — e é o índice do Bing
que alimenta o ChatGPT, que hoje é 40% do tráfego do site. Se ficar **verde**, está feito.
Se ficar **vermelho**, me mande o erro.

---

# As três mudanças

## 1. O site estava dizendo que o limite legal é 25 km/h. É 20 km/h. ← a mais grave

Em 20 lugares, a categoria de patinetes dizia que a lei irlandesa permite 25 km/h. Um dos
produtos tinha o selo **"Best Road-Legal Entry"** e o prós **"25 km/h — Irish-legal out of
the box"**. Isso é falso, e é falso de um jeito que pode custar o patinete de um leitor:
Gardaí podem apreender um aparelho que não cumpre a especificação técnica.

**Por que o erro aconteceu** — são duas leis diferentes lidas como uma:

| Lei | O que ela define | Velocidade |
|---|---|---|
| Road Traffic Act 2024, s.16 | a classe *powered personal transporter* (o envelope) | até **25 km/h** |
| S.I. 199/2024 | o uso do **patinete** dentro dessa classe | máximo **20 km/h** |

Os anúncios da Amazon citam o número do envelope. A lei que vale na estrada é a outra.
Corrigido em todos os 20 pontos: selos, prós, specs, veredictos e textos de guia.

## 2. Capacete e alta-visibilidade são obrigatórios desde 4 de setembro — o site dizia que não

Duas páginas no ar diziam *"helmets and hi-vis are currently recommended, not required by
law"*. A regra entrou em vigor em **04/09/2026** (S.I. 455/2026). O site ficou errado por
duas semanas.

Detalhe que quase toda a imprensa errou e que a página nova acerta: **a obrigação é lei, mas
a multa ainda não existe.** O Departamento de Transportes disse que a notificação de €100
entra junto com o aumento geral de €50 para €100, "nas próximas semanas".

## 3. A página nova: `e-scooter-law-ireland-2026.html`

O item da Semana 5 da fila. ~1.900 palavras, com cada número apontando para o artigo exato da
lei que o cria, e uma separação clara entre **o que está em vigor** e **o que só foi
anunciado** (idade mínima 18, multas de €100 e a reclassificação como veículo a motor — nada
disso é lei ainda).

Tem também a seção que nenhum concorrente tem: **por que os anúncios dizem 25 km/h**. É o tipo
de resposta que um assistente de IA levanta inteira — e o ChatGPT é 40% do tráfego do site.

Fontes conferidas uma a uma no texto original: `irishstatutebook.ie` (S.I. 199/2024 e Road
Traffic Act 2024 s.16), `citizensinformation.ie` (editada em 04/09/2026), e a nota do
Departamento de Transportes.

---

## Sobre a contagem de arquivos no GitHub Desktop

Eu mudei 11 arquivos hoje. O GitHub Desktop pode mostrar mais, porque o seu clone já estava
com uns 47 arquivos de diferença em relação a `C:\ireland` antes de eu copiar.

**Isso é seguro, e eu verifiquei:** comparei o sitemap que acabei de gerar contra o sitemap
que está **no ar agora**. Resultado: 1 URL nova, **nenhuma URL sumindo, nenhuma data
retrocedendo**. O que vai subir é superconjunto do que já está publicado — nada regride.

Pode commitar tudo.
