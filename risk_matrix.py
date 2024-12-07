from manimlib import *

class RiskMatrix(Scene):
    def construct(self):
        # Set background color to white
        self.camera.background_color = WHITE

        # Define risk colors
        LOW_RISK = "#00A3A3"  # Teal
        MEDIUM_RISK = "#FFB800"  # Gold
        HIGH_RISK = "#E6007E"  # Magenta

        # Create matrix grid
        matrix = VGroup()
        for i in range(5):  # i is likelihood (bottom to top)
            for j in range(5):  # j is consequences (left to right)
                square = Square(
                    side_length=1,
                    fill_opacity=0.7,
                    stroke_width=2,
                    stroke_color=GREY_E
                )
                
                # Color logic based on position
                if i + j <= 2:  # Bottom left - low risk
                    color = LOW_RISK
                elif i + j >= 6:  # Top right - high risk
                    color = HIGH_RISK
                else:  # Middle - medium risk
                    color = MEDIUM_RISK
                
                square.set_fill(color)
                square.move_to([j-2, 2-i, 0])
                matrix.add(square)

        # Rest of your code remains the same
        impact_text = Text("CONSEQUENCES", color=BLACK, weight=BOLD).next_to(matrix, UP)
        likelihood_text = Text("LIKELIHOOD", color=BLACK, weight=BOLD).next_to(matrix, LEFT, buff=0.3).rotate(90*DEGREES)

        # Define risks with initial and final positions for cyber attack
        risks = [
            {"name": "BOEING 737 MAX CRISIS", "pos": [2, 2, 0], "final_pos": [2, 2, 0]},  # Catastrophic impact, occurred
            {"name": "HURRICANE KATRINA", "pos": [2, -1, 0], "final_pos": [2, -1, 0]},  # Catastrophic impact, rare
        ]

        risk_dots = VGroup()
        risk_labels = VGroup()

        # Create dots and labels
        for risk in risks:
            dot = Dot(risk["pos"], color=BLUE_E, radius=0.15)
            label = Text(risk["name"], color=BLACK, font_size=24, weight=BOLD)
            label.next_to(dot, RIGHT, buff=0.5)
            risk_dots.add(dot)
            risk_labels.add(label)

        # Initial matrix and text animations
        self.play(
            ShowCreation(matrix, run_time=3, lag_ratio=0.1),
            Write(impact_text, run_time=2),
            Write(likelihood_text, run_time=2)
        )

        # Animate each risk point separately
        for i in range(len(risks)):
            self.play(
                FadeIn(risk_dots[i], run_time=1),
                Write(risk_labels[i], run_time=1)
            )
            self.wait(0.5)

        self.wait(2.5)  # Wait 2.5 seconds after initial animation

        # Define multiple random positions for each risk
        random_positions = [
            # Positions for Boeing 737 MAX
            [
                [-1, 1, 0],    # Position 1
                [0, -2, 0],    # Position 2
                [1, 0, 0],     # Position 3
                [-2, -1, 0],   # Position 4
                [1, 2, 0],     # Position 5
            ],
            # Positions for Hurricane Katrina
            [
                [1, -1, 0],    # Position 1
                [-2, 1, 0],    # Position 2
                [0, 2, 0],     # Position 3
                [2, 0, 0],     # Position 4
                [-1, -2, 0],   # Position 5
            ]
        ]

        # Animate through each random position
        for pos_index in range(5):
            self.play(
                *[risk_dots[i].animate.move_to(random_positions[i][pos_index]) for i in range(len(risks))],
                *[risk_labels[i].animate.next_to(random_positions[i][pos_index], RIGHT, buff=0.5) for i in range(len(risks))],
                run_time=1.0
            )
            self.wait(0.25)

        # Return to original positions
        self.play(
            *[risk_dots[i].animate.move_to(risks[i]["final_pos"]) for i in range(len(risks))],
            *[risk_labels[i].animate.next_to(risks[i]["final_pos"], RIGHT, buff=0.5) for i in range(len(risks))],
            run_time=1.875
        )

        self.wait(2)
