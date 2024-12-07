from manimlib import *

class TechLiteracyScene(Scene):
    def construct(self):
        # Set initial camera frame scale
        self.camera.frame.scale(1.15)  # Zoom out by 15%
        
        # Create the main text elements with smaller font size
        text1 = Text("CAUSAL MECHANISM", font_size=84, weight=BOLD)
        text2 = Text("LACK OF TECHNOLOGICAL LITERACY", font_size=72, weight=BOLD)
        
        # Create the bottom texts as separate elements
        better_left_top = Text("BETTER", font_size=48, weight=BOLD)
        better_left_bottom = Text("TECHNOLOGY", font_size=48, weight=BOLD)
        better_right_top = Text("BETTER", font_size=48, weight=BOLD)
        better_right_bottom = Text("GOVERNMENT", font_size=48, weight=BOLD)
        
        # Group and arrange the corner texts vertically
        left_group = VGroup(better_left_top, better_left_bottom).arrange(DOWN, buff=0.2)
        right_group = VGroup(better_right_top, better_right_bottom).arrange(DOWN, buff=0.2)
        
        # Position texts
        text1.center()
        text2.center()
        left_group.to_corner(DOWN + LEFT, buff=0.5)
        right_group.to_corner(DOWN + RIGHT, buff=0.5)
        
        # Create arrows going to/from centers with larger buffers
        arrow1 = Arrow(
            left_group.get_center(),
            text2.get_center(),
            buff=1.2,
            color=WHITE
        )
        
        arrow2 = Arrow(
            text2.get_center(),
            right_group.get_center(),
            buff=1.2,
            color=WHITE  # Start as white, will transition to red
        )
        
        # Animation sequence
        self.play(Write(text1))
        self.wait(2)
        self.play(Transform(text1, text2))
        self.wait(2)
        self.play(
            Write(left_group),
            Write(right_group)
        )
        self.wait(1)
        self.play(GrowArrow(arrow1))
        self.wait(0.5)
        self.play(GrowArrow(arrow2))
        self.wait(2)
        
        # Color transition animations
        self.play(
            text1[6:28].animate.set_color(RED)  # Adjusted indices to get full "TECHNOLOGICAL LITERACY"
        )
        self.wait(1)
        self.play(
            arrow2.animate.set_color(RED),
            run_time=2  # Slower transition for the arrow
        )
        self.wait(0.5)
        self.play(
            right_group.animate.set_color(RED),
            run_time=1
        )
        self.wait(2)
