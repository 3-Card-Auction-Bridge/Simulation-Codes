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

    grid.move_to(RIGHT*3.2)

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

class NTAlgorithmFinal(Scene):

    # -------------------------------
    # SLIDE HELPERS
    # -------------------------------
    def show_step_slide(self, matrix, step_text, wait=1.2):
        self.play(FadeOut(matrix), run_time=0.6*SLOW)
        self.play(FadeIn(step_text), run_time=0.8*SLOW)
        self.wait(wait*SLOW)
        self.play(FadeOut(step_text), run_time=0.8*SLOW)

    def show_content_slide(self, matrix, *mobjects, wait=1.6):
        self.play(FadeIn(matrix), run_time=0.6*SLOW)
        self.play(FadeIn(VGroup(*mobjects)), run_time=1.0*SLOW)
        self.wait(wait*SLOW)
        self.play(FadeOut(VGroup(*mobjects)), run_time=0.8*SLOW)

    # -------------------------------
    # CONSTRUCT
    # -------------------------------
    def construct(self):

        left_anchor = LEFT*4.5

        # -------------------------------
        # TITLE
        # -------------------------------
        title = Text("No Trump Calling Algorithm", font_size=38)
        self.show_step_slide(VGroup(), title, wait=2)

        # -------------------------------
        # STEP 1: INPUT HAND
        # -------------------------------
        step1 = Text("Step 1: Input Hand", font_size=30)
        self.show_step_slide(VGroup(), step1)

        hand_text = VGroup(
            Text("♣  A K Q", font_size=22),
            Text("♦  A K 6", font_size=22),
            Text("♥  A J 8 5", font_size=22),
            Text("♠  K 8 4", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(left_anchor)

        matrix, ones_positions = build_matrix()
        self.show_content_slide(matrix, hand_text, wait=2)

        # -------------------------------
        # STEP 2: ROW STATISTICS
        # -------------------------------
        step2 = Text(
            "Step 2: count_ones and zeros_before_first_one",
            font_size=30
        )
        self.show_step_slide(matrix, step2)

        row_stats = {}
        row_text = VGroup()

        for suit in SUITS:
            indices_of_ones = ones_positions[suit]
            count_ones = len(indices_of_ones)
            zeros_before_first_one = indices_of_ones[0]

            row_stats[suit] = (count_ones, zeros_before_first_one)

            row_text.add(
                Text(
                    f"{suit}: count_ones = {count_ones}, "
                    f"zeros_before_first_one = {zeros_before_first_one}",
                    font_size=20
                )
            )

        row_text.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(left_anchor)
        self.show_content_slide(matrix, row_text, wait=2)

        # -------------------------------
        # STEP 3: CONDITIONS A & B
        # -------------------------------
        step3 = Text("Step 3: Conditions A and B", font_size=30)
        self.show_step_slide(matrix, step3)

        total_zeros_before_first_1 = sum(
            z for _, z in row_stats.values()
        )

        cond_text = VGroup(
            Text(
                f"total_zeros_before_first_1 = {total_zeros_before_first_1}",
                font_size=22
            ),
            Text(
                f"Condition A: {total_zeros_before_first_1} ≤ {K} → PASSED",
                font_size=22,
                color=GREEN
            ),
            Text(
                "Condition B: count_ones > zeros_before_first_one (all suits) → PASSED",
                font_size=22,
                color=GREEN
            )
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(left_anchor)

        self.show_content_slide(matrix, cond_text, wait=2)

        # -------------------------------
        # STEP 4: ITERATION OVER INDICES
        # -------------------------------
        step4 = Text("Step 4: Iteration over indices_of_ones", font_size=30)
        self.show_step_slide(matrix, step4)

        count_of_one = 4
        remaining_zeros = K - total_zeros_before_first_1

        init_text = VGroup(
            Text("Initialization:", font_size=22),
            Text(f"count_of_one = 4", font_size=20),
            Text(f"remaining_zeros = {remaining_zeros}", font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(left_anchor)

        self.show_content_slide(matrix, init_text, wait=2)

        for suit in SUITS:
            indices_of_ones = ones_positions[suit]

            suit_text = VGroup(
                Text(f"Suit {suit}", font_size=22),
                Text(f"indices_of_ones = {indices_of_ones}", font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(left_anchor)

            self.show_content_slide(matrix, suit_text, wait=1.8)

            for i in range(len(indices_of_ones) - 1):
                zeros_between = (
                    indices_of_ones[i+1]
                    - indices_of_ones[i]
                    - 1
                )

                comparison = VGroup(
                    Text(
                        f"zeros_between = {indices_of_ones[i+1]} − "
                        f"{indices_of_ones[i]} − 1 = {zeros_between}",
                        font_size=18
                    ),
                    Text(
                        f"Check: {zeros_between} ≤ remaining_zeros ({remaining_zeros})",
                        font_size=18
                    )
                ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(left_anchor)

                self.show_content_slide(matrix, comparison, wait=1.5)

                if zeros_between <= remaining_zeros:
                    remaining_zeros -= zeros_between
                    count_of_one += 1

                    update = VGroup(
                        Text("Condition satisfied → update", font_size=18, color=GREEN),
                        Text(f"count_of_one = {count_of_one}", font_size=18),
                        Text(f"remaining_zeros = {remaining_zeros}", font_size=18),
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(left_anchor)

                    self.show_content_slide(matrix, update, wait=1.6)
                else:
                    reject = Text(
                        "Condition failed → no update",
                        font_size=18,
                        color=RED
                    ).move_to(left_anchor)

                    self.show_content_slide(matrix, reject, wait=1.4)

        # -------------------------------
        # FINAL DECISION
        # -------------------------------
        final_step = Text("Final Decision (Algorithm Output)", font_size=30)
        self.show_step_slide(matrix, final_step)

        final_decision = VGroup(
            Text(f"Final count_of_one = {count_of_one}", font_size=24),
            Text(f"P = {P}", font_size=24),
            Text(f"Check: {count_of_one} ≥ {P}", font_size=24),
            Text(
                "YES — final condition satisfied.\nProceed with the bid.",
                font_size=26,
                color=GREEN
            )
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(left_anchor)

        self.show_content_slide(matrix, final_decision, wait=3)
