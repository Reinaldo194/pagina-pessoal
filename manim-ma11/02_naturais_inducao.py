"""
MA11 - Unidade 2: Números naturais e Princípio de Indução

Renderizar:  manim -pql 02_naturais_inducao.py SomaImpares
             manim -pql 02_naturais_inducao.py DominoInducao
             manim -pql 02_naturais_inducao.py SomaNaturais
"""
from manim import *
import numpy as np


class SomaImpares(Scene):
    """1 + 3 + 5 + ... + (2n-1) = n^2, com 'gnômons' em forma de L."""

    def construct(self):
        N = 6
        lado = 0.6
        cores = color_gradient([BLUE, GREEN, YELLOW, ORANGE, RED, PURPLE], N)
        titulo = MathTex(r"1 + 3 + 5 + \cdots + (2n-1) = n^2").to_edge(UP)
        self.play(Write(titulo))

        origem = LEFT * 4.5 + DOWN * 2.3
        ancora = RIGHT * 0.3 + UP * 1  # a soma cresce para a direita a partir daqui
        soma = MathTex("1", font_size=36).move_to(ancora, aligned_edge=LEFT)
        resultado = MathTex("= 1 = 1^2", font_size=36).next_to(soma, DOWN, aligned_edge=LEFT)
        self.play(Write(soma), Write(resultado))

        termos = "1"
        for k in range(1, N + 1):
            # o k-ésimo gnômon tem 2k-1 quadradinhos
            quad = VGroup()
            for i in range(k):
                for j in range(k):
                    if i == k - 1 or j == k - 1:
                        q = Square(lado, fill_color=cores[k - 1], fill_opacity=0.8,
                                   stroke_color=WHITE, stroke_width=2)
                        q.move_to(origem + RIGHT * lado * i + UP * lado * j)
                        quad.add(q)
            n_q = MathTex(str(2 * k - 1), color=cores[k - 1], font_size=30)
            n_q.next_to(quad, RIGHT, buff=0.1).align_to(quad, UP)
            self.play(LaggedStart(*[FadeIn(q, scale=0.5) for q in quad],
                                  lag_ratio=0.08), run_time=1)
            if k > 1:
                termos += f" + {2 * k - 1}"
                nova_soma = MathTex(termos, font_size=36).move_to(ancora, aligned_edge=LEFT)
                novo_res = MathTex(f"= {k * k} = {k}^2", font_size=36).next_to(nova_soma, DOWN, aligned_edge=LEFT)
                self.play(Transform(soma, nova_soma), Transform(resultado, novo_res))
            self.wait(0.4)

        passo = MathTex(r"n^2 + (2n+1) = (n+1)^2", color=YELLOW).to_edge(DOWN)
        self.play(Write(passo))
        self.wait(2)


class DominoInducao(Scene):
    """Metáfora do dominó: P(1) verdadeira e P(n) => P(n+1)."""

    def construct(self):
        titulo = Text("Princípio da Indução", font_size=40).to_edge(UP)
        hip = VGroup(
            MathTex(r"\text{(i) } P(1) \text{ é verdadeira}"),
            MathTex(r"\text{(ii) } P(n) \Rightarrow P(n+1)"),
            MathTex(r"\Longrightarrow\ P(n) \text{ vale para todo } n \in \mathbb{N}", color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT).next_to(titulo, DOWN)
        self.play(Write(titulo))
        self.play(Write(hip[0]), Write(hip[1]))

        n = 10
        pecas = VGroup(*[
            Rectangle(width=0.25, height=1.6, fill_color=BLUE_D, fill_opacity=1,
                      stroke_color=WHITE)
            for _ in range(n)
        ]).arrange(RIGHT, buff=0.75).shift(DOWN * 1.8)
        rotulos = VGroup(*[
            MathTex(f"P({i + 1})", font_size=26).next_to(p, DOWN)
            for i, p in enumerate(pecas)
        ])
        chao = Line(pecas.get_left() + LEFT, pecas.get_right() + RIGHT * 2).next_to(pecas, DOWN, buff=0)
        self.play(Create(chao), FadeIn(pecas), FadeIn(rotulos))

        # cada peça gira em torno do seu canto inferior direito até encostar na próxima;
        # a última cai deitada no chão
        encosta = np.arcsin(0.75 / 1.6)
        for i, p in enumerate(pecas):
            ang = encosta if i < n - 1 else PI / 2
            self.play(p.animate.set_fill(GREEN).rotate(-ang, about_point=p.get_corner(DR)),
                      run_time=0.35, rate_func=rush_into)
        self.play(Write(hip[2]))
        self.wait(2)


class SomaNaturais(Scene):
    """1 + 2 + ... + n = n(n+1)/2, pela 'escada' duplicada (Gauss)."""

    def construct(self):
        n = 6
        s = 0.55
        titulo = MathTex(r"1 + 2 + \cdots + n = \frac{n(n+1)}{2}").to_edge(UP)
        self.play(Write(titulo))

        def escada(cor):
            g = VGroup()
            for i in range(n):
                for j in range(i + 1):
                    q = Square(s, fill_color=cor, fill_opacity=0.8, stroke_color=WHITE, stroke_width=2)
                    q.move_to(RIGHT * s * i + UP * s * j)
                    g.add(q)
            return g

        e1 = escada(BLUE).move_to(ORIGIN).shift(DOWN * 0.6 + LEFT * 3)
        self.play(LaggedStart(*[FadeIn(q) for q in e1], lag_ratio=0.03))
        e2 = escada(ORANGE).move_to(e1)
        self.add(e2)
        # gira a cópia 180° e encaixa sobre a primeira, formando n x (n+1)
        self.play(Rotate(e2, PI))
        self.play(e2.animate.shift(UP * s))
        chave_h = Brace(VGroup(e1, e2), DOWN)
        chave_v = Brace(VGroup(e1, e2), RIGHT)
        rot_h, rot_v = chave_h.get_tex("n"), chave_v.get_tex("n+1")
        self.play(GrowFromCenter(chave_h), Write(rot_h),
                  GrowFromCenter(chave_v), Write(rot_v))
        conta = MathTex(r"2\,(1+2+\cdots+n) = n(n+1)", color=YELLOW, font_size=36).next_to(rot_v, RIGHT, buff=0.6)
        self.play(Write(conta))
        self.wait(2)
