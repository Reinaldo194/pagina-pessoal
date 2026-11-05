"""
MA11 - Unidade 5: Função afim f(x) = ax + b

Renderizar:  manim -pql 05_funcao_afim.py CoeficientesAfim
             manim -pql 05_funcao_afim.py AfimEProgressaoAritmetica
"""
from manim import *


class CoeficientesAfim(Scene):
    """Efeito dos coeficientes a (taxa de variação) e b (valor inicial)."""

    def construct(self):
        eixos = Axes(x_range=[-5, 5, 1], y_range=[-4, 4, 1], x_length=8, y_length=6.4,
                     axis_config={"include_numbers": True, "font_size": 20}).shift(LEFT * 1.5)
        self.play(Create(eixos))
        a = ValueTracker(1)
        b = ValueTracker(0)

        reta = always_redraw(lambda: eixos.plot(
            lambda x: a.get_value() * x + b.get_value(), x_range=[-5, 5],
            color=YELLOW, use_smoothing=False).set_stroke(width=4))
        pb = always_redraw(lambda: Dot(eixos.c2p(0, b.get_value()), color=RED))
        # triângulo de inclinação: anda 1 em x, sobe a em y
        tri = always_redraw(lambda: VGroup(
            DashedLine(eixos.c2p(1, b.get_value() + a.get_value()), eixos.c2p(2, b.get_value() + a.get_value()), color=GREEN),
            DashedLine(eixos.c2p(2, b.get_value() + a.get_value()), eixos.c2p(2, b.get_value() + 2 * a.get_value()), color=GREEN),
        ))
        painel = always_redraw(lambda: VGroup(
            MathTex(r"f(x) = ax + b"),
            MathTex(rf"a = {a.get_value():.2f}", color=GREEN),
            MathTex(rf"b = {b.get_value():.2f}", color=RED),
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UR))
        self.play(Create(reta), FadeIn(pb), FadeIn(painel), Create(tri))
        self.wait()

        for v in [2, 0.5, 0, -1, -2]:
            self.play(a.animate.set_value(v), run_time=1.5)
        self.play(a.animate.set_value(1), run_time=1)
        for v in [2, -2, 0]:
            self.play(b.animate.set_value(v), run_time=1.5)

        nota = MathTex(r"a = \frac{f(x+h)-f(x)}{h}", font_size=38).to_corner(DR)
        self.play(Write(nota))
        self.wait(2)


class AfimEProgressaoAritmetica(Scene):
    """f afim transforma PA (em x) em PA (em y): f(x+h) - f(x) = ah."""

    def construct(self):
        eixos = Axes(x_range=[0, 7, 1], y_range=[0, 8, 1], x_length=7, y_length=5.5,
                     axis_config={"include_numbers": True, "font_size": 20}).to_edge(LEFT, buff=0.4)
        f = lambda x: 0.8 * x + 1.5
        graf = eixos.plot(f, x_range=[0, 7], color=YELLOW)
        self.play(Create(eixos), Create(graf))
        xs = [1, 2, 3, 4, 5, 6]
        pontos = VGroup()
        for x in xs:
            px = Dot(eixos.c2p(x, 0), color=BLUE)
            p = Dot(eixos.c2p(x, f(x)), color=WHITE)
            py = Dot(eixos.c2p(0, f(x)), color=RED)
            v = DashedLine(px.get_center(), p.get_center(), stroke_width=2)
            hz = DashedLine(p.get_center(), py.get_center(), stroke_width=2)
            self.play(FadeIn(px), Create(v), FadeIn(p), Create(hz), FadeIn(py), run_time=0.5)
            pontos.add(VGroup(px, p, py))
        txt = VGroup(
            MathTex(r"x_1, x_2, \ldots \text{ PA de razão } h", color=BLUE),
            MathTex(r"\Rightarrow f(x_1), f(x_2), \ldots", color=RED),
            MathTex(r"\text{PA de razão } ah", color=RED),
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.8).to_corner(UR)
        self.play(Write(txt))
        teo = Tex(r"Teorema: se $f$ é monótona\\ e transforma PA em PA,\\ então $f$ é afim.",
                  font_size=30).next_to(txt, DOWN, buff=0.8).to_edge(RIGHT, buff=0.3)
        self.play(Write(teo))
        self.wait(2)
