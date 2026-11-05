"""
MA11 - Ficha: função logarítmica f(x) = log_a x

Renderizar:  manim -pql logaritmica.py FuncaoLogaritmica
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


class FuncaoLogaritmica(Ficha):
    def construct(self):
        self.cabecalho("Função logarítmica", r"f(x) = \log_a x,\ \ a>0,\ a \ne 1")
        ax = self.eixos([-1, 8, 1], [-3, 4, 1])
        g = ax.plot(np.log2, x_range=[2 ** -3, 8], color=YELLOW)
        self.item(r"\text{Ex.: } f(x) = \log_2 x", WHITE, Create(g))

        assint = DashedLine(ax.c2p(0, -3), ax.c2p(0, 0), color=BLUE, stroke_width=5)
        self.item(r"D(f) = (0,+\infty),\ \ \operatorname{Im}(f) = \mathbb{R}", BLUE, Create(assint))
        self.item(r"x \to 0^+ \Rightarrow \log_2 x \to -\infty \text{ (assíntota } x=0)", BLUE)

        z = Dot(ax.c2p(1, 0), color=GREEN)
        u = Dot(ax.c2p(2, 1), color=RED)
        self.item(r"\log_a 1 = 0,\ \ \log_a a = 1", GREEN, FadeIn(z, scale=2), FadeIn(u, scale=2))

        # inversa da exponencial: reflexão na reta y = x
        diag = ax.plot(lambda x: x, x_range=[-1, 4], color=GRAY).set_stroke(opacity=0.6)
        exp_g = ax.plot(lambda x: 2 ** x, x_range=[-1, 2], color=GRAY).set_stroke(opacity=0.6)
        self.item(r"\text{Inversa de } 2^x:\ \ 2^{\log_2 x} = x", WHITE, Create(diag), Create(exp_g))
        self.play(FadeOut(diag), FadeOut(exp_g))

        g2 = ax.plot(lambda x: -np.log2(x), x_range=[2 ** -4, 8], color=ORANGE)
        self.item(r"a>1:\ \text{crescente};\ 0<a<1:\ \text{decrescente}", WHITE, Create(g2))
        self.item(r"\log_a(xy) = \log_a x + \log_a y", YELLOW)
        self.item(r"\text{Leva PG em PA}", YELLOW)
        self.wait(2)
