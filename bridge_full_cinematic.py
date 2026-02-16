from manim import *

# ==================================================
# PARAMETERS
# ==================================================

SLOW = 0.6
K = 6
P = 7

RANKS = ["A","K","Q","J","10","9","8","7","6","5","4","3","2"]
SUITS = ["♣","♦","♥","♠"]

HAND = {
    "♣": ["A", "K", "Q"],
    "♦": ["A", "K", "6"],
    "♥": ["A", "J", "8", "5"],
    "♠": ["K", "8", "4"],
}

# ==================================================
# MATRIX BUILDER
# ==================================================

def build_matrix():
    rows, cols = 4, 13
    cell = 0.32
    grid = VGroup()

    for i in range(rows):
        for j in range(cols):
            sq = Square(cell)
            sq.move_to(RIGHT*j*cell + DOWN*i*cell)
            grid.add(sq)

    grid.move_to(RIGHT*3)

    col_labels = VGroup(*[
        Text(r, font_size=12).next_to(grid[j], UP, buff=0.05)
        for j, r in enumerate(RANKS)
    ])

    row_labels = VGroup(*[
        Text(s, font_size=18).next_to(grid[i*cols], LEFT, buff=0.1)
        for i, s in enumerate(SUITS)
    ])

    ones = VGroup()
    ones_positions = {}

    for i, suit in enumerate(SUITS):
        indices_of_ones = [RANKS.index(r) for r in HAND[suit]]
        ones_positions[suit] = indices_of_ones
        for j in indices_of_ones:
            one = Text("1", font_size=14, color=GREEN)
            one.move_to(grid[i*cols + j])
            ones.add(one)

    return VGroup(grid, col_labels, row_labels, ones), ones_positions

# ==================================================
# MAIN SCENE WITH TRUE SLIDES
# ==================================================

