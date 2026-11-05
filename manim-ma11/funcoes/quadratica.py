"""
MA11 - Ficha: função quadrática f(x) = ax^2 + bx + c

Renderizar:  manim -pql quadratica.py FuncaoQuadratica
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


class FuncaoQuadratica(Ficha):
    def construct(self):
        self.cabecalho("Função quadrática", r"f(x) = ax^2 + bx + c,\ \ a \ne 0")
        ax = self.eixos([-3, 5, 1], [-5, 6, 1])
        f = lambda x: x ** 2 - 2 * x - 3
        g = ax.plot(f, x_range=[-2.1, 4.1], color=YELLOW)
        self.item(r"\text{Ex.: } f(x) = x^2 - 2x - 3", WHITE, Create(g))
        self.item(r"\text{Gráfico: parábola}")
        self.item(r"a>0 \Rightarrow \text{concavidade para cima}")

        z = VGroup(Dot(ax.c2p(-1, 0), color=GREEN), Dot(ax.c2p(3, 0), color=GREEN))
        self.item(r"\text{Zeros: } x = \frac{-b \pm \sqrt{\Delta}}{2a} \ \to\ -1 \text{ e } 3",
                  GREEN, FadeIn(z, scale=2))
        v = Dot(ax.c2p(1, -4), color=RED)
        self.item(r"\text{Vértice: } \left(-\tfrac{b}{2a}, -\tfrac{\Delta}{4a}\right) = (1,-4)",
                  RED, FadeIn(v, scale=2))
        eixo = DashedLine(ax.c2p(1, -5), ax.c2p(1, 6), color=RED, stroke_width=2)
        self.item(r"\text{Eixo de simetria: } x = 1", RED, Create(eixo))

        faixa = Line(ax.c2p(0, -4), ax.c2p(0, 6), color=BLUE, stroke_width=8)
        self.item(r"D(f)=\mathbb{R},\ \ \operatorname{Im}(f) = [-4, +\infty)", BLUE, Create(faixa))

        desc = ax.plot(f, x_range=[-2.1, 1], color=ORANGE, stroke_width=7)
        cres = ax.plot(f, x_range=[1, 4.1], color=GREEN, stroke_width=7)
        self.item(r"\text{Decresce em } (-\infty,1],\ \text{cresce em } [1,+\infty)",
                  WHITE, Create(desc), Create(cres))
        self.item(r"f(x) = a\left(x+\tfrac{b}{2a}\right)^2 - \tfrac{\Delta}{4a}", YELLOW)
        self.wait(2)
