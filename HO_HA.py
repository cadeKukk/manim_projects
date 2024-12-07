from manimlib import *

class HypothesisAnimation(Scene):
    def construct(self):
        # Create null hypothesis
        h0_title = Text("NULL HYPOTHESIS (H₀):", color=BLUE, font_size=36, weight=BOLD)
        h0_text = Text("BETTER TECHNOLOGY HAS NO SIGNIFICANT IMPACT\nON THE QUALITY OF GOVERNANCE.", 
                      font_size=28, weight=BOLD)
        
        h0_group = VGroup(h0_title, h0_text).arrange(DOWN, buff=0.5)
        h0_group.shift(UP * 1.5)
        
        # Create alternative hypothesis
        ha_title = Text("ALTERNATIVE HYPOTHESIS (Hₐ):", color=RED, font_size=36, weight=BOLD)
        ha_text = Text("BETTER TECHNOLOGY DOES NOT LEAD TO BETTER GOVERNANCE\nDUE TO MISUSE AND LACK OF UNDERSTANDING TECHNOLOGY.", 
                      font_size=28, weight=BOLD)
        
        ha_group = VGroup(ha_title, ha_text).arrange(DOWN, buff=0.5)
        ha_group.next_to(h0_group, DOWN, buff=1)
        
        # Create highlight box
        highlight_box = SurroundingRectangle(ha_group, color=YELLOW, buff=0.2)
        
        # Create final transformation text
        final_text1 = Text("TECHNOLOGY IS A TOOL,", color=YELLOW, font_size=68, weight=BOLD)
        final_text2 = Text("PEOPLE ARE THE TOOL", color=YELLOW, font_size=36, weight=BOLD)
        
        # Position them independently
        final_text1.move_to(ORIGIN)
        final_text2.next_to(final_text1, DOWN, buff=0.5)
        
        # Initial animation sequence
        self.play(Write(h0_title))
        self.play(Write(h0_text))
        self.wait()
        
        self.play(Write(ha_title))
        self.play(Write(ha_text))
        self.wait(1)
        
        # Add highlight box
        self.play(ShowCreation(highlight_box))
        self.wait(1)
        
        # Transform both hypothesis groups into the first line
        self.play(
            Transform(VGroup(h0_group, ha_group, highlight_box), final_text1),
            run_time=1.5
        )
        
        self.wait(1)  # Wait for a second
        
        # Write the second line
        self.play(Write(final_text2), run_time=1.5)
        
        # Final pause
        self.wait(3)
