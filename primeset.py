from manimlib import *

class RiemannExplanation(Scene):
    def construct(self):
        # Introduction
        title = Text("The Riemann Hypothesis", font_size=48).to_edge(UP)
        subtitle = Text("One of Mathematics' Greatest Unsolved Problems", 
                       font_size=32).next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait(2)
        self.play(FadeOut(subtitle))

        # Step 1: Introduce the Zeta Function
        zeta_formula = Tex(
            r"\zeta(s) = \sum_{n=1}^{\infty} \frac{1}{n^s}",
            font_size=48
        ).next_to(title, DOWN, buff=1)
        
        zeta_explanation = Text(
            "The Riemann zeta function extends this sum to complex numbers",
            font_size=32
        ).next_to(zeta_formula, DOWN)
        
        self.play(Write(zeta_formula))
        self.play(FadeIn(zeta_explanation))
        self.wait(3)
        self.play(FadeOut(zeta_explanation), FadeOut(zeta_formula))

        # Step 2: Show the Complex Plane
        complex_plane = ComplexPlane().add_coordinate_labels()
        self.play(Create(complex_plane))
        
        # Highlight Critical Strip
        critical_strip = Rectangle(
            width=1,
            height=FRAME_HEIGHT,
            stroke_color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.2
        ).move_to(complex_plane.c2p(0.5, 0))
        
        critical_line = Line(
            complex_plane.c2p(0.5, -FRAME_HEIGHT/2),
            complex_plane.c2p(0.5, FRAME_HEIGHT/2),
            color=RED
        )
        
        self.play(
            FadeIn(critical_strip),
            Create(critical_line)
        )

        # Add labels
        strip_label = Text("Critical Strip", font_size=24).next_to(critical_strip, UP)
        line_label = Text("Critical Line (Re(s) = 1/2)", font_size=24).next_to(critical_line, RIGHT)
        
        self.play(
            Write(strip_label),
            Write(line_label)
        )
        self.wait(2)

        # Step 3: Show Some Zeros
        zeros = [
            complex_plane.c2p(0.5, y) for y in [14.135, 21.022, 25.011]
        ]
        zero_dots = VGroup(*[Dot(point, color=BLUE) for point in zeros])
        zero_labels = VGroup(*[
            Tex(r"\rho_" + str(i), font_size=24).next_to(dot, RIGHT)
            for i, dot in enumerate(zero_dots, 1)
        ])

        self.play(
            FadeIn(zero_dots),
            Write(zero_labels)
        )

        # Step 4: Explain the Hypothesis
        hypothesis = Text(
            "The Riemann Hypothesis states that all non-trivial zeros\n"
            "have real part equal to 1/2",
            font_size=32
        ).to_edge(DOWN)
        
        self.play(Write(hypothesis))
        self.wait(2)

        # Step 5: Show Connection to Prime Numbers
        self.play(
            FadeOut(hypothesis),
            FadeOut(zero_labels),
            FadeOut(zero_dots)
        )

        prime_formula = Tex(
            r"\zeta(s) = \prod_{p \text{ prime}} \frac{1}{1-p^{-s}}",
            font_size=48
        ).next_to(title, DOWN, buff=1)
        
        prime_explanation = Text(
            "The zeros are deeply connected to the distribution of prime numbers",
            font_size=32
        ).next_to(prime_formula, DOWN)

        self.play(
            Write(prime_formula),
            FadeIn(prime_explanation)
        )
        self.wait(3)

        # Final Summary
        summary = VGroup(
            Text("If proven true, the Riemann Hypothesis would:", font_size=32),
            Text("• Give us deep insights into prime numbers", font_size=28),
            Text("• Solve many other mathematical problems", font_size=28),
            Text("• Earn you $1 million from the Clay Institute", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(DOWN)

        self.play(
            FadeOut(prime_formula),
            FadeOut(prime_explanation),
            Write(summary)
        )
        self.wait(3)

        # Optional: Add a visualization of prime counting function
        pi_x = Tex(
            r"\pi(x) = \text{Li}(x) + \text{Error}(x)",
            font_size=36
        ).next_to(summary, UP, buff=1)
        
        self.play(Write(pi_x))
        self.wait(2)

        # Final fade out
        self.play(
            FadeOut(VGroup(*self.mobjects))
        )
        self.wait(1)