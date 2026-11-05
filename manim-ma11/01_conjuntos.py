"""
MA11 - Unidade 1: Conjuntos
Operações com conjuntos e Leis de De Morgan via diagramas de Venn.

Renderizar:  manim -pql 01_conjuntos.py OperacoesConjuntos
             manim -pql 01_conjuntos.py DeMorgan
"""
from manim import *


def venn(raio=1.6, dx=1.0):
    """Retorna (universo, A, B, rótulos) centrados na origem."""
    U = Rectangle(width=8, height=5, color=WHITE)
    A = Circle(radius=raio, color=BLUE).shift(LEFT * dx)
    B = Circle(radius=raio, color=RED).shift(RIGHT * dx)
    rotulos = VGroup(
        MathTex("A", color=BLUE).next_to(A, UL, buff=-0.3),
        MathTex("B", color=RED).next_to(B, UR, buff=-0.3),
        MathTex("U").next_to(U.get_corner(UL), DR, buff=0.2),
    )
    return U, A, B, rotulos


def regiao(nome, U, A, B):
    """Região preenchida correspondente a cada operação."""
    if nome == "uniao":
        r = Union(A, B)
    elif nome == "intersecao":
        r = Intersection(A, B)
    elif nome == "diferenca":
        r = Difference(A, B)
    elif nome == "compl_uniao":
        r = Difference(U, Union(A, B))
    elif nome == "compl_inter":
        r = Difference(U, Intersection(A, B))
    elif nome == "compl_A":
        r = Difference(U, A)
    elif nome == "compl_B":
        r = Difference(U, B)
    return r.set_fill(YELLOW, opacity=0.5).set_stroke(width=0)


class OperacoesConjuntos(Scene):
    def construct(self):
        titulo = Text("Operações com conjuntos", font_size=40).to_edge(UP)
        U, A, B, rot = venn()
        diagrama = VGroup(U, A, B, rot).scale(0.85).shift(DOWN * 0.4)
        self.play(Write(titulo))
        self.play(Create(U), Create(A), Create(B), FadeIn(rot))

        operacoes = [
            ("uniao", r"A \cup B = \{x \mid x \in A \text{ ou } x \in B\}"),
            ("intersecao", r"A \cap B = \{x \mid x \in A \text{ e } x \in B\}"),
            ("diferenca", r"A \setminus B = \{x \mid x \in A \text{ e } x \notin B\}"),
            ("compl_A", r"A^c = \{x \in U \mid x \notin A\}"),
        ]
        formula_atual = None
        regiao_atual = None
        for nome, tex in operacoes:
            r = regiao(nome, U, A, B)
            f = MathTex(tex, font_size=36).to_edge(DOWN)
            if regiao_atual is None:
                self.play(FadeIn(r), Write(f))
            else:
                self.play(ReplacementTransform(regiao_atual, r),
                          ReplacementTransform(formula_atual, f))
            # mantém os contornos por cima do preenchimento
            self.bring_to_front(A, B, rot)
            regiao_atual, formula_atual = r, f
            self.wait(1.5)
        self.play(FadeOut(regiao_atual), FadeOut(formula_atual))
        self.wait()


class DeMorgan(Scene):
    """(A ∪ B)^c = A^c ∩ B^c, construído pela interseção de A^c e B^c."""

    def construct(self):
        titulo = MathTex(r"(A \cup B)^c = A^c \cap B^c", font_size=48).to_edge(UP)
        self.play(Write(titulo))

        def painel():
            U, A, B, rot = venn()
            return VGroup(U, A, B, rot).scale(0.45)

        esq, dir_ = painel(), painel()
        esq.to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        dir_.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.3)
        self.play(FadeIn(esq), FadeIn(dir_))

        # Lado esquerdo: complementar da união
        Ue, Ae, Be, _ = esq
        r_esq = regiao("compl_uniao", Ue, Ae, Be)
        leg_esq = MathTex(r"(A\cup B)^c").next_to(esq, DOWN)
        self.play(FadeIn(r_esq), Write(leg_esq))

        # Lado direito: A^c (azul) e B^c (vermelho), depois a interseção
        Ud, Ad, Bd, _ = dir_
        ac = Difference(Ud, Ad).set_fill(BLUE, 0.35).set_stroke(width=0)
        bc = Difference(Ud, Bd).set_fill(RED, 0.35).set_stroke(width=0)
        leg_dir = MathTex(r"A^c", r"\cap", r"B^c").next_to(dir_, DOWN)
        self.play(FadeIn(ac), Write(leg_dir[0]))
        self.play(FadeIn(bc), Write(leg_dir[1:]))
        inter = regiao("compl_uniao", Ud, Ad, Bd)
        self.play(FadeOut(ac), FadeOut(bc), FadeIn(inter))
        self.wait()

        igual = MathTex("=", font_size=72)
        self.play(Write(igual))
        self.play(Indicate(r_esq), Indicate(inter))
        self.wait(2)
