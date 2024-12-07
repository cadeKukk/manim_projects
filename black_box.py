from manimlib import *

class BlackBoxAnimation(Scene):
    def construct(self):
        # Create the black box
        box = Square(side_length=4, fill_opacity=1, color=GREY)
        
        # Create input and output arrows
        input_arrow = Arrow(LEFT * 5, LEFT * 2, buff=0)
        output_arrow = Arrow(RIGHT * 2, RIGHT * 5, buff=0)
        
        # Create input/output text
        input_text = Text("INPUT", font_size=36, weight=BOLD).next_to(input_arrow, UP)
        output_text = Text("OUTPUT", font_size=36, weight=BOLD).next_to(output_arrow, UP)
        
        # Create example inputs (phone, AI symbols)
        phone = Text("📱").scale(2)
        ai_symbol = Text("🤖").scale(2)
        
        # Create internal components - now with two layers
        layer1 = VGroup(
            *[Rectangle(height=0.5, width=1.5, fill_opacity=0.8, color=BLUE) 
              for _ in range(4)]
        ).arrange(DOWN, buff=0.3).shift(LEFT * 0.75)
        
        layer2 = VGroup(
            *[Rectangle(height=0.5, width=1.5, fill_opacity=0.8, color=BLUE) 
              for _ in range(4)]
        ).arrange(DOWN, buff=0.3).shift(RIGHT * 0.75)
        
        # Create connecting arrows between layers
        connecting_arrows_vertical_down = VGroup(
            *[Arrow(layer1[i], layer1[i+1], buff=0.1, color=YELLOW) 
              for i in range(len(layer1)-1)]
        )
        
        connecting_arrows_vertical_up = VGroup(
            *[Arrow(layer2[i+1], layer2[i], buff=0.1, color=YELLOW) 
              for i in range(len(layer2)-1)]
        )
        
        connecting_arrows_horizontal = VGroup(
            *[Arrow(layer1[i], layer2[i], buff=0.1, color=YELLOW) 
              for i in range(len(layer1))]
        )
        
        # Animation sequence
        self.play(FadeIn(box))
        self.play(
            Write(input_text),
            GrowArrow(input_arrow),
            Write(output_text),
            GrowArrow(output_arrow)
        )
        self.wait()

        # Show example inputs
        self.play(FadeIn(phone.next_to(input_arrow, LEFT)), run_time=1.5)
        self.wait(1.5)
        
        # Show error state while still a black box
        self.play(
            output_arrow.animate.set_color(RED),
            run_time=1.5
        )
        self.wait(1)
        
        # Transform box to reveal internals with error already present
        layer2[2].set_color(RED)  # Pre-set the error state
        error_text = Text("ERROR", color=RED, weight=BOLD).scale(0.8)
        error_text.move_to(layer2[2])
        
        self.play(
            box.animate.set_opacity(0.3),
            FadeIn(layer1),
            FadeIn(layer2),
            FadeIn(connecting_arrows_vertical_down),
            FadeIn(connecting_arrows_vertical_up),
            FadeIn(connecting_arrows_horizontal),
            FadeIn(error_text),
            run_time=2.5
        )
        
        self.wait(1.5)
        
        # Show fix
        fix_text = Text("FIX", color=GREEN, weight=BOLD).scale(0.8)
        fix_text.move_to(error_text.get_center())
        
        self.play(
            layer2[2].animate.set_color(GREEN),
            output_arrow.animate.set_color(WHITE),
            ReplacementTransform(error_text, fix_text),
            run_time=1.5
        )
        
        self.wait(1)
        
        # Return fixed block to normal
        self.play(
            layer2[2].animate.set_color(BLUE),
            FadeOut(fix_text),
            run_time=1.5
        )
        
        self.wait(2)
        
        # Create and show rotating arrows for each rectangle
     