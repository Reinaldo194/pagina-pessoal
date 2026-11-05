"""
MA11 - Unidade 9: Funções trigonométricas

Renderizar:  manim -pql 09_funcoes_trigonometricas.py SenoDoCirculo
             manim -pql 09_funcoes_trigonometricas.py AmplitudePeriodo
"""
from manim import *
import numpy as np


class SenoDoCirculo(Scene):
    """A função de Euler E(t) = (cos t, sen t) e o gráfico do seno 'desenrolado'."""

    def construct(self):
        R = 1.3
        centro = LEFT * 4.5
        circ = Circle(radius=R, color=WHITE).move_to(centro)
        eix_c = VGroup(Line(centro + LEFT * 1.6, centro + RIGHT * 1.6),
                       Line(centro + DOWN * 1.6, centro + UP * 1.6)).set_stroke(GRAY, 2)
        eixos = Axes(x_range=[0, 2 * PI + 0.3, PI / 2], y_range=[-1.3, 1.3, 1],
                     x_length=7.5, y_length=2 * R * 1.3, tips=False).next_to(circ, RIGHT, buff=0.8)
        # garante que y=0 do gráfico fique na altura do centro do círculo
        eixos.shift(UP * (centro[1] - eixos.c2p(0, 0)[1]))
        rotulos_x = VGroup(*[
            MathTex(t, font_size=26).next_to(eixos.c2p(v, 0), DOWN)
            for t, v in [(r"\tfrac{\pi}{2}", PI / 2), (r"\pi", PI), (r"\tfrac{3\pi}{2}", 3 * PI / 2), (r"2\pi", 2 * PI)]
        ])
        self.play(Create(circ), Create(eix_c), Create(eixos), Write(rotulos_x))

        t = ValueTracker(0)
        P = always_redraw(lambda: Dot(centro + R * np.array([np.cos(t.get_value()), np.sin(t.get_value()), 0]),
                                      color=YELLOW))
        raio = always_redraw(lambda: Line(centro, P.get_center(), color=YELLOW))
        arco = always_redraw(lambda: Arc(radius=R, start_angle=0, angle=t.get_value(),
                                         arc_center=centro, color=ORANGE, stroke_width=6))
        seno_seg = always_redraw(lambda: Line(centro + R * np.cos(t.get_value()) * RIGHT,
                                              P.get_center(), color=RED, stroke_width=5))
        cos_seg = always_redraw(lambda: Line(centro, centro + R * np.cos(t.get_value()) * RIGHT,
                                             color=BLUE, stroke_width=5))
        Q = always_redraw(lambda: Dot(eixos.c2p(t.get_value(), np.sin(t.get_value())), color=RED))
        ligacao = always_redraw(lambda: DashedLine(P.get_center(), Q.get_center(), stroke_width=1.5))
        curva = always_redraw(lambda: eixos.plot(np.sin, x_range=[0, max(t.get_value(), 1e-3)], color=RED))

        legenda = VGroup(MathTex(r"E(t) = (\cos t, \operatorname{sen} t)", font_size=32),
                         MathTex(r"\operatorname{sen} t", color=RED, font_size=32),
                         MathTex(r"\cos t", color=BLUE, font_size=32)).arrange(RIGHT, buff=0.6).to_edge(UP)
        self.play(Write(legenda))
        self.add(arco, raio, cos_seg, seno_seg, P, ligacao, curva, Q)
        self.play(t.animate.set_value(2 * PI), run_time=8, rate_func=linear)
        self.wait()
        per = MathTex(r"\operatorname{sen}(t + 2\pi) = \operatorname{sen} t", font_size=34).to_edge(DOWN)
        self.play(Write(per))
        self.wait(2)


class AmplitudePeriodo(Scene):
    """f(x) = A sen(Bx + C) + D: efeito de cada parâmetro."""

    def construct(self):
        eixos = Axes(x_range=[-2 * PI, 2 * PI, PI / 2], y_range=[-4, 4, 1], x_length=11, y_length=5.5,
                     axis_config={"font_size": 18}, y_axis_config={"include_numbers": True}).shift(DOWN * 0.5)
        self.play(Create(eixos))
        A, B, C, D = (ValueTracker(v) for v in (1, 1, 0, 0))
        f = lambda x: A.get_value() * np.sin(B.get_value() * x + C.get_value()) + D.get_value()
        base = eixos.plot(np.sin, color=GRAY).set_stroke(opacity=0.4)
        graf = always_redraw(lambda: eixos.plot(f, color=YELLOW, x_range=[-2 * PI, 2 * PI, 0.02]))
        info = always_redraw(lambda: MathTex(
            rf"f(x) = {A.get_value():.1f}\,\operatorname{{sen}}({B.get_value():.1f}x {C.get_value():+.1f}) {D.get_value():+.1f}"
            rf"\qquad \text{{período}} = \tfrac{{2\pi}}{{|B|}} \approx {2 * PI / abs(B.get_value()):.2f}",
            font_size=32).to_edge(UP))
        self.add(base)
        self.play(Create(graf), FadeIn(info))
        self.play(A.animate.set_value(2.5), run_time=2)
        self.play(A.animate.set_value(1), run_time=1)
        self.play(B.animate.set_value(2), run_time=2)
        self.play(B.animate.set_value(0.5), run_time=2)
        self.play(B.animate.set_value(1), run_time=1)
        self.play(C.animate.set_value(PI / 2), run_time=2)   # sen(x + pi/2) = cos x
        self.play(D.animate.set_value(1.5), run_time=2)
        self.play(D.animate.set_value(0), C.animate.set_value(0), run_time=1.5)
        self.wait(2)