class NTAlgorithmTrueSlides(Scene):

    def show_slide(self, *mobjects, wait=1.5):
        group = VGroup(*mobjects)
        self.play(FadeIn(group), run_time=1.2*SLOW)
        self.wait(wait*SLOW)
        self.play(FadeOut(group), run_time=1.0*SLOW)

    def construct(self):

        # --------------------------------------------------
        # SLIDE 0: TITLE
        # --------------------------------------------------
        title = Text("No Trump Calling Algorithm", font_size=40)
        self.show_slide(title, wait=2)

        # --------------------------------------------------
        # SLIDE 1: INPUT HAND
        # --------------------------------------------------
        step = Text("Step 1: Input Hand", font_size=30)
        hand = VGroup(
            Text("♣  A K Q", font_size=24),
            Text("♦  A K 6", font_size=24),
            Text("♥  A J 8 5", font_size=24),
            Text("♠  K 8 4", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        slide1 = VGroup(step, hand).arrange(DOWN, buff=0.8)
        self.show_slide(slide1, wait=2)

        # --------------------------------------------------
        # SLIDE 2: MATRIX CONSTRUCTION
        # --------------------------------------------------
        step = Text("Step 2: Binary Matrix Representation", font_size=30)
        matrix, ones_positions = build_matrix()
        slide2 = VGroup(step, matrix).arrange(DOWN, buff=0.6)
        self.show_slide(slide2, wait=2)

        # --------------------------------------------------
        # SLIDE 3: ROW STATISTICS
        # --------------------------------------------------
        step = Text(
            "Step 3: count_ones and zeros_before_first_one",
            font_size=30
        )

        row_lines = VGroup()
        row_stats = {}

        for suit in SUITS:
            indices_of_ones = ones_positions[suit]
            count_ones = len(indices_of_ones)
            zeros_before_first_one = indices_of_ones[0]
            row_stats[suit] = (count_ones, zeros_before_first_one)

            row_lines.add(
                Text(
                    f"{suit}: count_ones={count_ones}, "
                    f"zeros_before_first_one={zeros_before_first_one}",
                    font_size=22
                )
            )

        row_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        slide3 = VGroup(step, row_lines, matrix).arrange(DOWN, buff=0.6)
        self.show_slide(slide3, wait=2)
        # --------------------------------------------------
        # STEP 4: GAP FILLING — FULL DETAIL
        # --------------------------------------------------

        # --- Slide 4.0: Step title ---
        step = Text("Step 4: Gap Filling Loop (Detailed)", font_size=30)
        self.show_slide(step, wait=1.5)

        # Compute total zeros before first 1 across all suits (Z)
        Z = sum(stats[1] for stats in row_stats.values())
        # Initialize count_of_one from actual row counts
        count_of_one = 4
        remaining_zeros = K - Z

        # --- Slide 4.1: Initialization ---
        init_text = VGroup(
            Text("Initialization:", font_size=26),
            Text(f"count_of_one = {count_of_one}", font_size=22),
            Text(f"remaining_zeros = K - total_zeros_before_first_1 = {remaining_zeros}",
                 font_size=22)
        ).arrange(DOWN, buff=0.4)

        self.show_slide(init_text, wait=2)

        # --- Slide 4.2 onward: Suit-by-suit processing ---
        for suit in SUITS:

            indices_of_ones = ones_positions[suit]

            suit_header = Text(
                f"Processing suit {suit}",
                font_size=28
            )

            suit_info = Text(
                f"indices_of_ones = {indices_of_ones}",
                font_size=22
            )

            self.show_slide(
                VGroup(suit_header, suit_info).arrange(DOWN, buff=0.5),
                wait=2
            )

            # Inner loop over indices
            for i in range(len(indices_of_ones) - 1):

                zeros_between = (
                    indices_of_ones[i+1]
                    - indices_of_ones[i]
                    - 1
                )

                comparison = Text(
                    f"zeros_between = {indices_of_ones[i+1]} - {indices_of_ones[i]} - 1 = {zeros_between}",
                    font_size=22
                )

                check = Text(
                    f"Check: zeros_between ≤ remaining_zeros ({zeros_between} ≤ {remaining_zeros})",
                    font_size=22
                )

                slide = VGroup(comparison, check).arrange(DOWN, buff=0.4)
                self.show_slide(slide, wait=1.5)

                # Decision branch
                if zeros_between <= remaining_zeros:
                    remaining_zeros -= zeros_between
                    count_of_one += 1

                    update = VGroup(
                        Text("Condition satisfied → update variables", font_size=22, color=GREEN),
                        Text(f"count_of_one = {count_of_one}", font_size=22),
                        Text(f"remaining_zeros = {remaining_zeros}", font_size=22),
                    ).arrange(DOWN, buff=0.3)

                    self.show_slide(update, wait=1.8)

                else:
                    reject = Text(
                        "Condition failed → no update",
                        font_size=22,
                        color=RED
                    )
                    self.show_slide(reject, wait=1.5)

        # --- Slide 4.final: End of loop summary ---
        summary = VGroup(
            Text("End of gap filling loop", font_size=26),
            Text(f"Final count_of_one = {count_of_one}", font_size=24),
            Text(f"Final remaining_zeros = {remaining_zeros}", font_size=24),
        ).arrange(DOWN, buff=0.4)

        # --------------------------------------------------
        # FINAL DECISION SLIDE (Algorithm Output)
        # --------------------------------------------------

        decision_title = Text(
            "Final Decision (Algorithm Output)",
            font_size=30
        )

        decision_logic = VGroup(
            Text(
                f"Final count_of_one = {count_of_one}",
                font_size=24
            ),
            Text(
                f"Threshold P = {P}",
                font_size=24
            ),
            Text(
                f"Check: count_of_one ≥ P  ({count_of_one} ≥ {P})",
                font_size=24
            ),
        ).arrange(DOWN, buff=0.4)

        decision_result = Text(
            "Result: YES — final condition satisfied.\nProceed with the bid.",
            font_size=26,
            color=GREEN
        )

        final_slide = VGroup(
            decision_title,
            decision_logic,
            decision_result
        ).arrange(DOWN, buff=0.6)

        self.show_slide(final_slide, wait=3)
