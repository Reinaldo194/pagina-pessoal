"""
MA11 - Unidade 8: Funções exponenciais e logarítmicas

Renderizar:  manim -pql 08_exponencial_logaritmo.py ExponencialBase
             manim -pql 08_exponencial_logaritmo.py LogaritmoInversa
             manim -pql 08_exponencial_logaritmo.py ExponencialEPG
"""
from manim import *
import numpy as np


class ExponencialBase(Scene):
    """f(x) = a^x: crescente se a > 1, decrescente se 0 < a < 1; sempre passa por (0,1)."""

    def construct(self):
        eixos = Axes(x_range=[-4, 4, 1], y_range=[0, 8, 1], x_length=8, y_length=6,
                     axis_config={"include_numbers": True, "font_size": 18}).shift(LEFT * 1.5)
        self.play(Create(eixos))
        a = ValueTracker(2)
        # o gráfico é recortado para não sair da janela y <= 8
        graf = always_redraw(lambda: self.recorte(eixos, a.get_value()))
        p01 = Dot(eixos.c2p(0, 1), color=RED)
        info = always_redraw(lambda: VGroup(
            MathTex(rf"f(x) = {a.get_value():.2f}^x"),
            MathTex(r"\text{crescente}" if a.get_value() > 1 else
                    (r"\text{constante}" if abs(a.get_value() - 1) < 1e-3 else r"\text{decrescente}"),
                    color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UR))
        self.play(Create(graf), FadeIn(p01), FadeIn(info))
        for v in [3, 1.5, 1, 0.5, 1 / 3, np.e]:
            self.play(a.animate.set_value(v), run_time=1.8)
        prop = MathTex(r"a^{x+y} = a^x \cdot a^y", font_size=38).to_corner(DR)
        self.play(Write(prop))
        self.wait(2)

    @staticmethod
    def recorte(eixos, base):
        # intervalo de x em que 0 < base^x <= 8
        if abs(base - 1) < 1e-6:
            xr = [-4, 4]
        elif base > 1:
            xr = [-4, min(4, np.log(8) / np.log(base))]
        else:
            xr = [max(-4, np.log(8) / np.log(base)), 4]
        return eixos.plot(lambda x: base ** x, x_range=xr, color=YELLOW).set_stroke(width=4)


class LogaritmoInversa(Scene):
    """log_a é a inversa de a^x: reflexão do gráfico na reta y = x."""

    def construct(self):
        eixos = Axes(x_range=[-3, 6, 1], y_range=[-3, 6, 1], x_length=6.5, y_length=6.5,
                     axis_config={"include_numbers": True, "font_size": 18}).shift(LEFT * 2)
        self.play(Create(eixos))
        exp_g = eixos.plot(lambda x: 2 ** x, x_range=[-3, np.log2(6)], color=YELLOW)
        diag = eixos.plot(lambda x: x, x_range=[-3, 6], color=GRAY).set_stroke(opacity=0.6)
        rot_e = MathTex("y=2^x", color=YELLOW, font_size=32).next_to(eixos.c2p(2.3, 5), LEFT)
        rot_d = MathTex("y=x", color=GRAY, font_size=32).next_to(eixos.c2p(5.5, 5.5), DR, buff=0.05)
        self.play(Create(exp_g), Write(rot_e))
        self.play(Create(diag), Write(rot_d))

        # reflete pontos individuais primeiro
        for x in [-1, 0, 1, 2]:
            P = Dot(eixos.c2p(x, 2 ** x), color=YELLOW)
            Q = Dot(eixos.c2p(2 ** x, x), color=BLUE)
            seg = DashedLine(P.get_center(), Q.get_center(), stroke_width=2)
            self.play(FadeIn(P), Create(seg), TransformFromCopy(P, Q), run_time=0.6)

        log_g = exp_g.copy()
        self.play(log_g.animate.apply_function(
            lambda p: eixos.c2p(*reversed(eixos.p2c(p)[:2]))).set_color(BLUE), run_time=2)
        rot_l = MathTex(r"y=\log_2 x", color=BLUE, font_size=32).next_to(eixos.c2p(5, 2.3), DOWN)
        self.play(Write(rot_l))
        props = VGroup(
            MathTex(r"\log_a(xy) = \log_a x + \log_a y"),
            MathTex(r"a^{\log_a x} = x,\quad \log_a(a^x) = x"),
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.7).to_corner(UR)
        self.play(Write(props))
        self.wait(2)


class ExponencialEPG(Scene):
    """f exponencial transforma PA em PG: f(x + h) / f(x) = a^h (constante)."""

    def construct(self):
        eixos = Axes(x_range=[0, 5, 1], y_range=[0, 34, 4], x_length=7, y_length=6,
                     axis_config={"include_numbers": True, "font_size": 18}).shift(LEFT * 2)
        g = eixos.plot(lambda x: 2 ** x, x_range=[0, 5], color=YELLOW)
        self.play(Create(eixos), Create(g))
        valores = VGroup()
        for x in range(0, 6):
            P = Dot(eixos.c2p(x, 2 ** x))
            v = DashedLine(eixos.c2p(x, 0), P.get_center(), stroke_width=2, color=BLUE)
            self.play(Create(v), FadeIn(P), run_time=0.4)
            valores.add(MathTex(str(2 ** x), font_size=34))
        valores.arrange(RIGHT, buff=0.5).to_corner(UR).shift(DOWN * 0.5)
        setas = VGroup(*[
            CurvedArrow(valores[i].get_top(), valores[i + 1].get_top(), angle=-PI / 2,
                        tip_length=0.12).set_color(GREEN)
            for i in range(len(valores) - 1)
        ])
        x2 = VGroup(*[MathTex(r"\times 2", font_size=24, color=GREEN).next_to(s, UP, buff=0.05) for s in setas])
        self.play(Write(valores))
        self.play(Create(setas), Write(x2))
        txt = VGroup(MathTex(r"x: \text{PA de razão } 1", font_size=32),
                     MathTex(r"\Rightarrow\ 2^x: \text{PG de razão } 2", font_size=32)
                     ).arrange(DOWN, aligned_edge=LEFT).next_to(valores, DOWN, buff=0.8)
        self.play(Write(txt))
        self.wait(2)
