"""
MA11 - Unidade 7: Funções polinomiais

Renderizar:  manim -pql 07_funcoes_polinomiais.py RaizesEMultiplicidade
             manim -pql 07_funcoes_polinomiais.py ComportamentoNoInfinito
"""
from manim import *
import numpy as np


class RaizesEMultiplicidade(Scene):
    """Raiz simples: o gráfico cruza o eixo. Raiz dupla: tangencia. Tripla: cruza 'achatando'."""

    def construct(self):
        eixos = Axes(x_range=[-3, 3, 1], y_range=[-4, 4, 1], x_length=7, y_length=6,
                     axis_config={"include_numbers": True, "font_size": 18}).shift(LEFT * 2)
        self.play(Create(eixos))
        casos = [
            (r"p(x) = (x+2)(x-1)(x-2)", lambda x: (x + 2) * (x - 1) * (x - 2) / 2,
             r"\text{raízes simples: cruza o eixo}"),
            (r"p(x) = (x+2)(x-1)^2", lambda x: (x + 2) * (x - 1) ** 2 / 2,
             r"x=1 \text{ dupla: tangencia o eixo}"),
            (r"p(x) = (x+2)(x-1)^3", lambda x: (x + 2) * (x - 1) ** 3 / 2,
             r"x=1 \text{ tripla: cruza e achata}"),
        ]
        graf = txt = None
        for tex, f, obs in casos:
            g = eixos.plot(f, x_range=[-2.6, 2.6], color=YELLOW)
            t = VGroup(MathTex(tex + r"\,/\,2", font_size=32),
                       MathTex(obs, font_size=30, color=GREEN)).arrange(DOWN, aligned_edge=LEFT).to_corner(UR)
            if graf is None:
                self.play(Create(g), Write(t))
            else:
                self.play(ReplacementTransform(graf, g), ReplacementTransform(txt, t))
            graf, txt = g, t
            self.play(Flash(eixos.c2p(1, 0), color=GREEN))
            self.wait(1.5)
        teo = MathTex(r"p(\alpha)=0 \iff p(x) = (x-\alpha)\,q(x)", font_size=34).to_corner(DR)
        self.play(Write(teo))
        self.wait(2)


class ComportamentoNoInfinito(Scene):
    """Para |x| grande, p(x) ≈ a_n x^n: dá zoom-out e compara com o termo líder."""

    def construct(self):
        p = lambda x: x ** 3 - 4 * x ** 2 + x + 6
        lider = lambda x: x ** 3
        escala = ValueTracker(5)

        def cena():
            L = escala.get_value()
            ax = Axes(x_range=[-L, L, L / 5], y_range=[-L ** 3, L ** 3, L ** 3 / 5],
                      x_length=8, y_length=6, tips=False).shift(LEFT * 1.5)
            g1 = ax.plot(p, x_range=[-L, L], color=YELLOW)
            g2 = ax.plot(lider, x_range=[-L, L], color=BLUE).set_stroke(opacity=0.7)
            return VGroup(ax, g1, g2)

        grafico = always_redraw(cena)
        legenda = VGroup(MathTex(r"p(x)=x^3-4x^2+x+6", color=YELLOW, font_size=32),
                         MathTex(r"x^3", color=BLUE, font_size=32)).arrange(DOWN, aligned_edge=LEFT).to_corner(UR)
        janela = always_redraw(lambda: MathTex(rf"|x| \le {escala.get_value():.0f}",
                                               font_size=32).next_to(legenda, DOWN, aligned_edge=LEFT))
        self.play(FadeIn(grafico), Write(legenda), FadeIn(janela))
        self.wait()
        self.play(escala.animate.set_value(100), run_time=6, rate_func=smooth)
        lim = MathTex(r"\lim_{x\to\pm\infty}\frac{p(x)}{x^3} = 1", font_size=36).to_corner(DR)
        self.play(Write(lim))
        self.wait(2)
