"""
MolE-RTD: Full Pipeline Animation
4 scenes walking through the entire MolE-RTD architecture.
Uses ethanol (CCO) as the running example throughout.
"""
from manim import *

# ── Shared constants ──────────────────────────────────────────
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

TITLE_SIZE = 38
HEAD_SIZE = 28
BODY_SIZE = 22
LABEL_SIZE = 18
CAPTION_SIZE = 14


# ═══════════════════════════════════════════════════════════════
# SCENE 1: SMILES → Molecule
# ═══════════════════════════════════════════════════════════════
class Scene1_SMILES_to_Molecule(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ── Title ──
        title = Text("MolE-RTD: From SMILES to Molecule", font_size=TITLE_SIZE,
                     color=CYAN, weight=BOLD, font=MONO)
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)
        self.play(title.animate.to_edge(UP, buff=0.4).scale(0.55), run_time=1.0)

        # ── SMILES string ──
        smiles_label = Text("SMILES:", font_size=LABEL_SIZE, color=DIM, font=MONO)
        smiles_label.next_to(title, DOWN, buff=0.8).to_edge(LEFT, buff=1.5)
        smiles_text = Text('"CCO"', font_size=HEAD_SIZE, color=WHITE, font=MONO)
        smiles_text.next_to(smiles_label, RIGHT, buff=0.3)

        self.play(FadeIn(smiles_label), Write(smiles_text), run_time=1.0)
        self.wait(0.8)

        # ── Arrow ──
        arrow = Arrow(LEFT, RIGHT, color=PURPLE, stroke_width=3)
        arrow.next_to(smiles_text, RIGHT, buff=0.6)
        self.play(GrowArrow(arrow), run_time=0.6)

        # ── Molecule diagram ──
        c1 = Circle(radius=0.35, color=GREEN, fill_opacity=0.3, stroke_width=3)
        c1_label = Text("C₁", font_size=LABEL_SIZE, color=GREEN, font=MONO)
        c1_label.move_to(c1)
        c1_group = VGroup(c1, c1_label)

        c2 = Circle(radius=0.35, color=GREEN, fill_opacity=0.3, stroke_width=3)
        c2_label = Text("C₂", font_size=LABEL_SIZE, color=GREEN, font=MONO)
        c2_label.move_to(c2)
        c2_group = VGroup(c2, c2_label)

        o1 = Circle(radius=0.35, color=RED, fill_opacity=0.25, stroke_width=3)
        o1_label = Text("O", font_size=LABEL_SIZE, color=RED, font=MONO)
        o1_label.move_to(o1)
        o_group = VGroup(o1, o1_label)

        # Position atoms
        c1_group.move_to(arrow.get_right() + RIGHT * 1.2 + UP * 0.8)
        c2_group.move_to(c1_group.get_right() + RIGHT * 1.2)
        o_group.move_to(c2_group.get_right() + RIGHT * 1.2)

        # Bonds
        b1 = Line(c1.get_right(), c2.get_left(), color=WHITE, stroke_width=2)
        b2 = Line(c2.get_right(), o1.get_left(), color=WHITE, stroke_width=2)
        bond_label1 = Text("—", font_size=24, color=DIM, font=MONO)
        bond_label1.move_to((c1.get_center() + c2.get_center()) / 2)
        bond_label2 = Text("—", font_size=24, color=DIM, font=MONO)
        bond_label2.move_to((c2.get_center() + o1.get_center()) / 2)

        self.play(
            Create(c1), Write(c1_label),
            Create(c2), Write(c2_label),
            Create(o1), Write(o1_label),
            Create(b1), Create(b2),
            Write(bond_label1), Write(bond_label2),
            run_time=2.0
        )
        self.wait(1.0)

        # ── Stats ──
        stats = Text("3 heavy atoms · 2 bonds · sp³ hybridized",
                     font_size=CAPTION_SIZE, color=DIM, font=MONO)
        stats.next_to(VGroup(c1_group, o_group), DOWN, buff=0.8)
        self.play(Write(stats), run_time=1.0)
        self.wait(1.5)

        # ── RDKit info ──
        rdkit_note = Text("RDKit: Chem.MolFromSmiles(\"CCO\")",
                          font_size=CAPTION_SIZE, color=DIM, font=MONO)
        rdkit_note.next_to(stats, DOWN, buff=0.3)
        self.play(Write(rdkit_note), run_time=1.0)
        self.wait(2.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


# ═══════════════════════════════════════════════════════════════
# SCENE 2: Tokenization + Distance Matrix
# ═══════════════════════════════════════════════════════════════
class Scene2_Tokenization(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Tokenization: Morgan Fingerprint (Radius 0)",
                     font_size=TITLE_SIZE, color=CYAN, weight=BOLD, font=MONO)
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)
        self.play(title.animate.to_edge(UP, buff=0.4).scale(0.5), run_time=1.0)

        # ── Atom row ──
        atoms_header = Text("Atoms in ethanol:", font_size=LABEL_SIZE, color=DIM, font=MONO)
        atoms_header.to_edge(LEFT, buff=1.0).shift(UP * 1.2)

        c1_box = Rectangle(width=1.4, height=0.7, color=GREEN, fill_opacity=0.15, stroke_width=2)
        c1_t = Text("C₁ (sp³)", font_size=BODY_SIZE, color=GREEN, font=MONO).move_to(c1_box)
        c1_vg = VGroup(c1_box, c1_t)

        c2_box = Rectangle(width=1.8, height=0.7, color=GREEN, fill_opacity=0.15, stroke_width=2)
        c2_t = Text("C₂ (sp³)", font_size=BODY_SIZE, color=GREEN, font=MONO).move_to(c2_box)
        c2_vg = VGroup(c2_box, c2_t)

        o_box = Rectangle(width=1.6, height=0.7, color=RED, fill_opacity=0.15, stroke_width=2)
        o_t = Text("O (OH)", font_size=BODY_SIZE, color=RED, font=MONO).move_to(o_box)
        o_vg = VGroup(o_box, o_t)

        atoms = VGroup(c1_vg, c2_vg, o_vg).arrange(RIGHT, buff=0.4)
        atoms.next_to(atoms_header, DOWN, buff=0.4).to_edge(LEFT, buff=0.5)

        self.play(FadeIn(atoms_header), run_time=0.5)
        for a in [c1_vg, c2_vg, o_vg]:
            self.play(Create(a), run_time=0.6)

        self.wait(0.8)

        # ── Arrow down to token IDs ──
        arrows_down = VGroup(*[
            Arrow(atom.get_bottom(), atom.get_bottom() + DOWN * 0.6,
                  color=PURPLE, stroke_width=2, max_tip_length_to_length_ratio=0.15)
            for atom in [c1_vg, c2_vg, o_vg]
        ])

        self.play(*[GrowArrow(a) for a in arrows_down], run_time=1.0)

        # ── Token IDs ──
        tok_boxes = VGroup()
        tok_labels = VGroup()
        tokens_data = [
            ("C_sp3_aliph", "17", GREEN),
            ("C_sp3_adjO", "23", GREEN),
            ("O_sp3_hydroxyl", "89", RED),
        ]
        for i, (name, tid, col) in enumerate(tokens_data):
            box = Rectangle(width=2.0, height=0.7, color=col, fill_opacity=0.15, stroke_width=2)
            box.move_to(arrows_down[i].get_bottom() + DOWN * 0.15)
            tok_boxes.add(box)
            label = Text(f"{name} → {tid}", font_size=CAPTION_SIZE, color=col, font=MONO)
            label.move_to(box)
            tok_labels.add(label)

        for box, label in zip(tok_boxes, tok_labels):
            self.play(Create(box), Write(label), run_time=0.7)

        self.wait(1.0)

        # ── CLS insert ──
        cls_note = Text("Prepend [CLS] at position 0", font_size=LABEL_SIZE, color=GOLD, font=MONO)
        cls_note.next_to(tok_boxes, DOWN, buff=1.0)

        final_seq = Text("[CLS=1]  [C₁=17]  [C₂=23]  [O=89]",
                         font_size=BODY_SIZE, color=WHITE, font=MONO)
        final_seq.next_to(cls_note, DOWN, buff=0.3)

        self.play(Write(cls_note), run_time=0.8)
        self.play(Write(final_seq), run_time=1.2)
        self.wait(1.0)

        # ── Distance matrix section ──
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)

        # New title for distance matrix
        dm_title = Text("Distance Matrix → Relative Positions",
                        font_size=HEAD_SIZE, color=GOLD, weight=BOLD, font=MONO)
        dm_title.to_edge(UP, buff=0.5)
        self.play(Write(dm_title), run_time=1.2)
        self.wait(0.5)

        # Build matrix
        dist_data = [
            ["0", "1", "2"],
            ["1", "0", "1"],
            ["2", "1", "0"],
        ]

        # Build matrix manually (avoids MobjectTable API differences)
        rows = VGroup()
        for i, row in enumerate(dist_data):
            cells = VGroup()
            for j, d in enumerate(row):
                c = CYAN if d == "0" else WHITE
                cell = Rectangle(width=0.9, height=0.6, color=DIM, fill_opacity=0.08, stroke_width=1)
                label = Text(d, font_size=BODY_SIZE, color=c, font=MONO).move_to(cell)
                cells.add(VGroup(cell, label))
            cells.arrange(RIGHT, buff=0.1)
            rows.add(cells)

        rows.arrange(DOWN, buff=0.1)

        # Row labels
        rlabels = VGroup()
        for r in ["C₁", "C₂", "O"]:
            rlabels.add(Text(r, font_size=CAPTION_SIZE, color=DIM, font=MONO))
        rlabels.arrange(DOWN, buff=0.7)
        rlabels.next_to(rows, LEFT, buff=0.3)

        # Col labels
        clabels = VGroup()
        for c in ["C₁", "C₂", "O"]:
            clabels.add(Text(c, font_size=CAPTION_SIZE, color=DIM, font=MONO))
        clabels.arrange(RIGHT, buff=0.95)
        clabels.next_to(rows, UP, buff=0.15)

        matrix_group = VGroup(rlabels, clabels, rows)
        matrix_group.next_to(dm_title, DOWN, buff=0.6)

        self.play(Create(rows), Write(rlabels), Write(clabels), run_time=2.0)
        self.wait(1.0)

        # Annotation
        annotation = Text(
            "Bond distance d → row (d + 512) in position embedding table [1024 × 64]",
            font_size=CAPTION_SIZE, color=DIM, font=MONO
        )
        annotation.next_to(matrix_group, DOWN, buff=0.5)
        self.play(Write(annotation), run_time=1.5)
        self.wait(2.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


# ═══════════════════════════════════════════════════════════════
# SCENE 3: Disentangled Attention
# ═══════════════════════════════════════════════════════════════
class Scene3_Attention(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Disentangled Attention (The Heart of DeBERTa)",
                     font_size=TITLE_SIZE, color=CYAN, weight=BOLD, font=MONO)
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)
        self.play(title.animate.to_edge(UP, buff=0.4).scale(0.45), run_time=1.0)

        # ── Standard attention ──
        std = Text("Standard:  softmax(QKᵀ / √d) × V",
                   font_size=BODY_SIZE, color=DIM, font=MONO)
        std.next_to(title, DOWN, buff=0.7)
        self.play(Write(std), run_time=1.0)
        self.wait(0.5)

        # ── Disentangled formula ──
        formula_parts = VGroup(
            Text("Attention = softmax(", font_size=BODY_SIZE, color=CYAN, font=MONO),
            Text("QcKcᵀ", font_size=BODY_SIZE, color=GOLD, font=MONO, weight=BOLD),
            Text(" + ", font_size=BODY_SIZE, color=WHITE, font=MONO),
            Text("QcKrᵀ", font_size=BODY_SIZE, color=ORANGE, font=MONO, weight=BOLD),
            Text(" + ", font_size=BODY_SIZE, color=WHITE, font=MONO),
            Text("QrKcᵀ", font_size=BODY_SIZE, color=GREEN, font=MONO, weight=BOLD),
            Text(") × V", font_size=BODY_SIZE, color=CYAN, font=MONO),
        ).arrange(RIGHT, buff=0.1)
        formula_parts.next_to(std, DOWN, buff=0.7)

        self.play(Write(formula_parts), run_time=2.0)
        self.wait(1.5)

        # ── Legend ──
        legend = VGroup(
            VGroup(
                Dot(color=GOLD, radius=0.08),
                Text("Content↔Content", font_size=CAPTION_SIZE, color=GOLD, font=MONO)
            ).arrange(RIGHT, buff=0.15),
            VGroup(
                Dot(color=ORANGE, radius=0.08),
                Text("Content→Position (c2p)", font_size=CAPTION_SIZE, color=ORANGE, font=MONO)
            ).arrange(RIGHT, buff=0.15),
            VGroup(
                Dot(color=GREEN, radius=0.08),
                Text("Position→Content (p2c)", font_size=CAPTION_SIZE, color=GREEN, font=MONO)
            ).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        legend.next_to(formula_parts, DOWN, buff=0.8).to_edge(LEFT, buff=1.5)

        self.play(FadeIn(legend), run_time=1.2)
        self.wait(1.0)

        # ── Concrete example ──
        self.play(FadeOut(formula_parts), FadeOut(std), FadeOut(legend), run_time=0.6)

        ex_title = Text("Example: Attention from C₂ to all atoms in ethanol",
                        font_size=HEAD_SIZE, color=PURPLE, weight=BOLD, font=MONO)
        ex_title.next_to(title, DOWN, buff=0.6)
        self.play(Write(ex_title), run_time=1.2)
        self.wait(0.5)

        # Attention table
        att_data = [
            ["Target", "Dist", "QcKcᵀ", "QcKrᵀ", "QrKcᵀ", "Total", "Softmax"],
            ["[CLS]", "0", "0.12", "0.05", "0.03", "0.20", "0.18"],
            ["C₁", "1", "0.35", "0.28", "0.15", "0.78", "0.42"],
            ["C₂", "0", "0.40", "0.02", "0.01", "0.43", "0.28"],
            ["O", "1", "0.18", "0.22", "0.12", "0.52", "0.31"],
        ]

        # Color coding
        colors_per_col = [WHITE, WHITE, GOLD, ORANGE, GREEN, WHITE, WHITE]
        highlight_row = 2  # C₁ row (the max attention)

        att_rows = VGroup()
        for i, row in enumerate(att_data):
            row_group = VGroup()
            is_header = (i == 0)
            is_highlight = (i == highlight_row)
            for j, cell in enumerate(row):
                c = colors_per_col[j] if not is_header else CYAN
                if is_highlight and j >= 2 and j <= 6:
                    c = GOLD
                sz = CAPTION_SIZE if is_header else CAPTION_SIZE
                t = Text(cell, font_size=sz, color=c, font=MONO,
                         weight=BOLD if is_header or (is_highlight and j == 5) else NORMAL)
                row_group.add(t)
            row_group.arrange(RIGHT, buff=0.5)
            if is_highlight:
                bg = Rectangle(
                    width=row_group.width + 0.4,
                    height=row_group.height + 0.25,
                    color=GOLD, fill_opacity=0.08, stroke_width=1,
                    stroke_opacity=0.5
                ).move_to(row_group)
                row_group = VGroup(bg, row_group)
            att_rows.add(row_group)

        att_rows.arrange(DOWN, buff=0.2)
        att_rows.next_to(ex_title, DOWN, buff=0.5)

        for row in att_rows:
            self.play(FadeIn(row), run_time=0.5)

        self.wait(1.5)

        # Highlight note
        note = Text("C₂ attends most to its bonded neighbor C₁ (dist=1) — cross terms reinforce bonded pairs!",
                    font_size=CAPTION_SIZE, color=GOLD, font=MONO)
        note.next_to(att_rows, DOWN, buff=0.4)
        self.play(Write(note), run_time=1.5)
        self.wait(2.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)


# ═══════════════════════════════════════════════════════════════
# SCENE 4: RTD Pretraining + Pipeline Summary
# ═══════════════════════════════════════════════════════════════
class Scene4_RTD_and_Pipeline(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("RTD Pretraining: Generator → Discriminator",
                     font_size=TITLE_SIZE, color=CYAN, weight=BOLD, font=MONO)
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)
        self.play(title.animate.to_edge(UP, buff=0.4).scale(0.45), run_time=1.0)

        # ── Generator box ──
        gen_box = Rectangle(width=4.5, height=3.0, color=ORANGE, fill_opacity=0.1, stroke_width=2)
        gen_box.to_edge(LEFT, buff=0.8).shift(UP * 0.2)
        gen_title = Text("Generator (3 layers, ~7M)",
                         font_size=LABEL_SIZE, color=ORANGE, font=MONO, weight=BOLD)
        gen_title.next_to(gen_box, UP, buff=0.2)

        gen_items = VGroup(
            Text("① 15% tokens masked", font_size=CAPTION_SIZE, color=WHITE, font=MONO),
            Text("② 80% → [MASK], 10% random, 10% keep", font_size=CAPTION_SIZE, color=DIM, font=MONO),
            Text("③ Predict original token at masked pos", font_size=CAPTION_SIZE, color=DIM, font=MONO),
            Text("④ Replace masked tokens with best guess", font_size=CAPTION_SIZE, color=DIM, font=MONO),
            Text("Loss: CrossEntropy (masked only)", font_size=CAPTION_SIZE, color=ORANGE, font=MONO),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        gen_items.move_to(gen_box)

        self.play(Create(gen_box), Write(gen_title), run_time=1.0)
        for item in gen_items:
            self.play(Write(item), run_time=0.35)
        self.wait(0.8)

        # ── Arrow ──
        mid_arrow = Arrow(gen_box.get_right(), gen_box.get_right() + RIGHT * 1.5,
                          color=PURPLE, stroke_width=4, max_tip_length_to_length_ratio=0.1)
        mid_label = Text("corrupted\nsequence", font_size=CAPTION_SIZE, color=PURPLE, font=MONO)
        mid_label.next_to(mid_arrow, UP, buff=0.1)
        self.play(GrowArrow(mid_arrow), Write(mid_label), run_time=1.0)

        # ── Discriminator box ──
        disc_box = Rectangle(width=4.5, height=3.0, color=CYAN, fill_opacity=0.1, stroke_width=2)
        disc_box.next_to(mid_arrow, RIGHT, buff=0.5).shift(UP * 0.2)
        disc_title = Text("Discriminator (12 layers, ~89M)",
                          font_size=LABEL_SIZE, color=CYAN, font=MONO, weight=BOLD)
        disc_title.next_to(disc_box, UP, buff=0.2)

        disc_items = VGroup(
            Text("① Takes corrupted sequence as input", font_size=CAPTION_SIZE, color=WHITE, font=MONO),
            Text("② EVERY token: real(0) or replaced(1)?", font_size=CAPTION_SIZE, color=DIM, font=MONO),
            Text("③ Label=1 only if gen was wrong", font_size=CAPTION_SIZE, color=DIM, font=MONO),
            Text("④ Binary classification per token", font_size=CAPTION_SIZE, color=DIM, font=MONO),
            Text("Loss: BCE × 50 (on ALL tokens!)", font_size=CAPTION_SIZE, color=CYAN, font=MONO),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        disc_items.move_to(disc_box)

        self.play(Create(disc_box), Write(disc_title), run_time=1.0)
        for item in disc_items:
            self.play(Write(item), run_time=0.35)
        self.wait(1.0)

        # ── Example row ──
        ex_label = Text("Example: ethanol (CCO)", font_size=LABEL_SIZE, color=GOLD, font=MONO)
        ex_label.next_to(VGroup(gen_box, disc_box), DOWN, buff=0.8).to_edge(LEFT, buff=1.5)

        ex_tokens = Text(
            "[CLS]=1   C₁=[MASK]   C₂=23   O=89   →   Gen predicts C₁=17 ✓   →   Disc label: 0 (original)",
            font_size=CAPTION_SIZE, color=WHITE, font=MONO
        )
        ex_tokens.next_to(ex_label, DOWN, buff=0.3).to_edge(LEFT, buff=0.5)

        self.play(Write(ex_label), run_time=0.5)
        self.play(Write(ex_tokens), run_time=1.5)
        self.wait(1.5)

        # ── Transition to full pipeline ──
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)

        # ── FULL PIPELINE SUMMARY ──
        pipe_title = Text("MolE-RTD: End-to-End Pipeline",
                          font_size=TITLE_SIZE, color=CYAN, weight=BOLD, font=MONO)
        self.play(Write(pipe_title), run_time=1.2)
        self.wait(0.5)
        self.play(pipe_title.animate.to_edge(UP, buff=0.4).scale(0.5), run_time=1.0)

        # Pipeline boxes
        stages = [
            ("SMILES\n\"CCO\"", GREEN),
            ("Tokenize\nMorgan FP r=0", PURPLE),
            ("Distance\nMatrix", ORANGE),
            ("Embeddings\n211×768", GOLD),
            ("Attention\n×12 layers", CYAN),
            ("CLS Token\n768-dim", GREEN),
            ("Predict\nXGBoost/MLP", PURPLE),
        ]

        stage_boxes = VGroup()
        stage_arrows = VGroup()
        for i, (text, color) in enumerate(stages):
            box = Rectangle(width=1.6, height=1.2, color=color, fill_opacity=0.12, stroke_width=2)
            label = Text(text, font_size=CAPTION_SIZE, color=color, font=MONO, weight=BOLD)
            label.move_to(box)
            stage_boxes.add(VGroup(box, label))

        stage_boxes.arrange(RIGHT, buff=0.15)
        stage_boxes.next_to(pipe_title, DOWN, buff=0.8)

        # Arrows between boxes
        for i in range(len(stage_boxes) - 1):
            arr = Arrow(
                stage_boxes[i].get_right(),
                stage_boxes[i+1].get_left(),
                color=DIM, stroke_width=2, buff=0.07,
                max_tip_length_to_length_ratio=0.2
            )
            stage_arrows.add(arr)

        self.play(Create(stage_boxes), run_time=2.5)
        self.play(*[GrowArrow(a) for a in stage_arrows], run_time=1.0)
        self.wait(1.0)

        # Stats
        stats_line1 = Text("89M params · 4×A100 · 29 hrs · 415M molecules · Loss: 0.95",
                           font_size=CAPTION_SIZE, color=DIM, font=MONO)
        stats_line1.next_to(stage_boxes, DOWN, buff=0.8)

        stats_line2 = Text("BBBP AUROC: 0.878 (+5.07 over random init)",
                           font_size=CAPTION_SIZE, color=GREEN, font=MONO, weight=BOLD)
        stats_line2.next_to(stats_line1, DOWN, buff=0.15)

        self.play(Write(stats_line1), run_time=1.0)
        self.play(Write(stats_line2), run_time=1.0)
        self.wait(2.5)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
