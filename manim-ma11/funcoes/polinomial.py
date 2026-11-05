"""
MA11 - Ficha: função polinomial

Renderizar:  manim -pql polinomial.py FuncaoPolinomial
"""
from manim import *
import numpy as np


class Ficha(Scene):
    """Layout comum: título e definição no topo, gráfico à esquerda, propriedades à direita."""

    def cabecalho(self, nome, definicao):
        titulo = Text(nome, font_size=38, weight=BOLD).to_corner(UL)
        defi = MathTex(definicao, font_size=36).next_to(titulo, RIGHT, buff=0.6)
        linha = Line(LEFT * 7, RIGHT * 7, stroke_width=1, color=GRAY)
        linha.set_y(titulo.get_bottom()[1] - 0.2)
        self.play(Write(titulo))
        self.play(Write(defi), Create(linha))
        self.itens = VGroup()
        self.topo = linha.get_y()

    def eixos(self, xr, yr, **kw):
        config = dict(axis_config={"include_numbers": True, "font_size": 20})
        config.update(kw)
        ax = Axes(x_range=xr, y_range=yr, x_length=6.4, y_length=5.6, tips=False, **config)
        ax.move_to(LEFT * 3.4 + DOWN * 0.55)
        self.play(Create(ax))
        return ax

    def item(self, tex, cor=WHITE, *extras):
        """Escreve uma propriedade no painel da direita (com animações extras em paralelo)."""
        m = MathTex(r"\bullet\ " + tex, font_size=30, color=cor)
        if len(self.itens) == 0:
            m.move_to([0.4, self.topo - 0.4, 0], aligned_edge=UL)
        else:
            m.next_to(self.itens[-1], DOWN, buff=0.3, aligned_edge=LEFT)
        self.itens.add(m)
        self.play(Write(m), *extras)
        self.wait(0.8)
        return m


class FuncaoPolinomial(Ficha):
    def construct(self):
        self.cabecalho("Função polinomial", r"p(x) = a_n x^n + \cdots + a_1 x + a_0")
        ax = self.eixos([-3, 3, 1], [-4, 4, 1])
        f = lambda x: x ** 3 - 3 * x
        g = ax.plot(f, x_range=[-2.19, 2.19], color=YELLOW)
        self.item(r"\text{Ex.: } p(x) = x^3 - 3x \ (n = 3)", WHITE, Create(g))
        self.item(r"D(p) = \mathbb{R};\ \ n \text{ ímpar} \Rightarrow \operatorname{Im}(p) = \mathbb{R}")

        s3 = np.sqrt(3)
        z = VGroup(*[Dot(ax.c2p(x, 0), color=GREEN) for x in (-s3, 0, s3)])
        self.item(r"\text{Zeros: } 0,\ \pm\sqrt3\ \ (\text{no máximo } n)", GREEN, FadeIn(z, scale=2))
        self.item(r"p(\alpha)=0 \iff (x-\alpha) \mid p(x)", GREEN)

        ext = VGroup(Dot(ax.c2p(-1, 2), color=RED), Dot(ax.c2p(1, -2), color=RED))
        self.item(r"\text{Máx. local } (-1, 2),\ \text{mín. local } (1,-2)", RED, FadeIn(ext, scale=2))

        setas = VGroup(Arrow(ax.c2p(2.0, 2.0), ax.c2p(2.15, 3.6), buff=0, color=BLUE),
                       Arrow(ax.c2p(-2.0, -2.0), ax.c2p(-2.15, -3.6), buff=0, color=BLUE))
        self.item(r"|x| \text{ grande: } p(x) \approx a_n x^n", BLUE, GrowArrow(setas[0]), GrowArrow(setas[1]))
        self.item(r"p \text{ é contínua (sem saltos)}")
        self.wait(2)
