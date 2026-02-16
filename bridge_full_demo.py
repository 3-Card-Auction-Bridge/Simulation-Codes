from manim import *

# ----------------------------
# Shared hand (13 cards)
# ----------------------------

HAND = {
    "♣": ["A", "Q", "9"],
    "♦": ["K", "10", "6"],
    "♥": ["A", "J", "8", "5"],
    "♠": ["Q", "8", "4"],
}

RANKS = ["A","K","Q","J","10","9","8","7","6","5","4","3","2"]
SUITS = ["♣","♦","♥","♠"]


# ==================================================
# Scene 1: Show a priori 13-card hand
# ==================================================

class ShowHand(Scene):
    def construct(self):
        title = Text("Demo Hand (13 Cards)", font_size=36).to_edge(UP)
        self.play(Write(title))

        y_positions = [2, 0.8, -0.4, -1.6]
        hand_group = VGroup()

        for suit, y in zip(SUITS, y_positions):
            suit_label = Text(suit, font_size=36).move_to(LEFT*5 + UP*y)
            cards = VGroup(*[
                Text(f"{r}{suit}", font_size=26)
                for r in HAND[suit]
            ]).arrange(RIGHT, buff=0.4)
            cards.next_to(suit_label, RIGHT, buff=0.6)

            row = VGroup(suit_label, cards)
            hand_group.add(row)

        self.play(LaggedStart(*[FadeIn(r) for r in hand_group], lag_ratio=0.3))
        self.wait(2)


# ==================================================
# Scene 2: Hand -> 0–1 Matrix
# ==================================================

class HandToMatrix(Scene):
    def construct(self):
        title = Text("Hand → 0–1 Matrix Representation", font_size=36).to_edge(UP)
        self.play(Write(title))

        # Left: textual hand
        hand_text = VGroup(
            *[
                Text(f"{suit}: " + ", ".join(HAND[suit]), font_size=24)
                for suit in SUITS
            ]
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT).shift(DOWN*0.5)

        self.play(FadeIn(hand_text))

        # Matrix grid (right)
        rows, cols = 4, 13
        cell_size = 0.5

        grid = VGroup()
        for i in range(rows):
            for j in range(cols):
                cell = Square(cell_size)
                cell.move_to(
                    RIGHT * j * cell_size
                    + DOWN * i * cell_size
                )
                grid.add(cell)

        grid.move_to(RIGHT*3 + DOWN*0.5)
        self.play(Create(grid))

        # Rank labels
        for j, r in enumerate(RANKS):
            label = Text(r, font_size=18)
            label.next_to(grid[j], UP, buff=0.15)
            self.play(FadeIn(label), run_time=0.05)

        # Suit labels
        for i, s in enumerate(SUITS):
            label = Text(s, font_size=26)
            label.next_to(grid[i*cols], LEFT, buff=0.25)
            self.play(FadeIn(label), run_time=0.05)

        # Fill matrix
        for i, suit in enumerate(SUITS):
            present = HAND[suit]
            indices = [RANKS.index(r) for r in present]
            first = min(indices)

            # Zeros before first 1
            for j in range(first):
                zero = Text("0", font_size=18)
                zero.move_to(grid[i*cols + j])
                self.play(FadeIn(zero), run_time=0.15)

            # Ones
            for j in indices:
                one = Text("1", font_size=18, color=GREEN)
                one.move_to(grid[i*cols + j])
                self.play(FadeIn(one), run_time=0.2)

        self.wait(2)


# ==================================================
# Scene 3: Bidding + Gameplay (Winning Bidder)
# ==================================================

class Gameplay(Scene):
    def construct(self):
        title = Text("Gameplay: Bidder’s Team Wins", font_size=36).to_edge(UP)
        self.play(Write(title))

        # Players
        players = [
            Text("Player A").shift(LEFT*4 + UP*1.5),
            Text("Player B").shift(UP*1.5),
            Text("Player C (Bidder)").shift(RIGHT*4 + UP*1.5),
            Text("4th Hand").shift(DOWN*2),
        ]
        self.play(*[FadeIn(p) for p in players])

        # Bidding
        bids = VGroup(
            Text("A: 1♣"),
            Text("B: 1♥"),
            Text("C: 2♥ (Winning Bid)", color=GREEN),
            Text("A: Pass"),
            Text("B: Pass"),
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT).shift(DOWN*0.5)

        self.play(LaggedStart(*[Write(b) for b in bids], lag_ratio=0.4))
        self.wait(1)

        # Dynamic team
        arrow = Arrow(players[2].get_bottom(), players[3].get_top())
        self.play(GrowArrow(arrow))

        team = Text(
            "Team: Player C + 4th Hand",
            font_size=28,
            color=GREEN
        ).to_edge(DOWN)
        self.play(Write(team))
        self.wait(1)

        # Tricks (schematic)
        trick_title = Text("Winning Tricks", font_size=28).next_to(team, UP)
        self.play(Write(trick_title))

        tricks = VGroup(
            Text("♥A  → Win"),
            Text("♥K  → Win"),
            Text("♥Q  → Win"),
            Text("♠Q  → Win"),
        ).arrange(DOWN).next_to(trick_title, UP)

        self.play(LaggedStart(*[FadeIn(t) for t in tricks], lag_ratio=0.3))
        self.wait(2)

        conclusion = Text(
            "Bidder’s Team Secures the Contract",
            font_size=32,
            color=YELLOW
        ).to_edge(DOWN)
        self.play(Write(conclusion))
        self.wait(2)
