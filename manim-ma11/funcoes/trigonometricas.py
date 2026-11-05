"""
MA11 - Fichas: funções trigonométricas (seno, cosseno, tangente)

Renderizar:  manim -pql trigonometricas.py FuncaoSeno
             manim -pql trigonometricas.py FuncaoCosseno
             manim -pql trigonometricas.py FuncaoTangente
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

    def eixos_trig(self, ymax):
        ax = self.eixos([-2 * PI, 2 * PI, PI / 2], [-ymax, ymax, 1],
                        x_axis_config={"include_numbers": False},
                        y_axis_config={"include_numbers": True, "font_size": 20})
        rot = VGroup(*[
            MathTex(t, font_size=22).next_to(ax.c2p(v, 0), DOWN, buff=0.15)
            for t, v in [(r"-2\pi", -2 * PI), (r"-\pi", -PI), (r"\pi", PI), (r"2\pi", 2 * PI),
                         (r"\tfrac{\pi}{2}", PI / 2), (r"-\tfrac{\pi}{2}", -PI / 2)]
        ])
        self.play(Write(rot))
        return ax


class FuncaoSeno(Ficha):
    def construct(self):
        self.cabecalho("Função seno", r"\operatorname{sen}: \mathbb{R} \to \mathbb{R}")
        ax = self.eixos_trig(1.5)
        g = ax.plot(np.sin, x_range=[-2 * PI, 2 * PI], color=YELLOW)
        self.item(r"\operatorname{sen} t = \text{ordenada de } E(t) \text{ no círculo}", WHITE, Create(g))

        faixa = VGroup(DashedLine(ax.c2p(-2 * PI, 1), ax.c2p(2 * PI, 1), color=BLUE),
                       DashedLine(ax.c2p(-2 * PI, -1), ax.c2p(2 * PI, -1), color=BLUE))
        self.item(r"D = \mathbb{R},\ \ \operatorname{Im} = [-1, 1]", BLUE, Create(faixa))

        chave = BraceBetweenPoints(ax.c2p(0, -1.2), ax.c2p(2 * PI, -1.2), DOWN, color=RED)
        self.item(r"\text{Período } 2\pi:\ \operatorname{sen}(t+2\pi) = \operatorname{sen} t", RED,
                  GrowFromCenter(chave))
        z = VGroup(*[Dot(ax.c2p(k * PI, 0), color=GREEN) for k in range(-2, 3)])
        self.item(r"\text{Zeros: } t = k\pi,\ k \in \mathbb{Z}", GREEN, FadeIn(z, scale=2))

        t0 = 1.0
        par = VGroup(Dot(ax.c2p(t0, np.sin(t0)), color=ORANGE), Dot(ax.c2p(-t0, -np.sin(t0)), color=ORANGE))
        seg = DashedLine(par[0].get_center(), par[1].get_center(), color=ORANGE)
        self.item(r"\text{Ímpar: } \operatorname{sen}(-t) = -\operatorname{sen} t", ORANGE,
                  FadeIn(par), Create(seg))
        self.item(r"\text{Máx. } 1 \text{ em } \tfrac{\pi}{2} + 2k\pi")
        self.item(r"\text{Cresce em } \left[-\tfrac{\pi}{2}, \tfrac{\pi}{2}\right]", WHITE,
                  Create(ax.plot(np.sin, x_range=[-PI / 2, PI / 2], color=GREEN, stroke_width=7)))
        self.wait(2)


class FuncaoCosseno(Ficha):
    def construct(self):
        self.cabecalho("Função cosseno", r"\cos: \mathbb{R} \to \mathbb{R}")
        ax = self.eixos_trig(1.5)
        g = ax.plot(np.cos, x_range=[-2 * PI, 2 * PI], color=YELLOW)
        self.item(r"\cos t = \text{abscissa de } E(t) \text{ no círculo}", WHITE, Create(g))

        faixa = VGroup(DashedLine(ax.c2p(-2 * PI, 1), ax.c2p(2 * PI, 1), color=BLUE),
                       DashedLine(ax.c2p(-2 * PI, -1), ax.c2p(2 * PI, -1), color=BLUE))
        self.item(r"D = \mathbb{R},\ \ \operatorname{Im} = [-1, 1]", BLUE, Create(faixa))
        chave = BraceBetweenPoints(ax.c2p(0, -1.2), ax.c2p(2 * PI, -1.2), DOWN, color=RED)
        self.item(r"\text{Período } 2\pi", RED, GrowFromCenter(chave))
        z = VGroup(*[Dot(ax.c2p(PI / 2 + k * PI, 0), color=GREEN) for k in range(-2, 2)])
        self.item(r"\text{Zeros: } t = \tfrac{\pi}{2} + k\pi", GREEN, FadeIn(z, scale=2))

        t0 = 1.0
        par = VGroup(Dot(ax.c2p(t0, np.cos(t0)), color=ORANGE), Dot(ax.c2p(-t0, np.cos(t0)), color=ORANGE))
        seg = DashedLine(par[0].get_center(), par[1].get_center(), color=ORANGE)
        self.item(r"\text{Par: } \cos(-t) = \cos t \text{ (simetria no eixo } y)", ORANGE,
                  FadeIn(par), Create(seg))

        seno = ax.plot(np.sin, x_range=[-2 * PI, 2 * PI], color=GRAY).set_stroke(opacity=0.7)
        self.item(r"\cos t = \operatorname{sen}\left(t + \tfrac{\pi}{2}\right)", WHITE, Create(seno))
        self.play(seno.animate.shift(ax.c2p(-PI / 2, 0) - ax.c2p(0, 0)), run_time=2)
        self.item(r"\cos^2 t + \operatorname{sen}^2 t = 1", YELLOW)
        self.wait(2)


class FuncaoTangente(Ficha):
    def construct(self):
        self.cabecalho("Função tangente", r"\operatorname{tg} t = \operatorname{sen} t \,/\, \cos t")
        ax = self.eixos_trig(4)
        # um ramo por intervalo (-pi/2 + k pi, pi/2 + k pi), cortado em |tg| <= 4
        c = np.arctan(4)
        ramos = VGroup(*[
            ax.plot(np.tan, x_range=[max(k * PI - c, -2 * PI), min(k * PI + c, 2 * PI)], color=YELLOW)
            for k in range(-2, 3)
        ])
        self.item(r"\text{Gráfico formado por ramos}", WHITE, Create(ramos))

        assint = VGroup(*[DashedLine(ax.c2p(PI / 2 + k * PI, -4), ax.c2p(PI / 2 + k * PI, 4),
                                     color=BLUE, stroke_width=2) for k in range(-2, 2)])
        self.item(r"D = \{t \mid t \ne \tfrac{\pi}{2} + k\pi\}", BLUE, Create(assint))
        self.item(r"\text{Assíntotas verticais em } t = \tfrac{\pi}{2} + k\pi", BLUE)
        self.item(r"\operatorname{Im} = \mathbb{R}")

        chave = BraceBetweenPoints(ax.c2p(-PI / 2, 4.1), ax.c2p(PI / 2, 4.1), UP, color=RED)
        self.item(r"\text{Período } \pi:\ \operatorname{tg}(t+\pi) = \operatorname{tg} t", RED,
                  GrowFromCenter(chave))
        z = VGroup(*[Dot(ax.c2p(k * PI, 0), color=GREEN) for k in range(-2, 3)])
        self.item(r"\text{Zeros: } t = k\pi;\ \ \text{ímpar}", GREEN, FadeIn(z, scale=2))
        self.item(r"\text{Crescente em cada } \left(-\tfrac{\pi}{2}+k\pi, \tfrac{\pi}{2}+k\pi\right)")
        self.wait(2)
