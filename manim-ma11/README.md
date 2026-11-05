# Animações Manim — MA11 Números e Funções Reais (PROFMAT)

Cenas em [Manim Community](https://www.manim.community/) (testadas na versão 0.22) organizadas pela ementa da disciplina.

| Arquivo | Unidade | Cenas |
|---|---|---|
| `01_conjuntos.py` | Conjuntos | `OperacoesConjuntos` (união, interseção, diferença, complementar), `DeMorgan` |
| `02_naturais_inducao.py` | Números naturais | `SomaImpares` (1+3+…+(2n−1)=n²), `DominoInducao`, `SomaNaturais` (Gauss) |
| `03_cardinalidade.py` | Números cardinais | `RacionaisEnumeraveis` (grade de Cantor), `DiagonalCantor` ([0,1] não enumerável) |
| `04_numeros_reais.py` | Números reais | `RaizDoisNaReta` (construção + irracionalidade), `IntervalosEncaixados` (expansão decimal de √2) |
| `05_funcao_afim.py` | Funções afins | `CoeficientesAfim` (a e b variando), `AfimEProgressaoAritmetica` (PA → PA) |
| `06_funcao_quadratica.py` | Funções quadráticas | `CompletarQuadrado` (geométrico), `ParabolaParametros` (vértice, Δ, raízes) |
| `07_funcoes_polinomiais.py` | Funções polinomiais | `RaizesEMultiplicidade`, `ComportamentoNoInfinito` (p(x) ≈ termo líder) |
| `08_exponencial_logaritmo.py` | Exponenciais e logaritmos | `ExponencialBase`, `LogaritmoInversa` (reflexão em y=x), `ExponencialEPG` (PA → PG) |
| `09_funcoes_trigonometricas.py` | Funções trigonométricas | `SenoDoCirculo` (função de Euler → gráfico), `AmplitudePeriodo` (A sen(Bx+C)+D) |

## Fichas por tipo de função (`funcoes/`)

Um vídeo separado para cada tipo de função, todos com o mesmo layout: definição no topo, gráfico à esquerda e as propriedades surgindo à direita (domínio, imagem, zeros, monotonicidade, simetrias e a propriedade característica), cada uma destacada no gráfico.

| Arquivo | Cenas |
|---|---|
| `funcoes/afim.py` | `FuncaoAfim` |
| `funcoes/quadratica.py` | `FuncaoQuadratica` |
| `funcoes/polinomial.py` | `FuncaoPolinomial` |
| `funcoes/exponencial.py` | `FuncaoExponencial` |
| `funcoes/logaritmica.py` | `FuncaoLogaritmica` |
| `funcoes/trigonometricas.py` | `FuncaoSeno`, `FuncaoCosseno`, `FuncaoTangente` |

Exemplo: `manim -pql funcoes/quadratica.py FuncaoQuadratica`

## Instalação

Requer Python 3.9+, FFmpeg e uma distribuição LaTeX (TeX Live ou MiKTeX) com `dvisvgm`.

```bash
pip install manim
```

No Linux também são necessárias as bibliotecas `libcairo2-dev` e `libpango1.0-dev`. Guia completo: <https://docs.manim.community/en/stable/installation.html>.

## Como renderizar

Uma cena, baixa qualidade, abrindo o vídeo ao final (bom para testar):

```bash
manim -pql 06_funcao_quadratica.py ParabolaParametros
```

Alta qualidade (1080p, 60 fps) para usar em aula:

```bash
manim -qh 06_funcao_quadratica.py ParabolaParametros
```

Todas as cenas de todos os arquivos:

```bash
bash renderizar_tudo.sh       # qualidade baixa
bash renderizar_tudo.sh -qh   # qualidade alta
```

Os vídeos ficam em `media/videos/<arquivo>/<qualidade>/`.

## Dicas para adaptar

- Coeficientes animados usam `ValueTracker` + `always_redraw`: para mostrar outros casos basta mudar a lista de valores em `self.play(x.animate.set_value(...))`.
- `-s` gera só o último quadro como imagem PNG (útil para slides): `manim -s -qh 01_conjuntos.py DeMorgan`.
- Para fundo branco (impressão/slides claros): `manim -qh --background_color WHITE ...` — nesse caso troque cores claras como `WHITE`/`YELLOW` por cores escuras.
