from manimlib import *

class IdeologyDistribution(Scene):
    def construct(self):
        # Colors from the image
        dem_color = "#607D8B"  # Blue-grey
        rep_color = "#E57373"  # Salmon-red
        overlap_color = "#4A5459"  # Darker grey for overlap
        reference_color = "#D3D3C3"  # Beige-grey for reference curve

        # Create year labels - kept lower
        year_1994 = Text("1994", font_size=48, weight=BOLD).shift(LEFT * 3 + UP * 2.5).to_edge(UP)
        year_2017 = Text("2017", font_size=48, weight=BOLD).shift(RIGHT * 3 + UP * 2.5).to_edge(UP)

        # Create party labels - moved back to original positions
        dem_label_1994 = Text("AVERAGE\nDEMOCRAT", color=dem_color, font_size=32, weight=BOLD).shift(LEFT * 4.5 + UP * 2)
        rep_label_1994 = Text("AVERAGE\nREPUBLICAN", color=rep_color, font_size=32, weight=BOLD).shift(LEFT * 1.5 + UP * 2)
        dem_label_2017 = Text("AVERAGE\nDEMOCRAT", color=dem_color, font_size=32, weight=BOLD).shift(RIGHT * 1.5 + UP * 2)
        rep_label_2017 = Text("AVERAGE\nREPUBLICAN", color=rep_color, font_size=32, weight=BOLD).shift(RIGHT * 4.5 + UP * 2)

        # Create the distribution curves - kept lower
        # 1994 distributions
        dem_curve_1994 = self.create_distribution_curve(dem_color, LEFT * 3 + DOWN * 1)
        rep_curve_1994 = self.create_distribution_curve(rep_color, LEFT * 3 + DOWN * 1, shift_right=1)

        # 2017 distributions
        dem_curve_2017 = self.create_distribution_curve(dem_color, RIGHT * 3 + DOWN * 1, steeper=True)
        rep_curve_2017 = self.create_distribution_curve(rep_color, RIGHT * 3 + DOWN * 1, shift_right=2)

        # Create vertical peak lines
        # 1994 peak lines
        dem_peak_1994 = Line(
            start=LEFT * 4 + DOWN * 2,  # Democrat peak position unchanged
            end=LEFT * 4 + UP * 1,
            color=dem_color,
            stroke_width=2
        )
        
        rep_peak_1994 = Line(
            start=LEFT * 3 + DOWN * 2,  # Slight adjustment more to the left
            end=LEFT * 3 + UP * 1,
            color=rep_color,
            stroke_width=2
        )

        # 2017 peak lines
        dem_peak_2017 = Line(
            start=RIGHT * 2 + DOWN * 2,  # Democrat peak position unchanged
            end=RIGHT * 2 + UP * 1,
            color=dem_color,
            stroke_width=2
        )
        
        rep_peak_2017 = Line(
            start=RIGHT * 4 + DOWN * 2,  # 2017 Republican peak position unchanged
            end=RIGHT * 4 + UP * 1,
            color=rep_color,
            stroke_width=2
        )

        # Create horizontal middle reference lines
        middle_line_1994 = Line(
            start=LEFT * 5 + DOWN * 1,
            end=LEFT * 1 + DOWN * 1,
            color=GREY,
            stroke_width=1,
            stroke_opacity=0.5
        )
        
        middle_line_2017 = Line(
            start=RIGHT * 1 + DOWN * 1,
            end=RIGHT * 5 + DOWN * 1,
            color=GREY,
            stroke_width=1,
            stroke_opacity=0.5
        )

        # Create vertical center lines with increased visibility
        center_line_1994 = Line(
            start=LEFT * 3.5 + DOWN * 2,  # Halfway between dem_peak_1994 (4) and rep_peak_1994 (3)
            end=LEFT * 3.5 + UP * 1,
            color=GREY,
            stroke_width=2,
            stroke_opacity=0.8
        )
        
        center_line_2017 = Line(
            start=RIGHT * 3 + DOWN * 2,  # Halfway between dem_peak_2017 (2) and rep_peak_2017 (4)
            end=RIGHT * 3 + UP * 1,
            color=GREY,
            stroke_width=2,
            stroke_opacity=0.8
        )

        # Create highlight rectangle for 2017
        highlight_rect = SurroundingRectangle(
            year_2017,
            color=YELLOW,
            buff=0.2,
            stroke_width=3
        )

        # Create a simple connecting line for 1994 medians
        distance_line_1994 = Line(
            start=LEFT * 4,  # Democrat peak position
            end=LEFT * 3,    # Republican peak position
            color=WHITE,
            stroke_width=2
        ).shift(UP * 1.5)  # Position above the peaks

        # Add vertical connecting lines for the bracket
        left_vertical_1994 = Line(
            start=LEFT * 4 + UP * 1.5,  # Top of left side (matches distance_line position)
            end=LEFT * 4 + UP * 1,      # Connect to Democrat peak line
            color=WHITE,
            stroke_width=2
        )

        right_vertical_1994 = Line(
            start=LEFT * 3 + UP * 1.5,  # Top of right side (matches distance_line position)
            end=LEFT * 3 + UP * 1,      # Connect to Republican peak line
            color=WHITE,
            stroke_width=2
        )

        # Animation sequence
        # First show 1994 elements
        self.play(
            Write(year_1994),
            Write(dem_label_1994),
            Write(rep_label_1994)
        )

        self.play(
            ShowCreation(middle_line_1994),
            ShowCreation(center_line_1994)
        )

        self.play(
            ShowCreation(dem_curve_1994),
            ShowCreation(rep_curve_1994)
        )

        self.play(
            ShowCreation(dem_peak_1994),
            ShowCreation(rep_peak_1994)
        )

        # Wait for 3 seconds
        self.wait(3)

        # Then show 2017 elements
        self.play(
            Write(year_2017),
            Write(dem_label_2017),
            Write(rep_label_2017)
        )

        self.play(
            ShowCreation(middle_line_2017),
            ShowCreation(center_line_2017)
        )

        self.play(
            ShowCreation(dem_curve_2017),
            ShowCreation(rep_curve_2017)
        )

        self.play(
            ShowCreation(dem_peak_2017),
            ShowCreation(rep_peak_2017)
        )

        self.wait(1)

        # Add highlight rectangle around 2017
        self.play(
            ShowCreation(highlight_rect)
        )

        # Now show all parts of the bracket together
        self.play(
            ShowCreation(distance_line_1994),
            ShowCreation(left_vertical_1994),
            ShowCreation(right_vertical_1994)
        )

        self.wait(2)

        # Add X2 label - positioned for 2017 location
        x2_label = Text(
            "X2", 
            font_size=36,
            color=WHITE
        ).next_to(right_vertical_1994.copy().shift(RIGHT * 6), RIGHT, buff=0.2)

        # After the bracket moves to 2017 position, show the label
        self.play(
            distance_line_1994.animate.shift(RIGHT * 6),
            left_vertical_1994.animate.shift(RIGHT * 6),
            right_vertical_1994.animate.shift(RIGHT * 6)
        )

        self.play(
            Write(x2_label)
        )

        self.wait(2)

        # After the X2 label animation and wait
        
        # Create intersection highlights for overlapping areas
        intersection_1994 = VMobject()
        intersection_1994.set_points_smoothly([
            LEFT * 3.75 + DOWN * 2,    # Bottom left of overlap
            LEFT * 3.5 + DOWN * 1.2,   # Middle of overlap
            LEFT * 3.25 + DOWN * 2     # Bottom right of overlap
        ])
        intersection_1994.set_fill(PURPLE, opacity=0.3)  # Lower opacity to see both curves
        intersection_1994.set_stroke(PURPLE, width=0)

        intersection_2017 = VMobject()
        intersection_2017.set_points_smoothly([
            RIGHT * 2.75 + DOWN * 2,   # Bottom left of overlap
            RIGHT * 3 + DOWN * 1.2,    # Middle of overlap
            RIGHT * 3.25 + DOWN * 2    # Bottom right of overlap
        ])
        intersection_2017.set_fill(PURPLE, opacity=0.3)  # Lower opacity to see both curves
        intersection_2017.set_stroke(PURPLE, width=0)

        # Show 1994 intersection
        self.play(
            FadeIn(intersection_1994)
        )
        
        self.wait(2)

        # Show 2017 intersection
        self.play(
            FadeIn(intersection_2017)
        )
        
        self.wait(2)

    def create_distribution_curve(self, color, offset, shift_right=0, shift_down=0, scale=1, steeper=False):
        if steeper:
            control_points = [
                [-2, 0, 0],
                [-1, 2, 0],
                [0, 0.5, 0],
                [1, 0, 0],
                [2, 0, 0]
            ]
        else:
            control_points = [
                [-2, 0, 0],
                [-1, 1.5, 0],
                [0, 1, 0],
                [1, 0.5, 0],
                [2, 0, 0]
            ]
        
        curve = VMobject()
        curve.set_points_smoothly([
            np.array(point) * scale + offset + RIGHT * shift_right + DOWN * shift_down 
            for point in control_points
        ])
        curve.set_color(color)
        curve.set_fill(color, opacity=0.3)
        return curve
