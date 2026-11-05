"""
MA11 - Unidade 6: Função quadrática f(x) = ax^2 + bx + c

Renderizar:  manim -pql 06_funcao_quadratica.py CompletarQuadrado
             manim -pql 06_funcao_quadratica.py ParabolaParametros
"""
from manim import *
import numpy as np


class CompletarQuadrado(Scene):
    """x^2 + bx + (b/2)^2 = (x + b/2)^2, de forma geométrica."""

    def construct(self):
        titulo = MathTex(r"x^2 + bx = \left(x+\tfrac b2\right)^2 - \left(\tfrac b2\right)^2").to_edge(UP)
        self.play(Write(titulo))
        x, b = 2.4, 1.6
        q = Square(x, fill_color=BLUE, fill_opacity=0.7).shift(LEFT * 1.5 + DOWN * 0.5)
        lx = MathTex("x^2").move_to(q)
        ret = Rectangle(width=b, height=x, fill_color=GREEN, fill_opacity=0.7).next_to(q, RIGHT, buff=0)
        lr = MathTex("bx").move_to(ret)
        self.play(FadeIn(q), Write(lx))
        self.play(FadeIn(ret), Write(lr))
        self.wait()

        # divide o retângulo em duas metades b/2
        r1 = Rectangle(width=b / 2, height=x, fill_color=GREEN, fill_opacity=0.7).next_to(q, RIGHT, buff=0)
        r2 = r1.copy().next_to(r1, RIGHT, buff=0)
        self.play(FadeOut(ret), FadeOut(lr), FadeIn(r1), FadeIn(r2))
        r2_alvo = Rectangle(width=x, height=b / 2, fill_color=GREEN, fill_opacity=0.7).next_to(q, UP, buff=0)
        self.play(Transform(r2, r2_alvo))
        l1 = MathTex(r"\tfrac b2 x", font_size=30).move_to(r1)
        l2 = MathTex(r"\tfrac b2 x", font_size=30).move_to(r2_alvo)
        self.play(Write(l1), Write(l2))

        canto = Square(b / 2, fill_color=YELLOW, fill_opacity=0.8).next_to(r1, UP, buff=0)
        lc = MathTex(r"\left(\tfrac b2\right)^2", font_size=26, color=BLACK).move_to(canto)
        self.play(DrawBorderThenFill(canto), Write(lc))
        chave = Brace(VGroup(q, r1), DOWN)
        self.play(GrowFromCenter(chave), Write(chave.get_tex(r"x + \tfrac b2")))
        self.wait(2)


class ParabolaParametros(Scene):
    """Gráfico com vértice (-b/2a, -Δ/4a) e raízes, variando a, b, c."""

    def construct(self):
        eixos = Axes(x_range=[-5, 5, 1], y_range=[-5, 5, 1], x_length=7.5, y_length=7,
                     axis_config={"include_numbers": True, "font_size": 18}).shift(LEFT * 2)
        self.add(eixos)
        a, b, c = ValueTracker(1), ValueTracker(0), ValueTracker(-2)

        def coef():
            A = a.get_value()
            if abs(A) < 1e-4:  # evita divisão por zero quando a passa por 0
                A = 1e-4
            return A, b.get_value(), c.get_value()

        parab = always_redraw(lambda: eixos.plot(
            lambda x: coef()[0] * x ** 2 + coef()[1] * x + coef()[2],
            x_range=[-5, 5], color=YELLOW
        ).set_stroke(width=4))

        def vertice():
            A, B, C = coef()
            d = B * B - 4 * A * C
            return -B / (2 * A), -d / (4 * A)

        vert = always_redraw(lambda: Dot(eixos.c2p(*vertice()), color=RED))
        eixo_sim = always_redraw(lambda: DashedLine(eixos.c2p(vertice()[0], -5),
                                                    eixos.c2p(vertice()[0], 5), color=RED, stroke_width=2))

        def raizes():
            A, B, C = coef()
            d = B * B - 4 * A * C
            if d < 0:
                return VGroup()
            r = [(-B - np.sqrt(d)) / (2 * A), (-B + np.sqrt(d)) / (2 * A)]
            return VGroup(*[Dot(eixos.c2p(x, 0), color=GREEN) for x in r if -5 <= x <= 5])

        pontos_raiz = always_redraw(raizes)

        def painel():
            A, B, C = coef()
            d = B * B - 4 * A * C
            xv, yv = vertice()
            return VGroup(
                MathTex(rf"a={A:.1f},\ b={B:.1f},\ c={C:.1f}", font_size=32),
                MathTex(rf"\Delta = b^2-4ac = {d:.2f}", font_size=32),
                MathTex(rf"V = \left(-\tfrac{{b}}{{2a}}, -\tfrac{{\Delta}}{{4a}}\right) = ({xv:.2f},\,{yv:.2f})",
                        font_size=28, color=RED),
                MathTex(r"\Delta>0:\ 2\text{ raízes}" if d > 1e-9 else
                        (r"\Delta=0:\ 1\text{ raiz}" if abs(d) <= 1e-9 else r"\Delta<0:\ \text{sem raízes reais}"),
                        font_size=30, color=GREEN),
            ).arrange(DOWN, aligned_edge=LEFT).to_corner(UR)

        info = always_redraw(painel)
        forma = MathTex(r"f(x) = a\left(x+\tfrac{b}{2a}\right)^2 - \tfrac{\Delta}{4a}",
                        font_size=32).to_corner(DR)
        self.play(Create(parab), FadeIn(vert), Create(eixo_sim), FadeIn(pontos_raiz), FadeIn(info))
        self.play(Write(forma))

        self.play(c.animate.set_value(0), run_time=1.5)
        self.play(c.animate.set_value(2), run_time=2)          # Δ < 0
        self.play(b.animate.set_value(2), run_time=1.5)
        self.play(c.animate.set_value(1), run_time=1)          # Δ = 0
        self.play(a.animate.set_value(-0.5), run_time=2)       # concavidade para baixo
        self.play(b.animate.set_value(-1), c.animate.set_value(3), run_time=2)
        self.play(a.animate.set_value(2), b.animate.set_value(0), c.animate.set_value(-3), run_time=2)
        self.wait(2)
