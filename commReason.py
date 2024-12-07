from manimlib import *

class PoliticalSilenceReasons(Scene):
    def construct(self):
        # Add camera adjustments at the beginning of construct
        self.camera.frame.scale(1.25)  # Zoom out 25%
        self.camera.frame.shift(DOWN * 1.0)  # Move up 25%

        # Add helper function for number formatting
        def format_number(num):
            if num >= 1000000:
                return f"{num/1000000:.1f}M"
            elif num >= 1000:
                return f"{num/1000:.0f}K"
            else:
                return str(num)
        
        # Define the data with scrambled order and sample size
        sample_size = 2.5  # 2.5 million people
        reasons = [
            "WON'T BE LISTENED TO",    
            "SOCIAL ISOLATION",         
            "WORK CONSEQUENCES",
            "PRIVACY CONCERNS",         
            "FEAR OF CONFLICT"          
        ]
        probabilities = [0.85, 0.45, 0.55, 0.35, 0.65]
        
        # Create axes
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 1, 0.2],
            height=5,
            width=10,
            axis_config={
                "include_tip": True
            }
        ).shift(DOWN * 0.5)
        
        # Add percentage labels on y-axis
        y_labels = VGroup()
        for i in range(6):
            value = i * 0.2
            label = Text(
                f"{int(value * 100)}%",
                font_size=16,
                weight="BOLD"
            ).next_to(axes.c2p(0, value, 0), LEFT, buff=0.1)
            y_labels.add(label)
        
        bars = VGroup()
        labels = VGroup()
        
        for i, (reason, prob) in enumerate(zip(reasons, probabilities)):
            # Create bar with solid color
            bar = Rectangle(
                width=0.8,
                height=prob * 5,
                fill_opacity=1,
                color=BLUE if i == 0 else BLUE_D
            )
            
            # Position bar from the origin (0,0)
            bar_bottom = axes.c2p(i + 1, 0, 0)  # Get position at x=(i+1), y=0
            bar.move_to(bar_bottom, aligned_edge=DOWN)  # Align bottom of bar with this point
            
            # Calculate the actual number (multiplied by 1000 since sample_size is in millions)
            number = int(prob * sample_size * 1000000)
            
            percent_text = Text(
                f"{int(prob * 100)}%",
                font_size=28 if i == 0 else 24,
                weight="BOLD",
                color="#000000",
                fill_opacity=1
            )
            
            count_text = Text(
                f"({format_number(number)})",  # Use the new formatting function
                font_size=24 if i == 0 else 20,
                weight="BOLD",
                color="#000000",
                fill_opacity=1
            )
            
            # Group and position the labels
            stat_group = VGroup(percent_text, count_text).arrange(DOWN, buff=0.1)
            stat_group.move_to(bar.get_top() + UP * 0.4)
            
            # Create reason label with adjusted position
            label = Text(
                reason,
                font_size=24 if i == 0 else 20,
                weight="BOLD",
                color=YELLOW if i == 0 else WHITE
            ).rotate(PI/4)
            
            # Position label to align with bar's bottom center
            label_start = bar.get_bottom()
            label.move_to(label_start)
            # Shift the label so its start (not center) aligns with the bar's bottom
            shift_amount = -(label.get_width() / 2) * np.array([np.cos(PI/4), np.sin(PI/4), 0])
            # Add additional downward shift to prevent overlap
            shift_amount += DOWN * 0.5  # Adjust the 0.5 value to increase/decrease spacing
            label.shift(shift_amount)
            
            bars.add(bar)
            labels.add(VGroup(label, stat_group))
        
        # Updated title with all caps and bold
        title = Text(
            "WHY PEOPLE DON'T SHARE THEIR POLITICAL VIEWS",
            font_size=32,
            weight="BOLD"
        ).to_edge(UP, buff=0.5)
        
        # Animations
        self.play(Write(title), run_time=1.2)
        self.play(
            ShowCreation(axes), 
            *[Write(label) for label in y_labels],
            run_time=1.2
        )
        
        # First animate all bars except the first one (WON'T BE LISTENED TO)
        for bar, label_group in zip(bars[1:], labels[1:]):
            self.play(
                GrowFromEdge(bar, DOWN),
                Write(label_group),
                run_time=1.0
            )
        
        self.wait(1.5)
        
        # Then animate the "WON'T BE LISTENED TO" bar
        self.play(
            GrowFromEdge(bars[0], DOWN),
            Write(labels[0]),
            run_time=1.2
        )
        
        self.wait(2.5)