from manimlib import *

class QuadrantDiagram(Scene):
    def construct(self):
        # Create the circle (with no stroke)
        circle = Circle(radius=3, stroke_width=0)
        
        # Create the quadrant lines (with no stroke)
        vertical_line = Line(3*UP, 3*DOWN, stroke_width=0)
        horizontal_line = Line(3*LEFT, 3*RIGHT, stroke_width=0)
        
        # Create labels with same positions (uppercase)
        labels = {
            "VOICE": UP + RIGHT,
            "LOYALTY": DOWN + RIGHT,
            "NEGLECT": DOWN + LEFT,
            "EXIT": UP + LEFT
        }
        
        # Create axis labels (uppercase)
        active = Text("ACTIVE", font_size=40, weight=BOLD).next_to(circle, UP, buff=0.5)
        passive = Text("PASSIVE", font_size=40, weight=BOLD).next_to(circle, DOWN, buff=0.5)
        constructive = Text("CONSTRUCTIVE", font_size=40, weight=BOLD).rotate(-90*DEGREES).next_to(circle, RIGHT, buff=0.5)
        destructive = Text("DESTRUCTIVE", font_size=40, weight=BOLD).rotate(90*DEGREES).next_to(circle, LEFT, buff=0.5)
        
        # Create quadrant text labels (bold)
        quadrant_labels = VGroup(*[
            Text(text, font_size=40, weight=BOLD).move_to(pos * 1.5)
            for text, pos in labels.items()
        ])
        
        # Create colored sections with gradients
        angles = [0, PI/2, PI, 3*PI/2]
        colors = [
            (["#FFA500", "#FFD700"]),  # Orange to Gold
            (["#FF0000", "#FF6B6B"]),  # Red to Light Red
            (["#00FF00", "#90EE90"]),  # Green to Light Green
            (["#800080", "#DA70D6"])   # Purple to Orchid
        ]
        
        sectors = VGroup()
        for angle, color_pair in zip(angles, colors):
            sector = Sector(
                radius=3,
                angle=PI/2,
                start_angle=angle,
                fill_opacity=1,
                stroke_width=0
            )
            # Apply gradient
            sector.set_fill(
                color=color_pair,
                opacity=[1, 0.8]  # Gradient opacity from center to edge
            )
            sectors.add(sector)
        
        # Animation sequence
        self.play(ShowCreation(circle))
        self.play(
            ShowCreation(vertical_line),
            ShowCreation(horizontal_line)
        )
        self.play(FadeIn(sectors))
        self.play(
            Write(quadrant_labels),
            Write(active),
            Write(passive),
            Write(constructive),
            Write(destructive)
        )
        self.wait(2)
