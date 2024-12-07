from manimlib import *
import numpy as np
from scipy import stats

class TechLiteracyRegression(Scene):
    def construct(self):
        # Create axes for the scatter plot with a smaller y-range
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 6, 1],
            axis_config={"include_tip": True}
        ).scale(0.8).shift(LEFT * 0.5)

        # Add labels with adjusted positioning
        x_label = VGroup(
            Text("ADVANCEMENTS IN", weight=BOLD).scale(0.5),
            Text("TECHNOLOGY", weight=BOLD).scale(0.5)
        ).arrange(DOWN, buff=0.1)  # Arrange vertically with small buffer

        y_label = VGroup(
            Text("GOVERNMENT", weight=BOLD).scale(0.5),
            Text("SATISFACTION", weight=BOLD).scale(0.5)
        ).arrange(DOWN, buff=0.1)  # Arrange vertically with small buffer
        
        # Adjust x-label position (slightly closer to graph)
        x_label.next_to(axes.x_axis.get_end(), RIGHT + UP * 0.5).shift(RIGHT * 0.3)
        
        # Adjust y-label position (horizontal and near top of axis)
        y_label.next_to(
            axes.y_axis.get_end(), 
            LEFT,
            buff=0.3  # Reduced buffer space
        ).shift(UP * 0.5)  # Move up slightly
        
        # Generate data with controlled bounds
        np.random.seed(42)
        x = np.random.uniform(2, 8, 300)
        y = -0.7 * x + np.random.normal(6, 0.8, 300)
        y = np.clip(y, 0.2, 5.8)
        
        # Calculate final regression line
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        # Create equation displays
        eq_start = Tex(r"y = \beta_0 + \beta_1x + \epsilon").scale(0.7)
        eq_process = Tex(r"\min_{\beta_0, \beta_1} \sum_{i=1}^{n} (y_i - (\beta_0 + \beta_1x_i))^2").scale(0.7)
        
        # Create final equation with moderation note
        eq_final = VGroup(
            Tex(r"y = ", f"{intercept:.2f}", r" + ", f"{slope:.2f}", r"x"),
            Tex(r"\text{(Mod by HC)}")
        ).arrange(RIGHT, buff=0.1).scale(0.7)
        
        # Position equations on the right side
        eq_start.to_edge(RIGHT).shift(LEFT * 2 + UP * 2)
        eq_process.to_edge(RIGHT).shift(LEFT * 2 + UP * 2)
        eq_final.to_edge(RIGHT).shift(LEFT * 2 + UP * 2)

        # Create dots
        dots = VGroup(*[
            Dot(axes.c2p(x_val, y_val), color=BLUE_C, radius=0.03)
            for x_val, y_val in zip(x, y)
        ])

        # Create multiple initial regression lines
        n_lines = 5
        initial_lines = VGroup(*[
            axes.get_graph(
                lambda x: max(min(
                    (slope + (np.random.random() - 0.5) * 0.3) * x + 
                    (intercept + (np.random.random() - 0.5) * 0.5), 
                    5.8), 0.2),
                x_range=[0, 10],
                color=RED_A
            )
            for _ in range(n_lines)
        ])

        # Final regression line
        final_line = axes.get_graph(
            lambda x: max(min(slope * x + intercept, 5.8), 0.2),
            x_range=[0, 10],
            color=RED
        )

        # Create labels and title
        title = Text(
            "HUMAN CAPITAL AND ITS EFFECTS ON\nGOVERNMENT TECH IMPLEMENTATION", 
            font_size=24,
            weight=BOLD
        ).to_edge(UP)
        p_value_text = Text(
            "p-value: 0.043178", 
            font_size=48,
            weight=BOLD
        ).to_edge(DOWN).shift(UP * 0.5)  # Moved up slightly
        
        # Position elements
        title.to_edge(UP)
        p_value_text.to_edge(DOWN)  # Move p-value to the bottom

        # Animation sequence
        self.play(Write(title))
        self.play(ShowCreation(axes))
        self.play(Write(x_label), Write(y_label))
        
        # Show initial equation
        self.play(Write(eq_start))
        
        self.play(LaggedStart(*[ShowCreation(dot) for dot in dots], lag_ratio=0.01))
        self.wait()

        # Transform to process equation
        self.play(
            ReplacementTransform(eq_start, eq_process)
        )

        # Show initial lines appearing
        self.play(
            LaggedStart(*[ShowCreation(line) for line in initial_lines], 
            lag_ratio=0.2)
        )
        self.wait()

        # Transform all lines to the final line and show final equation
        self.play(
            *[Transform(line, final_line) for line in initial_lines],
            ReplacementTransform(eq_process, eq_final),
            run_time=2
        )
        
        # Show p-value
        self.play(Write(p_value_text))
        
        # Create confidence interval shading
        upper_bound = axes.get_graph(
            lambda x: max(min((slope + std_err) * x + (intercept + std_err), 5.8), 0.2),
            color=RED_A
        )
        lower_bound = axes.get_graph(
            lambda x: max(min((slope - std_err) * x + (intercept - std_err), 5.8), 0.2),
            color=RED_A
        )
        confidence_interval = VGroup(upper_bound, lower_bound).set_fill(opacity=0.2)

        self.play(ShowCreation(confidence_interval))
        self.wait(1)
        
        # Create and animate highlight box around p-value
        highlight_box = SurroundingRectangle(
            p_value_text,
            buff=0.2,
            color=YELLOW,
            stroke_width=3
        )
        self.play(ShowCreation(highlight_box))
        
        # Add comparison text
        comparison_text = Text(
            "< 0.05",
            font_size=48,
            weight=BOLD
        ).next_to(p_value_text, RIGHT, buff=0.5)
        
        self.play(Write(comparison_text))
        self.wait(2)
