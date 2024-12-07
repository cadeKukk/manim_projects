from manimlib import *
from manimlib.animation.creation import ShowCreation

class SatisfactionGraph(Scene):
    def setup(self):
        self.camera.frame.shift(RIGHT * 232.5)
        self.camera.frame.scale(0.6)
        
    def construct(self):
        # Scale everything down and center it
        scale_factor = 0.7
        
        # Create axes with updated time range
        axes = Axes(
            x_range=[2005, 2024, 2],
            y_range=[0, 100, 20],
            height=5,
            width=7,
            axis_config={
                "include_tip": False,
                "include_numbers": True,
                "decimal_number_config": {
                    "num_decimal_places": 0,
                    "font_size": 20,
                    "group_with_commas": False
                }
            },
            x_axis_config={"include_ticks": False},
            y_axis_config={"include_ticks": False}
        )
        
        axes.scale(scale_factor)
        axes.center()

        # Create grid with updated range
        grid = VGroup()
        for x in range(2005, 2025, 2):
            line = Line(
                axes.c2p(x, 0),
                axes.c2p(x, 100),
                stroke_width=0.5,
                stroke_opacity=0.2
            )
            grid.add(line)
        for y in range(0, 101, 20):
            line = Line(
                axes.c2p(2005, y),
                axes.c2p(2024, y),
                stroke_width=0.5,
                stroke_opacity=0.2
            )
            grid.add(line)

        # Add y-axis labels back
        y_labels = VGroup(*[
            Text(f"{i}%", font_size=16).next_to(axes.c2p(2005, i), LEFT, 0.2)
            for i in range(0, 101, 20)
        ])

        # Updated modern technologies
        technologies = {
            "Artificial Intelligence": {
                "color": "#FFD700",
                "data": [(2005, 5), (2010, 15), (2015, 35), (2018, 55), 
                        (2020, 75), (2022, 90), (2024, 95)]
            },
            "Cloud Computing": {
                "color": "#90EE90",
                "data": [(2005, 10), (2010, 30), (2015, 60), (2018, 75), 
                        (2020, 85), (2022, 90), (2024, 95)]
            },
            "Social Media": {
                "color": "#FF4040",
                "data": [(2005, 20), (2010, 45), (2015, 70), (2018, 85), 
                        (2020, 90), (2022, 88), (2024, 85)]
            },
            "Blockchain": {
                "color": "#20B2AA",
                "data": [(2005, 0), (2010, 5), (2015, 15), (2018, 45), 
                        (2020, 60), (2022, 65), (2024, 70)]
            },
            "Quantum Computing": {
                "color": "#DA70D6",
                "data": [(2005, 0), (2010, 0), (2015, 5), (2018, 15), 
                        (2020, 45), (2022, 70), (2024, 85)]
            },
            "Machine Learning": {
                "color": "#FFA500",
                "data": [(2005, 8), (2010, 20), (2015, 40), (2018, 65), 
                        (2020, 80), (2022, 88), (2024, 92)]
            },
            "Cybersecurity": {
                "color": "#228B22",
                "data": [(2005, 0), (2010, 2), (2015, 5), (2018, 10), 
                        (2020, 15), (2022, 25), (2024, 35)]
            },
            "IoT Devices": {
                "color": "#CD5C5C",
                "data": [(2005, 5), (2010, 15), (2015, 35), (2018, 55), 
                        (2020, 70), (2022, 80), (2024, 85)]
            },
            "Virtual Reality": {
                "color": "#4169E1",
                "data": [(2005, 5), (2010, 10), (2015, 20), (2018, 35), 
                        (2020, 45), (2022, 60), (2024, 70)]
            }
        }

        # Create graphs
        graphs = VGroup()
        for tech, info in technologies.items():
            points = info["data"]
            graph = VMobject()
            graph.set_points_smoothly([
                axes.c2p(x, y) for x, y in points
            ])
            graph.set_color(info["color"])
            graphs.add(graph)

        # Create legend
        legend_entries = VGroup()
        for i, (tech, info) in enumerate(technologies.items()):
            line = Line(LEFT * 0.25, RIGHT * 0.25, color=info["color"], stroke_width=3)
            text = Text(tech, font_size=14)
            entry = VGroup(line, text.next_to(line, RIGHT, 0.1))
            entry.next_to(axes, RIGHT, buff=0.2)
            entry.shift(UP * (1.5 - i * 0.3))
            legend_entries.add(entry)

        # Group everything
        entire_graph = VGroup(axes, grid, y_labels, graphs, legend_entries)
        
        # Final positioning of entire graph
        entire_graph.move_to(ORIGIN)
        entire_graph.scale(0.9)

        # Animations
        self.play(ShowCreation(axes))
        self.play(ShowCreation(grid))
        self.play(*[Write(label) for label in y_labels])
        
        for graph, entry in zip(graphs, legend_entries):
            self.play(ShowCreation(graph), Write(entry), run_time=1)
        
        self.wait(2)
        
        # Create and animate highlight box for 2017
        highlight_box = Rectangle(
            width=0.5,  # Small width to highlight just 2017
            height=axes.get_height(),
            stroke_width=2,
            stroke_color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.2
        )
        highlight_box.move_to(axes.c2p(2017, 50))  # Position at 2017 (y=50 is middle of axis)
        self.play(ShowCreation(highlight_box))
        
        self.wait(1)
        
        # Create and animate highlight box for Social Media legend entry
        social_media_entry = legend_entries[2]  # Social Media is the third entry
        social_media_highlight = Rectangle(
            width=social_media_entry.get_width() + 0.2,
            height=social_media_entry.get_height() + 0.1,
            stroke_width=2,
            stroke_color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.2
        )
        social_media_highlight.move_to(social_media_entry)
        self.play(ShowCreation(social_media_highlight))
        
        self.wait(1)
        
        # Create and display UNITED STATES label
        country_label = Text(
            "UNITED STATES",
            font_size=36,
            weight=BOLD
        ).move_to(entire_graph.get_center() + UP * 0.5)
        self.play(Write(country_label))
        
        self.wait(1)
        
        # Fade out existing highlight boxes
        self.play(
            FadeOut(highlight_box),
            FadeOut(social_media_highlight)
        )
        
        # Create and animate highlight box for Cybersecurity legend entry
        cybersecurity_entry = legend_entries[6]  # Cybersecurity is the 7th entry
        cybersecurity_highlight = Rectangle(
            width=cybersecurity_entry.get_width() + 0.2,
            height=cybersecurity_entry.get_height() + 0.1,
            stroke_width=2,
            stroke_color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.2
        )
        cybersecurity_highlight.move_to(cybersecurity_entry)
        self.play(ShowCreation(cybersecurity_highlight))
        
        self.wait(1)