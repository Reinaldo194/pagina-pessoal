"""
MA11 - Unidade 3: Números cardinais (conjuntos enumeráveis e não enumeráveis)

Renderizar:  manim -pql 03_cardinalidade.py RacionaisEnumeraveis
             manim -pql 03_cardinalidade.py DiagonalCantor
"""
from manim import *
from math import gcd
import random


class RacionaisEnumeraveis(Scene):
    """Percorre a grade p/q em diagonais, pulando frações não irredutíveis."""

    def construct(self):
        titulo = MathTex(r"\mathbb{Q}^+ \text{ é enumerável}").to_edge(UP)
        self.play(Write(titulo))
        N = 5
        dx, dy = 1.6, 1.0
        canto = LEFT * 5 + UP * 2
        fr = {}
        grade = VGroup()
        for p in range(1, N + 1):
            for q in range(1, N + 1):
                m = MathTex(rf"\frac{{{p}}}{{{q}}}", font_size=34)
                m.move_to(canto + RIGHT * dx * (p - 1) + DOWN * dy * (q - 1))
                fr[(p, q)] = m
                grade.add(m)
        self.play(LaggedStart(*[FadeIn(m) for m in grade], lag_ratio=0.02))

        # ordem das diagonais p + q = s
        ordem = []
        for s in range(2, N + 2):
            diag = [(p, s - p) for p in range(1, s)]
            if s % 2 == 0:
                diag.reverse()
            ordem += [(p, q) for p, q in diag if p <= N and q <= N]

        lista = MathTex(r"\mathbb{Q}^+ = \{", font_size=32).to_corner(DR).shift(UP * 0.6 + LEFT * 6)
        self.play(Write(lista))
        ultimo = lista
        anterior = None
        cont = 0
        for (p, q) in ordem:
            m = fr[(p, q)]
            if anterior is not None:
                self.play(Create(Arrow(anterior.get_center(), m.get_center(), buff=0.25,
                                       stroke_width=3, color=YELLOW,
                                       max_tip_length_to_length_ratio=0.15)),
                          run_time=0.25)
            if gcd(p, q) == 1:
                cont += 1
                self.play(m.animate.set_color(GREEN), run_time=0.2)
                if cont <= 9:
                    item = MathTex(rf"\tfrac{{{p}}}{{{q}}},", font_size=32).next_to(ultimo, RIGHT, buff=0.1)
                    self.play(TransformFromCopy(m, item), run_time=0.3)
                    ultimo = item
            else:
                # fração repetida (ex.: 2/2 = 1/1)
                self.play(m.animate.set_color(GRAY).set_opacity(0.4), run_time=0.2)
            anterior = m
        self.play(Write(MathTex(r"\ldots\}", font_size=32).next_to(ultimo, RIGHT, buff=0.1)))
        self.wait(2)


class DiagonalCantor(Scene):
    """[0,1] não é enumerável: o número diagonal difere de todos da lista."""

    def construct(self):
        random.seed(7)
        n = 6
        titulo = MathTex(r"[0,1] \text{ não é enumerável}").to_edge(UP)
        self.play(Write(titulo))

        digitos = [[random.randint(0, 9) for _ in range(n)] for _ in range(n)]
        linhas = VGroup()
        for i in range(n):
            lin = VGroup(MathTex(rf"x_{{{i + 1}}} = 0,"),
                         *[MathTex(str(d)) for d in digitos[i]],
                         MathTex(r"\ldots"))
            lin.arrange(RIGHT, buff=0.25)
            linhas.add(lin)
        linhas.arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(LEFT * 2 + DOWN * 0.3)
        self.play(LaggedStart(*[FadeIn(l) for l in linhas], lag_ratio=0.15))

        novo = []
        caixas = VGroup()
        for i in range(n):
            d = linhas[i][i + 1]
            caixas.add(SurroundingRectangle(d, color=YELLOW, buff=0.07))
            # troca o dígito: escolha que evita 0 e 9 (problema do 0,999... = 1)
            novo.append(5 if digitos[i][i] != 5 else 4)
        self.play(LaggedStart(*[Create(c) for c in caixas], lag_ratio=0.2))

        y = VGroup(MathTex("y = 0,", color=YELLOW),
                   *[MathTex(str(d), color=YELLOW) for d in novo],
                   MathTex(r"\ldots", color=YELLOW)).arrange(RIGHT, buff=0.25)
        y.next_to(linhas, DOWN, buff=0.6, aligned_edge=LEFT)
        self.play(Write(y[0]))
        for i in range(n):
            self.play(TransformFromCopy(linhas[i][i + 1], y[i + 1]), run_time=0.5)
        self.play(Write(y[-1]))

        regra = MathTex(r"y_k \ne (x_k)_k \;\Rightarrow\; y \ne x_k \ \ \forall k",
                        font_size=36).to_edge(RIGHT).shift(UP)
        self.play(Write(regra))
        self.wait(2)
