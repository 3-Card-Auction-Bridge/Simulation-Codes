from manim import *

class ZeroOneMatrix(Scene):
    def construct(self):

        title = Text("0–1 Hand Representation for NT Algorithm", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # Rank labels
        ranks = ["A","K","Q","J","10","9","8","7","6","5","4","3","2"]
        suits = ["♣","♦","♥","♠"]

        # Grid parameters
        rows = 4
        cols = 13
        cell_size = 0.6

        # Create grid
        grid = VGroup()
        for i in range(rows):
            for j in range(cols):
                cell = Square(
                    side_length=cell_size,
                    stroke_width=1
                )
                cell.move_to(
                    RIGHT * j * cell_size
                    + DOWN * i * cell_size
                )
                grid.add(cell)

        grid.move_to(ORIGIN + DOWN*0.5)
        self.play(Create(grid))

        # Rank labels (top)
        rank_labels = VGroup()
        for j, r in enumerate(ranks):
            t = Text(r, font_size=20)
            t.next_to(grid[j], UP, buff=0.15)
            rank_labels.add(t)

        self.play(Write(rank_labels))

        # Suit labels (left)
        suit_labels = VGroup()
        for i, s in enumerate(suits):
            t = Text(s, font_size=28)
            t.next_to(grid[i*cols], LEFT, buff=0.25)
            suit_labels.add(t)

        self.play(Write(suit_labels))

        # Example hand (same as your slides)
        # Clubs: A Q 9
        # Diamonds: K 10 6
        # Hearts: A J 8 5
        # Spades: Q 8 4

        ones = {
            0: [0,2,5],        # Clubs
            1: [1,4,8],        # Diamonds
            2: [0,3,6,9],      # Hearts
            3: [2,6,10],       # Spades
        }

        # Animate filling rows
        for i in range(rows):
            first_one = min(ones[i])

            # Animate leading zeros
            for j in range(first_one):
                zero = Text("0", font_size=22)
                zero.move_to(grid[i*cols + j])
                self.play(FadeIn(zero), run_time=0.2)

            # Animate ones
            for j in ones[i]:
                one = Text("1", font_size=22, color=GREEN)
                one.move_to(grid[i*cols + j])
                self.play(FadeIn(one), run_time=0.25)

            self.wait(0.3)

        # Highlight zeros_before_first_1
        brace = Brace(
            VGroup(*grid[0:first_one]),
            UP,
            color=YELLOW
        )
        label = Text("zeros_before_first_1", font_size=22)
        label.next_to(brace, UP)

        self.play(Create(brace), Write(label))
        self.wait(2)
