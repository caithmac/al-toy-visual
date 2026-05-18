"""
MolE-RTD: Narrated Animation — narration-first, visuals follow.
Single scene with embedded audio, timed to narration beats.
"""
from manim import *

BG = "#0A0A14"
CYAN = "#00D4FF"
PURPLE = "#7B2FF7"
GREEN = "#00FF96"
GOLD = "#FFD700"
ORANGE = "#FF9944"
WHITE = "#EAEAEA"
DIM = "#666688"
RED = "#FF4444"
MONO = "Consolas"


class MolERTD_Narrated(Scene):
    def construct(self):
        self.camera.background_color = BG

        # Embed the narration audio
        self.add_sound("C:/tmp/narration_synced.mp3", gain=1.0)

        # ═════════════════════════════════════════════════════
        # SECTION 1: Title + SMILES (0:00 - 0:25)
        # "MolE-RTD is a molecular encoder... C-C-O... three heavy atoms"
        # ═════════════════════════════════════════════════════

        title = Text("MolE-RTD", font_size=48, color=CYAN, weight=BOLD, font=MONO)
        subtitle = Text("Molecular Encoder with Replaced Token Detection",
                       font_size=20, color=DIM, font=MONO)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle), run_time=0.8)
        self.wait(2.5)  # ~4.8s — "MolE-RTD is a molecular encoder..."

        self.play(FadeOut(title), FadeOut(subtitle), run_time=0.5)

        # Show SMILES
        smiles_label = Text('SMILES: "CCO" (ethanol)', font_size=32, color=WHITE, font=MONO)
        self.play(Write(smiles_label), run_time=1.0)
        self.wait(2.0)  # "ethanol, CCO"

        # Show molecule
        c1 = Circle(radius=0.4, color=GREEN, fill_opacity=0.3, stroke_width=3)
        c1_t = Text("C₁", font_size=20, color=GREEN, font=MONO).move_to(c1)
        c1_g = VGroup(c1, c1_t).shift(LEFT * 2 + UP * 1.5)

        c2 = Circle(radius=0.4, color=GREEN, fill_opacity=0.3, stroke_width=3)
        c2_t = Text("C₂", font_size=20, color=GREEN, font=MONO).move_to(c2)
        c2_g = VGroup(c2, c2_t).shift(UP * 1.5)

        o1 = Circle(radius=0.4, color=RED, fill_opacity=0.25, stroke_width=3)
        o1_t = Text("O", font_size=20, color=RED, font=MONO).move_to(o1)
        o_g = VGroup(o1, o1_t).shift(RIGHT * 2 + UP * 1.5)

        b1 = Line(c1.get_right(), c2.get_left(), color=WHITE, stroke_width=2)
        b2 = Line(c2.get_right(), o1.get_left(), color=WHITE, stroke_width=2)

        atoms_group = VGroup(c1_g, c2_g, o_g, b1, b2)
        atoms_group.next_to(smiles_label, DOWN, buff=0.8)

        self.play(Create(c1_g), Create(c2_g), Create(o_g), Create(b1), Create(b2), run_time=2.0)
        self.wait(3.0)  # "three heavy atoms... two sp3 carbons... hydroxyl oxygen"

        stats = Text("3 heavy atoms · sp³ hybridized · 2 bonds",
                     font_size=16, color=DIM, font=MONO)
        stats.next_to(atoms_group, DOWN, buff=0.6)
        self.play(Write(stats), run_time=1.0)
        self.wait(3.0)  # "connected by two single bonds"

        # ═════════════════════════════════════════════════════
        # SECTION 2: Tokenization (0:25 - 1:05)
        # "Morgan fingerprints with radius zero... 211 tokens..."
        # ═════════════════════════════════════════════════════

        self.play(FadeOut(smiles_label), FadeOut(atoms_group), FadeOut(stats), run_time=0.6)

        tok_title = Text("Tokenization: Morgan Fingerprint (r=0)",
                        font_size=28, color=CYAN, weight=BOLD, font=MONO)
        tok_title.to_edge(UP, buff=0.4)
        self.play(Write(tok_title), run_time=1.0)
        self.wait(2.0)

        # Atom → token mapping
        atoms_row = VGroup(
            self._make_atom_box("C₁ (sp³)", GREEN),
            self._make_atom_box("C₂ (sp³ adj O)", GREEN),
            self._make_atom_box("O (hydroxyl)", RED),
        ).arrange(RIGHT, buff=0.6)
        atoms_row.next_to(tok_title, DOWN, buff=0.8)

        self.play(Create(atoms_row), run_time=2.0)
        self.wait(2.0)  # "each atom gets fingerprinted by elemental type alone"

        # WHY radius 0
        why_note = Text("⚠ Why radius 0?", font_size=22, color=GOLD, font=MONO, weight=BOLD)
        why_note.next_to(atoms_row, DOWN, buff=0.8)
        why_detail = Text("Larger radii → neighborhood in tokens → RTD becomes trivial",
                         font_size=16, color=DIM, font=MONO)
        why_detail.next_to(why_note, DOWN, buff=0.2)

        self.play(Write(why_note), run_time=0.8)
        self.play(Write(why_detail), run_time=1.2)
        self.wait(4.0)  # "deliberate choice... model could cheat..."

        self.play(FadeOut(why_note), FadeOut(why_detail), run_time=0.5)

        # Token IDs
        tokens_data = [
            ("C_sp3", "17", GREEN),
            ("C_sp3_adjO", "23", GREEN),
            ("O_hydroxyl", "89", RED),
        ]
        token_boxes = VGroup()
        arrows_vg = VGroup()
        for i, (name, tid, col) in enumerate(tokens_data):
            box = Rectangle(width=2.0, height=0.65, color=col, fill_opacity=0.15, stroke_width=2)
            label = Text(f"{name} → {tid}", font_size=16, color=col, font=MONO).move_to(box)
            token_boxes.add(VGroup(box, label))
            arr = Arrow(atoms_row[i].get_bottom(), box.get_top() + UP * 0.1,
                       color=PURPLE, stroke_width=2, max_tip_length_to_length_ratio=0.15)

        token_boxes.arrange(RIGHT, buff=0.6)
        token_boxes.next_to(atoms_row, DOWN, buff=1.2)

        for i, (tb, arr) in enumerate(zip(token_boxes, [Arrow(atoms_row[j].get_bottom(), token_boxes[j].get_top(),
                       color=PURPLE, stroke_width=2, max_tip_length_to_length_ratio=0.15) for j in range(3)])):
            self.play(GrowArrow(arr), Create(tb), run_time=0.8)

        self.wait(3.0)  # "211 vocabulary tokens... CLS, PAD, MASK"

        # CLS insert
        cls_note = Text("Prepend [CLS] token at position 0",
                       font_size=22, color=GOLD, font=MONO, weight=BOLD)
        cls_note.next_to(token_boxes, DOWN, buff=1.0)
        final_seq = Text("[CLS=1]  [C₁=17]  [C₂=23]  [O=89]",
                        font_size=20, color=WHITE, font=MONO)
        final_seq.next_to(cls_note, DOWN, buff=0.3)

        self.play(Write(cls_note), run_time=0.8)
        self.play(Write(final_seq), run_time=1.2)
        self.wait(3.0)  # "CLS... later aggregate information"

        # ═════════════════════════════════════════════════════
        # SECTION 3: Distance Matrix (1:05 - 1:35)
        # ═════════════════════════════════════════════════════

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)

        dm_title = Text("Distance Matrix → Positional Encoding",
                       font_size=28, color=CYAN, weight=BOLD, font=MONO)
        dm_title.to_edge(UP, buff=0.4)
        self.play(Write(dm_title), run_time=1.0)
        self.wait(1.5)

        # Build matrix
        rows = VGroup()
        for i, row_data in enumerate([["0", "1", "2"], ["1", "0", "1"], ["2", "1", "0"]]):
            cells = VGroup()
            for d in row_data:
                c = CYAN if d == "0" else WHITE
                cell = Rectangle(width=0.9, height=0.6, color=DIM, fill_opacity=0.08, stroke_width=1)
                label = Text(d, font_size=24, color=c, font=MONO, weight=BOLD).move_to(cell)
                cells.add(VGroup(cell, label))
            cells.arrange(RIGHT, buff=0.1)
            rows.add(cells)
        rows.arrange(DOWN, buff=0.1)

        rlabels = VGroup(*[Text(r, font_size=18, color=DIM, font=MONO) for r in ["C₁", "C₂", "O"]])
        rlabels.arrange(DOWN, buff=0.7).next_to(rows, LEFT, buff=0.3)
        clabels = VGroup(*[Text(c, font_size=18, color=DIM, font=MONO) for c in ["C₁", "C₂", "O"]])
        clabels.arrange(RIGHT, buff=0.95).next_to(rows, UP, buff=0.15)

        matrix = VGroup(rlabels, clabels, rows).next_to(dm_title, DOWN, buff=0.6)
        self.play(Create(rows), Write(rlabels), Write(clabels), run_time=2.5)
        self.wait(3.0)  # "C1 to itself is zero... C1 to C2 is one"

        note = Text("Bond distance d → row (d + 512) in [1024 × 64] embedding table",
                   font_size=14, color=DIM, font=MONO)
        note.next_to(matrix, DOWN, buff=0.5)
        self.play(Write(note), run_time=1.0)
        self.wait(3.0)  # "graph IS the position"

        # ═════════════════════════════════════════════════════
        # SECTION 4: Disentangled Attention (1:35 - 2:30)
        # ═════════════════════════════════════════════════════

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)

        att_title = Text("Disentangled Attention",
                        font_size=28, color=CYAN, weight=BOLD, font=MONO)
        att_title.to_edge(UP, buff=0.4)
        self.play(Write(att_title), run_time=1.0)
        self.wait(1.0)

        # Formula
        formula = VGroup(
            Text("Attention = softmax( ", font_size=22, color=CYAN, font=MONO),
            Text("QcKcᵀ", font_size=22, color=GOLD, font=MONO, weight=BOLD),
            Text(" + ", font_size=22, color=WHITE, font=MONO),
            Text("QcKrᵀ", font_size=22, color=ORANGE, font=MONO, weight=BOLD),
            Text(" + ", font_size=22, color=WHITE, font=MONO),
            Text("QrKcᵀ", font_size=22, color=GREEN, font=MONO, weight=BOLD),
            Text(" ) × V", font_size=22, color=CYAN, font=MONO),
        ).arrange(RIGHT, buff=0.08)
        formula.next_to(att_title, DOWN, buff=0.7)

        self.play(Write(formula), run_time=2.0)
        self.wait(4.0)  # "content to content... content to position... position to content"

        # Legend
        legend_items = [
            (GOLD, "Content ↔ Content"),
            (ORANGE, "Content → Position (c2p)"),
            (GREEN, "Position → Content (p2c)"),
        ]
        legend = VGroup()
        for color, text in legend_items:
            dot = Dot(color=color, radius=0.08)
            label = Text(text, font_size=14, color=color, font=MONO)
            item = VGroup(dot, label).arrange(RIGHT, buff=0.15)
            legend.add(item)
        legend.arrange(RIGHT, buff=0.5)
        legend.next_to(formula, DOWN, buff=0.8)

        self.play(FadeIn(legend), run_time=1.5)
        self.wait(3.0)

        # Attention example
        self.play(FadeOut(formula), FadeOut(legend), run_time=0.5)

        ex_title = Text("Example: C₂ attending to all atoms",
                       font_size=24, color=PURPLE, weight=BOLD, font=MONO)
        ex_title.next_to(att_title, DOWN, buff=0.6)
        self.play(Write(ex_title), run_time=1.0)
        self.wait(1.5)  # "Let's watch C2 attend"

        # Mini table
        table_data = [
            ["Target", "Dist", "QcKc", "QcKr", "QrKc", "Total"],
            ["[CLS]", "0", ".12", ".05", ".03", ".20"],
            ["C₁ ⬅", "1", ".35", ".28", ".15", ".78"],
            ["C₂", "0", ".40", ".02", ".01", ".43"],
            ["O", "1", ".18", ".22", ".12", ".52"],
        ]

        tbl = VGroup()
        for i, row in enumerate(table_data):
            row_g = VGroup()
            for j, cell in enumerate(row):
                is_header = (i == 0)
                is_hl = (i == 2)
                c = CYAN if is_header else GOLD if (is_hl and j >= 2) else WHITE
                font_sz = 16 if is_header else 14
                w = BOLD if is_header or (is_hl and j == 5) else NORMAL
                t = Text(cell, font_size=font_sz, color=c, font=MONO, weight=w)
                row_g.add(t)
            row_g.arrange(RIGHT, buff=0.45)
            if i == 2:
                bg = Rectangle(width=row_g.width + 0.3, height=row_g.height + 0.2,
                              color=GOLD, fill_opacity=0.08, stroke_width=1).move_to(row_g)
                row_g = VGroup(bg, row_g)
            tbl.add(row_g)
        tbl.arrange(DOWN, buff=0.2)
        tbl.next_to(ex_title, DOWN, buff=0.5)

        for row in tbl:
            self.play(FadeIn(row), run_time=0.4)

        self.wait(5.0)  # "pays most attention to directly bonded neighbor C1"

        # ═════════════════════════════════════════════════════
        # SECTION 5: 12 layers + CLS (2:30 - 2:55)
        # ═════════════════════════════════════════════════════

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)

        stack_title = Text("12-Layer Transformer Stack",
                          font_size=28, color=CYAN, weight=BOLD, font=MONO)
        stack_title.to_edge(UP, buff=0.4)
        self.play(Write(stack_title), run_time=1.0)
        self.wait(1.5)

        # Layer stack
        layers = VGroup()
        for i in range(12):
            box = Rectangle(width=2.0, height=0.35, color=PURPLE,
                          fill_opacity=0.1 + i * 0.06, stroke_width=1)
            label = Text(f"Layer {i+1}", font_size=12, color=CYAN if i == 11 else DIM, font=MONO)
            label.move_to(box)
            layers.add(VGroup(box, label))
        layers.arrange(DOWN, buff=0.08)
        layers.next_to(stack_title, DOWN, buff=0.5)

        self.play(Create(layers), run_time=3.0)
        self.wait(2.0)  # "twelve layers... each refines"

        # CLS output
        cls_box = Rectangle(width=2.4, height=0.7, color=GREEN,
                           fill_opacity=0.2, stroke_width=3, stroke_color=GREEN)
        cls_label = Text("CLS Token [768-dim]", font_size=16, color=GREEN, font=MONO, weight=BOLD)
        cls_label.move_to(cls_box)
        cls_group = VGroup(cls_box, cls_label).next_to(layers, DOWN, buff=0.3)

        cls_arrow = Arrow(layers.get_bottom(), cls_group.get_top(),
                         color=GREEN, stroke_width=2)

        self.play(GrowArrow(cls_arrow), Create(cls_group), run_time=1.5)
        self.wait(3.0)  # "CLS token aggregates... molecular embedding"

        # ═════════════════════════════════════════════════════
        # SECTION 6: RTD Pretraining (2:55 - 3:50)
        # ═════════════════════════════════════════════════════

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)

        rtd_title = Text("RTD Pretraining: Generator → Discriminator",
                        font_size=26, color=CYAN, weight=BOLD, font=MONO)
        rtd_title.to_edge(UP, buff=0.35)
        self.play(Write(rtd_title), run_time=1.0)
        self.wait(1.5)

        # Generator box
        gen_box = Rectangle(width=4.0, height=2.8, color=ORANGE, fill_opacity=0.1, stroke_width=2)
        gen_box.to_edge(LEFT, buff=0.5).shift(UP * 0.2)
        gen_lbl = Text("Generator", font_size=20, color=ORANGE, font=MONO, weight=BOLD)
        gen_lbl.next_to(gen_box, UP, buff=0.15)
        gen_items = VGroup(
            Text("3 layers · ~7M params", font_size=14, color=DIM, font=MONO),
            Text("15% tokens masked", font_size=14, color=WHITE, font=MONO),
            Text("80% → [MASK]", font_size=14, color=DIM, font=MONO),
            Text("10% → random", font_size=14, color=DIM, font=MONO),
            Text("10% → unchanged", font_size=14, color=DIM, font=MONO),
            Text("Predicts original token", font_size=14, color=DIM, font=MONO),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to(gen_box)

        # Discriminator box
        disc_box = Rectangle(width=4.2, height=2.8, color=CYAN, fill_opacity=0.1, stroke_width=2)
        disc_box.next_to(gen_box, RIGHT, buff=0.8).shift(UP * 0.2)
        disc_lbl = Text("Discriminator", font_size=20, color=CYAN, font=MONO, weight=BOLD)
        disc_lbl.next_to(disc_box, UP, buff=0.15)
        disc_items = VGroup(
            Text("12 layers · ~89M params", font_size=14, color=DIM, font=MONO),
            Text("Classifies EVERY token", font_size=14, color=WHITE, font=MONO),
            Text("Original (0) or Replaced (1)", font_size=14, color=DIM, font=MONO),
            Text("Loss: BCE on ALL positions", font_size=14, color=CYAN, font=MONO),
            Text("λ_rtd = 50", font_size=14, color=GOLD, font=MONO),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to(disc_box)

        # Arrow between
        mid_arr = Arrow(gen_box.get_right(), disc_box.get_left(),
                       color=PURPLE, stroke_width=4, buff=0.15)

        self.play(Create(gen_box), Write(gen_lbl), run_time=1.0)
        self.play(FadeIn(gen_items), run_time=1.5)
        self.play(Create(disc_box), Write(disc_lbl), run_time=1.0)
        self.play(GrowArrow(mid_arr), run_time=0.6)
        self.play(FadeIn(disc_items), run_time=1.5)
        self.wait(5.0)  # "generator corrupts... discriminator detects EVERY token"

        # Example
        ex_row = Text(
            "[CLS]=1  C₁→[MASK]→17✓  C₂=23  O=89  →  Disc labels: [0, 0, 0, 0]",
            font_size=14, color=WHITE, font=MONO
        )
        ex_row.next_to(VGroup(gen_box, disc_box), DOWN, buff=0.8)
        self.play(Write(ex_row), run_time=1.5)
        self.wait(4.0)  # "sometimes gets it right... 50x weight..."

        # ═════════════════════════════════════════════════════
        # SECTION 7: Full Pipeline + Results (3:50 - 5:09)
        # ═════════════════════════════════════════════════════

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)

        pipe_title = Text("End-to-End Pipeline",
                         font_size=28, color=CYAN, weight=BOLD, font=MONO)
        self.play(Write(pipe_title), run_time=1.0)
        pipe_title.to_edge(UP, buff=0.4)
        self.wait(1.0)

        # Pipeline boxes
        stages = [
            ("SMILES\n\"CCO\"", GREEN),
            ("Tokenize\n211 tokens", PURPLE),
            ("Distance\nMatrix", ORANGE),
            ("Embed\n768-dim", GOLD),
            ("Attention\n×12 layers", CYAN),
            ("CLS\n768-dim", GREEN),
            ("Predict\nXGBoost", PURPLE),
        ]

        stage_boxes = VGroup()
        for text, color in stages:
            box = Rectangle(width=1.5, height=1.0, color=color, fill_opacity=0.12, stroke_width=2)
            label = Text(text, font_size=13, color=color, font=MONO, weight=BOLD).move_to(box)
            stage_boxes.add(VGroup(box, label))

        stage_boxes.arrange(RIGHT, buff=0.12)
        stage_boxes.next_to(pipe_title, DOWN, buff=0.8)

        # Arrows
        arrows_vg = VGroup()
        for i in range(len(stage_boxes) - 1):
            a = Arrow(stage_boxes[i].get_right(), stage_boxes[i+1].get_left(),
                     color=DIM, stroke_width=2, buff=0.06, max_tip_length_to_length_ratio=0.25)
            arrows_vg.add(a)

        self.play(Create(stage_boxes), run_time=3.0)
        self.play(*[GrowArrow(a) for a in arrows_vg], run_time=1.5)
        self.wait(6.0)  # "complete pipeline... SMILES enters... tokenization..."

        # Stats
        stat_lines = VGroup(
            Text("89M params · 4×A100 · 29 hrs · 415M molecules · Loss: 0.95",
                 font_size=16, color=DIM, font=MONO),
            Text("BBBP AUROC: 0.878  (+5.07 over random init)",
                 font_size=20, color=GREEN, font=MONO, weight=BOLD),
        ).arrange(DOWN, buff=0.2)
        stat_lines.next_to(stage_boxes, DOWN, buff=1.0)

        self.play(Write(stat_lines[0]), run_time=1.5)
        self.play(Write(stat_lines[1]), run_time=1.5)
        self.wait(6.0)  # "BBBP benchmark... pre-training works"

        # Fade out gracefully
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)

    def _make_atom_box(self, text, color):
        box = Rectangle(width=2.2, height=0.7, color=color, fill_opacity=0.15, stroke_width=2)
        label = Text(text, font_size=16, color=color, font=MONO).move_to(box)
        return VGroup(box, label)
