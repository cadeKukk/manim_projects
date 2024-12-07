from manimlib import *
import numpy as np

class SatisfactionGraph(Scene):
    def construct(self):
        # Data
        countries = [
            "Singapore", "India", "Sweden", "Thailand", "Australia", "Netherlands",
            "Philippines", "Poland", "Germany", "Malaysia", "Canada", "Mexico",
            "Hungary", "Brazil", "Argentina", "UK", "Sri Lanka", "France",
            "South Korea", "Japan", "U.S.", "Italy", "Spain", "Chile",
            "Greece", "Colombia", "Peru"
        ]
        satisfied = [
            80, 77, 75, 64, 60, 58, 57, 57, 55, 51, 52, 50, 49, 44, 44,
            39, 38, 35, 36, 31, 31, 30, 30, 30, 22, 21, 11
        ]
        
        # Color gradient based on satisfaction level
        def get_color(value):
            if value >= 70:
                return "#00FF00"  # Green
            elif value >= 50:
                return "#FFFF00"  # Yellow
            elif value >= 30:
                return "#FFA500"  # Orange
            else:
                return "#FF0000"  # Red

        # Create reference line - positioned closer to top
        reference_line = Line(
            LEFT * 4, RIGHT * 4,
            stroke_width=2
        ).shift(UP * 2)  # Reduced vertical shift
        
        # Add tick marks and numbers
        ticks = VGroup()
        numbers = VGroup()
        for i in range(0, 101, 20):
            x = reference_line.get_left()[0] + (i/100) * reference_line.get_length()
            tick = Line(UP * 0.1, DOWN * 0.1).move_to([x, reference_line.get_y(), 0])
            number = Text(str(i), font_size=20).next_to(tick, DOWN, buff=0.1)
            ticks.add(tick)
            numbers.add(number)

        # Create bars, inverse bars, and labels
        bars = VGroup()
        inverse_bars = VGroup()  # New group for inverse bars
        labels = VGroup()
        all_elements = VGroup()
        
        BAR_HEIGHT = 0.3
        SPACE_FACTOR = 1.5
        
        # Title - positioned closer to first bar
        title = Text("Global Satisfaction Levels (%)", font_size=36)
        title.next_to(reference_line, UP, buff=0.3)  # Reduced buffer
        
        # Add reference elements to group
        reference_group = VGroup(reference_line, ticks, numbers, title)
        all_elements.add(reference_group)
        
        # Create and position bars
        for i, (country, value) in enumerate(zip(countries, satisfied)):
            # Original bar
            bar_width = (value/100) * reference_line.get_length()
            bar = Rectangle(
                height=BAR_HEIGHT,
                width=bar_width,
                fill_opacity=0.8,
                fill_color=get_color(value),
                stroke_width=1,
                stroke_color=WHITE
            )
            
            # Inverse bar (100 - value)
            inverse_width = ((100 - value)/100) * reference_line.get_length()
            inverse_bar = Rectangle(
                height=BAR_HEIGHT,
                width=inverse_width,
                fill_opacity=0.3,  # More transparent
                fill_color=BLUE,   # Different color for contrast
                stroke_width=1,
                stroke_color=WHITE
            )
            
            # Position bars
            bar.align_to(reference_line, LEFT)
            bar.shift(DOWN * (i * BAR_HEIGHT * SPACE_FACTOR + BAR_HEIGHT))
            
            inverse_bar.align_to(reference_line, LEFT)
            inverse_bar.shift(DOWN * (i * BAR_HEIGHT * SPACE_FACTOR + BAR_HEIGHT))
            
            bars.add(bar)
            inverse_bars.add(inverse_bar)
            
            label = Text(
                f"{country} ({value}%)", 
                font_size=20,
                color=WHITE
            ).next_to(bar, LEFT, buff=0.3)
            labels.add(label)
            
            all_elements.add(bar, inverse_bar, label)
        
        # Initial camera position - centered on title and first bar
        self.camera.frame.move_to(title.get_center() + DOWN * 2)
        
        # Initial animations
        self.play(Write(title))
        self.play(
            ShowCreation(reference_line),
            ShowCreation(ticks),
            Write(numbers)
        )
        
        # Animate only the original bars and labels first
        for i, (bar, label) in enumerate(zip(bars, labels)):
            target_y = bar.get_center()[1]
            self.play(
                ShowCreation(bar),
                Write(label),
                self.camera.frame.animate.move_to([0, target_y, 0]),
                run_time=0.5
            )
        
        # Calculate perfect frame size and position for final zoom
        top_edge = reference_group.get_top()[1]
        bottom_edge = bars[-1].get_bottom()[1]
        left_edge = labels.get_left()[0]
        right_edge = reference_line.get_right()[0]
        
        center_y = (top_edge + bottom_edge) / 2
        center_x = (left_edge + right_edge) / 2
        height = top_edge - bottom_edge
        
        # Move center down by 15% of the height
        center_y -= height * 0.10
        
        width = right_edge - left_edge
        
        # Calculate required scale
        scale_factor = max(height / 10, width / 16) * 1.1
        
        # Create the main label for inverse bars - reduced buffer by 10%
        inverse_label = Text(
            "Government Technology\nAdoption Rate",
            font_size=48,
            color=BLUE
        ).next_to(all_elements, RIGHT, buff=0.5)  # Reduced from 1 to 0.9
        
        # Create the subtitle
        subtitle = Text(
            "(all stats are self-reported)",
            font_size=48,
            color=WHITE
        ).next_to(inverse_label, DOWN, buff=0.3)
        
        # Find the U.S. bar index
        us_index = countries.index("U.S.")
        us_bar = bars[us_index]
        us_label = labels[us_index]
        
        # Create highlight box around U.S. bar and label
        highlight_box = Rectangle(
            width=us_label.get_width() + reference_line.get_width(),  # Width to cover label and full bar width
            height=BAR_HEIGHT * 1.5,  # Slightly taller than the bar
            stroke_color=YELLOW,
            stroke_width=3,
            fill_opacity=0
        )
        
        # Position the box to cover both bar and label
        highlight_box.move_to(us_bar.get_center())  # Center on the bar first
        highlight_box.align_to(us_label, LEFT)  # Align with left edge of label
        highlight_box.shift(LEFT * (highlight_box.get_width() * 0.1))  # Shift left by 10% of box width
        
        # Final overview zoom out
        self.play(
            self.camera.frame.animate
                .scale(scale_factor)
                .move_to([center_x, center_y, 0]),
            run_time=2
        )
        
        # Wait for a second before showing inverse bars
        self.wait(1)
        
        # After wait, animate inverse bars and main label appearing together
        self.play(
            *[ShowCreation(inverse_bar) for inverse_bar in inverse_bars],
            Write(inverse_label),
            run_time=1.5
        )
        
        # Short wait before showing subtitle
        self.wait(0.5)
        
        # Animate subtitle appearing
        self.play(
            Write(subtitle),
            run_time=1
        )
        
        # Wait a moment before showing highlight
        self.wait(1)
        
        # Animate the highlight box
        self.play(
            ShowCreation(highlight_box),
            run_time=1
        )
        
        self.wait()
