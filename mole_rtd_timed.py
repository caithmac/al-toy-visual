"""
MolE-RTD: Precisely Timed Animation
Each chunk's duration drives the waiting time.
Audio will be muxed separately for frame-perfect sync.
"""
from manim import *

BG = "#0A0A14"
CYAN = "#00D4FF"; PURPLE = "#7B2FF7"; GREEN = "#00FF96"
GOLD = "#FFD700"; ORANGE = "#FF9944"; WHITE = "#EAEAEA"; DIM = "#666688"; RED = "#FF4444"
MONO = "Consolas"

# Exact durations from TTS chunks
D = {
    1: 10.656, 2: 15.024, 3: 17.808, 4: 12.264,
    5: 18.576, 6: 16.056, 7: 17.592, 8: 17.112,
    9: 20.184, 10: 21.960, 11: 17.016, 12: 32.880,
}

def boxed(text, color, w=2.2, h=0.7):
    r = Rectangle(width=w, height=h, color=color, fill_opacity=0.15, stroke_width=2)
    t = Text(text, font_size=16, color=color, font=MONO).move_to(r)
    return VGroup(r, t)


class MolERTD_Timed(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ═══ CHUNK 1: Title (10.7s) ═══════════════════════════
        title = Text("MolE-RTD", font_size=52, color=CYAN, weight=BOLD, font=MONO)
        sub = Text("Molecular Encoder with Replaced Token Detection",
                  font_size=20, color=DIM, font=MONO).next_to(title, DOWN, buff=0.3)
        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(sub), run_time=0.8)
        self.wait(D[1] - 1.8)  # fill remaining chunk time

        # ═══ CHUNK 2: SMILES + Molecule (15.0s) ═══════════════
        self.play(FadeOut(title), FadeOut(sub), run_time=0.5)

        smi = Text('SMILES: "CCO"  →  ethanol', font_size=30, color=WHITE, font=MONO)
        self.play(Write(smi), run_time=0.8)

        c1 = Circle(0.4, color=GREEN, fill_opacity=0.3, stroke_width=3)
        c1t = Text("C₁", font_size=20, color=GREEN, font=MONO).move_to(c1); c1g = VGroup(c1, c1t)
        c2 = Circle(0.4, color=GREEN, fill_opacity=0.3, stroke_width=3)
        c2t = Text("C₂", font_size=20, color=GREEN, font=MONO).move_to(c2); c2g = VGroup(c2, c2t)
        o1 = Circle(0.4, color=RED, fill_opacity=0.25, stroke_width=3)
        o1t = Text("O", font_size=20, color=RED, font=MONO).move_to(o1); og = VGroup(o1, o1t)
        atoms = VGroup(c1g, c2g, og).arrange(RIGHT, buff=1.2).next_to(smi, DOWN, buff=0.8)
        b1 = Line(c1g.get_right(), c2g.get_left(), color=WHITE, stroke_width=2)
        b2 = Line(c2g.get_right(), og.get_left(), color=WHITE, stroke_width=2)

        self.play(Create(c1g), Create(c2g), Create(og), run_time=1.5)
        self.play(Create(b1), Create(b2), run_time=0.5)
        stats = Text("3 heavy atoms · sp³ · 2 bonds", font_size=16, color=DIM, font=MONO)
        stats.next_to(atoms, DOWN, buff=0.6)
        self.play(Write(stats), run_time=0.8)
        self.wait(D[2] - 3.6)

        # ═══ CHUNK 3: Tokenization (17.8s) ════════════════════
        self.play(FadeOut(smi), FadeOut(atoms), FadeOut(b1), FadeOut(b2), FadeOut(stats), run_time=0.5)

        tok_title = Text("Tokenization: Morgan Fingerprint (r=0)",
                        font_size=28, color=CYAN, weight=BOLD, font=MONO).to_edge(UP, buff=0.4)
        self.play(Write(tok_title), run_time=0.8)

        atom_boxes = VGroup(
            boxed("C₁ (sp³)", GREEN), boxed("C₂ (sp³ adj O)", GREEN), boxed("O (hydroxyl)", RED)
        ).arrange(RIGHT, buff=0.5).next_to(tok_title, DOWN, buff=0.9)
        self.play(Create(atom_boxes), run_time=1.5)
        self.wait(D[3] - 2.8)

        # ═══ CHUNK 4: Why radius 0 (12.3s) ════════════════════
        why = Text("⚠ Why radius 0?", font_size=24, color=GOLD, font=MONO, weight=BOLD)
        why.next_to(atom_boxes, DOWN, buff=0.7)
        detail = Text("Larger radii → neighborhood in tokens → model cheats",
                     font_size=15, color=DIM, font=MONO).next_to(why, DOWN, buff=0.2)
        self.play(Write(why), run_time=0.7)
        self.play(Write(detail), run_time=1.0)
        self.wait(D[4] - 1.7)

        # ═══ CHUNK 5: 211 tokens + CLS (18.6s) ════════════════
        self.play(FadeOut(why), FadeOut(detail), run_time=0.4)

        tok_data = [("C_sp3 → 17", GREEN), ("C_sp3_adjO → 23", GREEN), ("O_hydroxyl → 89", RED)]
        tok_boxes = VGroup()
        for i, (txt, col) in enumerate(tok_data):
            b = boxed(txt, col, w=2.4)
            b.next_to(atom_boxes[i], DOWN, buff=0.8)
            arr = Arrow(atom_boxes[i].get_bottom(), b.get_top(), color=PURPLE, stroke_width=2,
                       max_tip_length_to_length_ratio=0.2)
            self.play(GrowArrow(arr), Create(b), run_time=0.6)
            tok_boxes.add(b)

        cls_note = Text("[CLS=1]  [C₁=17]  [C₂=23]  [O=89]",
                       font_size=22, color=WHITE, font=MONO).next_to(tok_boxes, DOWN, buff=0.9)
        self.play(Write(cls_note), run_time=1.0)
        self.wait(D[5] - 3.2)

        # ═══ CHUNK 6: Distance Matrix (16.1s) ═════════════════
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)

        dm_t = Text("Distance Matrix → Positional Encoding",
                   font_size=26, color=CYAN, weight=BOLD, font=MONO).to_edge(UP, buff=0.4)
        self.play(Write(dm_t), run_time=0.8)

        rows = VGroup()
        for rd in [["0","1","2"],["1","0","1"],["2","1","0"]]:
            cells = VGroup()
            for d in rd:
                c = CYAN if d=="0" else WHITE
                cell = Rectangle(width=0.9, height=0.6, color=DIM, fill_opacity=0.08, stroke_width=1)
                lbl = Text(d, font_size=24, color=c, font=MONO, weight=BOLD).move_to(cell)
                cells.add(VGroup(cell, lbl))
            cells.arrange(RIGHT, buff=0.1); rows.add(cells)
        rows.arrange(DOWN, buff=0.1)
        rl = VGroup(*[Text(r,font_size=16,color=DIM,font=MONO) for r in ["C₁","C₂","O"]])
        rl.arrange(DOWN,buff=0.7).next_to(rows,LEFT,buff=0.3)
        cl = VGroup(*[Text(c,font_size=16,color=DIM,font=MONO) for c in ["C₁","C₂","O"]])
        cl.arrange(RIGHT,buff=0.95).next_to(rows,UP,buff=0.15)
        mg = VGroup(rl,cl,rows).next_to(dm_t,DOWN,buff=0.6)

        self.play(Create(rows), Write(rl), Write(cl), run_time=2.0)
        note = Text("Bond distance → relative position in attention",
                   font_size=14, color=DIM, font=MONO).next_to(mg, DOWN, buff=0.5)
        self.play(Write(note), run_time=1.0)
        self.wait(D[6] - 3.8)

        # ═══ CHUNK 7: Disentangled Attention (17.6s) ══════════
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)

        att_t = Text("Disentangled Attention", font_size=28, color=CYAN, weight=BOLD, font=MONO)
        att_t.to_edge(UP, buff=0.4)
        self.play(Write(att_t), run_time=0.8)

        formula = VGroup(
            Text("Attention = softmax( ", font_size=22, color=CYAN, font=MONO),
            Text("QcKcᵀ", font_size=22, color=GOLD, font=MONO, weight=BOLD),
            Text(" + ", font_size=22, color=WHITE, font=MONO),
            Text("QcKrᵀ", font_size=22, color=ORANGE, font=MONO, weight=BOLD),
            Text(" + ", font_size=22, color=WHITE, font=MONO),
            Text("QrKcᵀ", font_size=22, color=GREEN, font=MONO, weight=BOLD),
            Text(" ) × V", font_size=22, color=CYAN, font=MONO),
        ).arrange(RIGHT, buff=0.08).next_to(att_t, DOWN, buff=0.7)
        self.play(Write(formula), run_time=2.0)

        legend_items = [
            (GOLD, "Content↔Content"), (ORANGE, "Content→Position (c2p)"), (GREEN, "Position→Content (p2c)")
        ]
        legend = VGroup()
        for col, txt in legend_items:
            legend.add(VGroup(Dot(color=col,radius=0.08),
                Text(txt,font_size=14,color=col,font=MONO)).arrange(RIGHT,buff=0.15))
        legend.arrange(RIGHT, buff=0.5).next_to(formula, DOWN, buff=0.8)
        self.play(FadeIn(legend), run_time=1.0)
        self.wait(D[7] - 4.6)

        # ═══ CHUNK 8: Attention Example (17.1s) ═══════════════
        self.play(FadeOut(formula), FadeOut(legend), run_time=0.4)

        ex_t = Text("C₂ attending to all atoms in ethanol",
                   font_size=24, color=PURPLE, weight=BOLD, font=MONO).next_to(att_t, DOWN, buff=0.6)
        self.play(Write(ex_t), run_time=0.8)

        tbl_data = [
            ["Target","Dist","QcKc","QcKr","QrKc","Total"],
            ["[CLS]","0",".12",".05",".03",".20"],
            ["C₁ ⬅","1",".35",".28",".15",".78"],
            ["C₂","0",".40",".02",".01",".43"],
            ["O","1",".18",".22",".12",".52"],
        ]
        tbl = VGroup()
        for i,row in enumerate(tbl_data):
            rg = VGroup()
            for j,cell in enumerate(row):
                hl = (i==2); hd = (i==0)
                c = CYAN if hd else GOLD if (hl and j>=2) else WHITE
                sz = 16 if hd else 14
                w = BOLD if hd or (hl and j==5) else NORMAL
                rg.add(Text(cell,font_size=sz,color=c,font=MONO,weight=w))
            rg.arrange(RIGHT,buff=0.4)
            if i==2:
                bg = Rectangle(width=rg.width+0.3,height=rg.height+0.2,
                              color=GOLD,fill_opacity=0.08,stroke_width=1).move_to(rg)
                rg = VGroup(bg,rg)
            tbl.add(rg)
        tbl.arrange(DOWN,buff=0.2).next_to(ex_t,DOWN,buff=0.5)

        for r in tbl: self.play(FadeIn(r), run_time=0.3)
        self.wait(D[8] - 2.3)

        # ═══ CHUNK 9: 12 Layers + CLS (20.2s) ═════════════════
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)

        lay_t = Text("12-Layer Transformer → CLS Embedding",
                    font_size=26, color=CYAN, weight=BOLD, font=MONO).to_edge(UP, buff=0.4)
        self.play(Write(lay_t), run_time=0.8)

        layers_vg = VGroup()
        for i in range(12):
            b = Rectangle(width=2.2, height=0.3, color=PURPLE, fill_opacity=0.08+i*0.07, stroke_width=1)
            l = Text(f"Layer {i+1}", font_size=11, color=CYAN if i==11 else DIM, font=MONO).move_to(b)
            layers_vg.add(VGroup(b,l))
        layers_vg.arrange(DOWN,buff=0.06).next_to(lay_t,DOWN,buff=0.5)
        self.play(Create(layers_vg), run_time=3.0)

        cls_b = Rectangle(width=2.6, height=0.6, color=GREEN, fill_opacity=0.2, stroke_width=2, stroke_color=GREEN)
        cls_l = Text("CLS Token [768-dim]", font_size=16, color=GREEN, font=MONO, weight=BOLD).move_to(cls_b)
        cls_g = VGroup(cls_b, cls_l).next_to(layers_vg, DOWN, buff=0.3)
        cls_a = Arrow(layers_vg.get_bottom(), cls_g.get_top(), color=GREEN, stroke_width=2)
        self.play(GrowArrow(cls_a), Create(cls_g), run_time=1.5)
        self.wait(D[9] - 6.1)

        # ═══ CHUNK 10: RTD Pretraining (22.0s) ════════════════
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)

        rtd_t = Text("RTD Pretraining", font_size=28, color=CYAN, weight=BOLD, font=MONO)
        rtd_t.to_edge(UP, buff=0.35)
        self.play(Write(rtd_t), run_time=0.8)

        gen_b = Rectangle(width=4.0, height=2.5, color=ORANGE, fill_opacity=0.1, stroke_width=2).to_edge(LEFT,buff=0.5).shift(UP*0.2)
        gen_l = Text("Generator", font_size=20, color=ORANGE, font=MONO, weight=BOLD).next_to(gen_b,UP,buff=0.15)
        gen_items = VGroup(
            Text("3 layers, ~7M params",font_size=14,color=DIM,font=MONO),
            Text("Masks 15% of tokens",font_size=14,color=WHITE,font=MONO),
            Text("Predicts & fills in",font_size=14,color=DIM,font=MONO),
            Text("Loss: CrossEntropy",font_size=14,color=DIM,font=MONO),
        ).arrange(DOWN,buff=0.15,aligned_edge=LEFT).move_to(gen_b)

        disc_b = Rectangle(width=4.2, height=2.5, color=CYAN, fill_opacity=0.1, stroke_width=2)
        disc_b.next_to(gen_b,RIGHT,buff=0.8).shift(UP*0.2)
        disc_l = Text("Discriminator", font_size=20, color=CYAN, font=MONO, weight=BOLD).next_to(disc_b,UP,buff=0.15)
        disc_items = VGroup(
            Text("12 layers, ~89M params",font_size=14,color=DIM,font=MONO),
            Text("Classifies EVERY token",font_size=14,color=WHITE,font=MONO),
            Text("Real(0) or Replaced(1)",font_size=14,color=DIM,font=MONO),
            Text("Loss: BCE × 50",font_size=14,color=CYAN,font=MONO),
        ).arrange(DOWN,buff=0.15,aligned_edge=LEFT).move_to(disc_b)

        mid_a = Arrow(gen_b.get_right(), disc_b.get_left(), color=PURPLE, stroke_width=4, buff=0.1)

        self.play(Create(gen_b), Write(gen_l), run_time=0.8)
        self.play(FadeIn(gen_items), run_time=1.2)
        self.play(Create(disc_b), Write(disc_l), run_time=0.8)
        self.play(GrowArrow(mid_a), run_time=0.5)
        self.play(FadeIn(disc_items), run_time=1.2)
        self.wait(D[10] - 5.3)

        # ═══ CHUNK 11: Stats (17.0s) ══════════════════════════
        ex = Text("[CLS]=1  C₁→[MASK]→17✓  C₂=23  O=89  →  Labels: [0,0,0,0]",
                 font_size=14, color=WHITE, font=MONO)
        ex.next_to(VGroup(gen_b,disc_b),DOWN,buff=0.8)
        self.play(Write(ex), run_time=1.0)
        self.wait(D[11] - 1.8)

        # ═══ CHUNK 12: Full Pipeline + Results (32.9s) ════════
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)

        pipe_t = Text("End-to-End Pipeline", font_size=28, color=CYAN, weight=BOLD, font=MONO)
        self.play(Write(pipe_t), run_time=0.8)
        pipe_t.to_edge(UP, buff=0.4)

        stages = [
            ("SMILES",GREEN),("Tokenize",PURPLE),("Distance\nMatrix",ORANGE),
            ("Embed\n768-dim",GOLD),("Attention\n×12",CYAN),("CLS\n768-dim",GREEN),("Predict\nXGBoost",PURPLE),
        ]
        sb = VGroup()
        for txt,col in stages:
            b = Rectangle(width=1.5, height=1.0, color=col, fill_opacity=0.12, stroke_width=2)
            l = Text(txt,font_size=13,color=col,font=MONO,weight=BOLD).move_to(b)
            sb.add(VGroup(b,l))
        sb.arrange(RIGHT,buff=0.12).next_to(pipe_t,DOWN,buff=0.8)
        arrows_v = VGroup()
        for i in range(len(sb)-1):
            arrows_v.add(Arrow(sb[i].get_right(),sb[i+1].get_left(),color=DIM,stroke_width=2,buff=0.06,max_tip_length_to_length_ratio=0.3))

        self.play(Create(sb), run_time=3.0)
        self.play(*[GrowArrow(a) for a in arrows_v], run_time=1.0)

        st = VGroup(
            Text("89M params · 4×A100 · 29 hrs · 415M molecules · Loss: 0.95",
                font_size=16,color=DIM,font=MONO),
            Text("BBBP AUROC: 0.878  (+5.07 over random init)",
                font_size=22,color=GREEN,font=MONO,weight=BOLD),
        ).arrange(DOWN,buff=0.2).next_to(sb,DOWN,buff=1.0)
        self.play(Write(st[0]), run_time=1.0)
        self.play(Write(st[1]), run_time=1.0)
        self.wait(D[12] - 6.8)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
