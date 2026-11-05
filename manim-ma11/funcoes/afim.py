"""
MA11 - Ficha: função afim f(x) = ax + b

Renderizar:  manim -pql afim.py FuncaoAfim
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


class FuncaoAfim(Ficha):
    def construct(self):
        self.cabecalho("Função afim", r"f(x) = ax + b,\ \ a, b \in \mathbb{R}")
        ax = self.eixos([-3, 4, 1], [-4, 4, 1])
        g = ax.plot(lambda x: 2 * x - 2, x_range=[-1, 3], color=YELLOW)
        self.item(r"\text{Gráfico: uma reta}", WHITE, Create(g))
        self.item(r"D(f) = \mathbb{R},\ \ \operatorname{Im}(f) = \mathbb{R}\ (a \ne 0)")

        pb = Dot(ax.c2p(0, -2), color=RED)
        self.item(r"f(0) = b \text{ (valor inicial)}", RED, FadeIn(pb, scale=2))
        pz = Dot(ax.c2p(1, 0), color=GREEN)
        self.item(r"\text{Zero: } x = -\tfrac{b}{a}", GREEN, FadeIn(pz, scale=2))

        tri = VGroup(DashedLine(ax.c2p(1, 0), ax.c2p(2, 0), color=BLUE),
                     DashedLine(ax.c2p(2, 0), ax.c2p(2, 2), color=BLUE))
        self.item(r"a = \frac{f(x_2)-f(x_1)}{x_2-x_1} \text{ (taxa constante)}", BLUE, Create(tri))

        self.item(r"a>0:\ \text{crescente};\ \ a<0:\ \text{decrescente}")
        g2 = ax.plot(lambda x: -2 * x + 2, x_range=[-1, 3], color=YELLOW)
        self.play(FadeOut(tri), FadeOut(pb), FadeOut(pz), Transform(g, g2))
        self.wait(0.5)

        self.item(r"b=0:\ f(x)=ax \text{ (linear)}")
        self.play(Transform(g, ax.plot(lambda x: 2 * x, x_range=[-2, 2], color=YELLOW)))
        self.item(r"a=0:\ f(x)=b \text{ (constante)}")
        self.play(Transform(g, ax.plot(lambda x: 2 + 0 * x, x_range=[-3, 4], color=YELLOW)))
        self.play(Transform(g, ax.plot(lambda x: 2 * x - 2, x_range=[-1, 3], color=YELLOW)))
        self.wait(2)
