"""
MA11 - Ficha: função exponencial f(x) = a^x

Renderizar:  manim -pql exponencial.py FuncaoExponencial
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


class FuncaoExponencial(Ficha):
    def construct(self):
        self.cabecalho("Função exponencial", r"f(x) = a^x,\ \ a>0,\ a \ne 1")
        ax = self.eixos([-4, 4, 1], [0, 8, 1])
        g = ax.plot(lambda x: 2 ** x, x_range=[-4, 3], color=YELLOW)
        self.item(r"\text{Ex.: } f(x) = 2^x", WHITE, Create(g))
        p = Dot(ax.c2p(0, 1), color=RED)
        self.item(r"f(0) = 1 \text{ (para toda base)}", RED, FadeIn(p, scale=2))

        assint = DashedLine(ax.c2p(-4, 0), ax.c2p(0, 0), color=BLUE, stroke_width=5)
        self.item(r"D(f)=\mathbb{R},\ \ \operatorname{Im}(f) = (0,+\infty)", BLUE, Create(assint))
        self.item(r"x \to -\infty \Rightarrow 2^x \to 0 \text{ (assíntota } y=0)", BLUE)

        g2 = ax.plot(lambda x: 0.5 ** x, x_range=[-3, 4], color=ORANGE)
        r2 = MathTex(r"\left(\tfrac12\right)^x", color=ORANGE, font_size=30).next_to(ax.c2p(-2.6, 6), LEFT)
        self.item(r"a>1:\ \text{crescente};\ 0<a<1:\ \text{decrescente}", WHITE, Create(g2), Write(r2))
        self.item(r"\text{Injetiva: } a^x = a^y \Rightarrow x = y")
        self.item(r"a^{x+y} = a^x \cdot a^y", YELLOW)

        pts = VGroup(*[Dot(ax.c2p(x, 2 ** x)) for x in range(-1, 4)])
        self.item(r"\text{Leva PA em PG: } 2^{x+h} = 2^h \cdot 2^x", YELLOW,
                  LaggedStart(*[FadeIn(d, scale=2) for d in pts], lag_ratio=0.2))
        self.wait(2)
