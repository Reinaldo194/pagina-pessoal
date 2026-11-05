"""
MA11 - Unidade 4: Números reais

Renderizar:  manim -pql 04_numeros_reais.py RaizDoisNaReta
             manim -pql 04_numeros_reais.py IntervalosEncaixados
"""
from manim import *
import numpy as np


class RaizDoisNaReta(Scene):
    """Construção de sqrt(2) com régua e compasso e a prova de irracionalidade."""

    def construct(self):
        reta = NumberLine(x_range=[-1, 3, 1], length=8, include_numbers=True).shift(DOWN * 1.5 + LEFT * 2)
        self.play(Create(reta))
        p0, p1 = reta.n2p(0), reta.n2p(1)
        u = p1[0] - p0[0]
        quad = Square(side_length=u, color=BLUE).move_to(p0, aligned_edge=DL)
        self.play(Create(quad))
        diag = Line(p0, p0 + np.array([u, u, 0]), color=YELLOW)
        rot = MathTex(r"\sqrt{1^2+1^2}=\sqrt 2", font_size=32, color=YELLOW).next_to(diag.get_center(), UL, buff=0.1)
        self.play(Create(diag), Write(rot))

        # compasso: gira a diagonal até a reta
        arco = Arc(radius=diag.get_length(), start_angle=PI / 4, angle=-PI / 4,
                   arc_center=p0, color=YELLOW)
        self.play(Create(arco), Rotate(diag.copy(), -PI / 4, about_point=p0))
        ponto = Dot(reta.n2p(np.sqrt(2)), color=YELLOW)
        rotulo = MathTex(r"\sqrt 2", color=YELLOW).next_to(ponto, DOWN, buff=0.5)
        self.play(FadeIn(ponto), Write(rotulo))
        self.wait()

        prova = VGroup(
            MathTex(r"\text{Suponha } \sqrt2=\tfrac{p}{q},\ \operatorname{mdc}(p,q)=1"),
            MathTex(r"p^2 = 2q^2 \Rightarrow p \text{ par},\ p=2k"),
            MathTex(r"4k^2 = 2q^2 \Rightarrow q^2=2k^2 \Rightarrow q \text{ par}"),
            MathTex(r"\text{Contradição!}\ \ \sqrt 2 \notin \mathbb{Q}", color=RED),
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.7).to_corner(UR)
        for linha in prova:
            self.play(Write(linha))
            self.wait(0.6)
        self.wait(2)


def dec(x, casas):
    """Número com vírgula decimal, no formato do LaTeX."""
    return f"{x:.{casas}f}".replace(".", "{,}")


class IntervalosEncaixados(Scene):
    """Aproximações decimais de sqrt(2): cada casa refina o intervalo por 10."""

    def construct(self):
        titulo = MathTex(r"\sqrt2 = 1{,}41421\ldots").to_edge(UP)
        self.play(Write(titulo))
        alvo = np.sqrt(2)
        a, h = 1.0, 1.0
        reta = None
        for k in range(5):
            nova = NumberLine(x_range=[a, a + h, h / 10], length=10,
                              include_ticks=True).shift(DOWN * 0.5)
            extremos = VGroup(MathTex(dec(a, k), font_size=30).next_to(nova.n2p(a), DOWN),
                              MathTex(dec(a + h, k), font_size=30).next_to(nova.n2p(a + h), DOWN))
            ponto = Dot(nova.n2p(alvo), color=YELLOW)
            grupo = VGroup(nova, extremos, ponto)
            if reta is None:
                self.play(Create(nova), Write(extremos), FadeIn(ponto))
            else:
                self.play(ReplacementTransform(reta, grupo))
            reta = grupo
            # subintervalo de tamanho h/10 que contém sqrt(2)
            j = int((alvo - a) // (h / 10))
            novo_a = a + j * h / 10
            destaque = Line(nova.n2p(novo_a), nova.n2p(novo_a + h / 10), color=RED, stroke_width=10)
            desig = MathTex(
                rf"{dec(novo_a, k + 1)} < \sqrt2 < {dec(novo_a + h / 10, k + 1)}",
                font_size=36).shift(UP * 1.3)
            self.play(Create(destaque), FadeIn(desig))
            self.wait(0.8)
            self.play(FadeOut(destaque), FadeOut(desig))
            a, h = novo_a, h / 10
        concl = Tex(r"Intervalos encaixados de comprimento $10^{-n}$ determinam um único real.",
                    font_size=34).to_edge(DOWN)
        self.play(Write(concl))
        self.wait(2)
