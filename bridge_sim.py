from manim import *
import random

# ----------------------------
# Helper functions
# ----------------------------

SUITS = ["♣", "♦", "♥", "♠"]
RANKS = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]

def generate_deck():
    return [f"{r}{s}" for s in SUITS for r in RANKS]

def deal(deck):
    random.shuffle(deck)
    return deck[:13], deck[13:26], deck[26:39], deck[39:]

# ----------------------------
# Main Scene
# ----------------------------

class BridgeGame(Scene):
    def construct(self):

        title = Text("3-Player Auction Bridge Simulation").to_edge(UP)
        self.play(Write(title))

        # Players
        players = [
            Text("Player A").shift(LEFT*4 + UP*2),
            Text("Player B").shift(UP*2),
            Text("Player C").shift(RIGHT*4 + UP*2),
            Text("4th Hand").shift(DOWN*2),
        ]
        self.play(*[FadeIn(p) for p in players])

        # Deal cards
        deck = generate_deck()
        hands = deal(deck)

        hand_groups = []
        for i, hand in enumerate(hands):
            cards = VGroup(*[
                Text(card, font_size=24)
                for card in hand
            ]).arrange_in_grid(rows=3, cols=5, buff=0.15).scale(0.6)
            cards.next_to(players[i], DOWN)
            hand_groups.append(cards)
            self.play(FadeIn(cards), run_time=0.8)

        self.wait(1)

        # ----------------------------
        # BIDDING PHASE
        # ----------------------------

        bidding_title = Text("Bidding Phase").to_edge(LEFT)
        self.play(Transform(title, bidding_title))

        bids = [
            ("Player A", "1♣"),
            ("Player B", "1♥"),
            ("Player C", "2♥"),
            ("Player A", "Pass"),
            ("Player B", "Pass"),
        ]

        bid_texts = VGroup()
        y = 1
        for bidder, bid in bids:
            txt = Text(f"{bidder}: {bid}", font_size=28)
            txt.shift(DOWN*y)
            bid_texts.add(txt)
            y += 0.6

        self.play(LaggedStart(*[Write(b) for b in bid_texts], lag_ratio=0.4))
        self.wait(1)

        # Winning bidder
        winner_box = SurroundingRectangle(players[2], color=YELLOW)
        self.play(Create(winner_box))
        winner_label = Text("Winning Bidder", font_size=24).next_to(players[2], UP)
        self.play(Write(winner_label))

        # Dynamic partner assignment
        arrow = Arrow(players[2].get_bottom(), players[3].get_top())
        self.play(GrowArrow(arrow))

        team_text = Text(
            "Team: Player C + 4th Hand",
            font_size=30,
            color=GREEN
        ).to_edge(DOWN)
        self.play(Write(team_text))
        self.wait(2)

        # ----------------------------
        # PLAY PHASE (Schematic)
        # ----------------------------

        play_title = Text("Gameplay Phase (Trick Flow)").to_edge(LEFT)
        self.play(Transform(bidding_title, play_title))

        trick = VGroup(
            Text("A♠"),
            Text("K♠"),
            Text("3♠"),
            Text("Q♠"),
        ).arrange(RIGHT, buff=0.8).shift(DOWN*1)

        self.play(FadeIn(trick))
        self.wait(1)

        win_arrow = Arrow(trick[3].get_top(), players[2].get_bottom(), color=GREEN)
        self.play(GrowArrow(win_arrow))

        trick_text = Text("Trick won by Player C", font_size=28)
        trick_text.next_to(trick, DOWN)
        self.play(Write(trick_text))

        self.wait(2)

        # End
        end = Text("End of One Deal", font_size=36).to_edge(DOWN)
        self.play(Write(end))
        self.wait(2)
