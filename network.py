from manimlib import *
import numpy as np
import random

class NetworkAnimation(Scene):
    def construct(self):
        # Camera setup
        frame = self.camera.frame
        frame.set_euler_angles(
            theta=30 * DEGREES,
            phi=75 * DEGREES,
        )
        frame.scale(2.0)
        
        # Create points
        num_points = 20
        points = VGroup()
        
        # Initialize points in 3D space
        for _ in range(num_points):
            # Create a small circle to represent a point
            point = Circle(
                radius=0.1,
                fill_opacity=1,
                stroke_width=0,
                color=BLUE_A
            ).rotate(about_point=ORIGIN, angle=random.uniform(0, TAU))
            
            # Move to random position
            point.move_to(
                np.array([
                    np.random.uniform(-3, 3),
                    np.random.uniform(-3, 3),
                    np.random.uniform(-3, 3)
                ])
            )
            points.add(point)
        
        # Create lines between nearby points
        lines = VGroup()
        max_distance = 2.0  # Maximum distance for connecting points
        
        def update_lines(lines):
            lines.become(VGroup())
            for i in range(len(points)):
                for j in range(i + 1, len(points)):
                    distance = np.linalg.norm(
                        points[i].get_center() - points[j].get_center()
                    )
                    if distance < max_distance:
                        opacity = 1 - (distance / max_distance) ** 0.5
                        line = Line(
                            points[i].get_center(),
                            points[j].get_center(),
                            stroke_width=2,
                            stroke_opacity=opacity
                        ).set_color(BLUE_A)
                        lines.add(line)
        
        # Add movement to points
        def move_points(points, dt):
            for point in points:
                # Add small random movement
                point.shift(
                    np.array([
                        np.random.uniform(-0.02, 0.02),
                        np.random.uniform(-0.02, 0.02),
                        np.random.uniform(-0.02, 0.02)
                    ])
                )
                
                # Keep points within bounds
                pos = point.get_center()
                for i in range(3):
                    if abs(pos[i]) > 3:
                        pos[i] *= -0.95
                point.move_to(pos)
                
                # Rotate the point to give 3D appearance
                point.rotate(
                    about_point=point.get_center(),
                    angle=0.1 * dt,
                    axis=UP
                )
        
        # Add camera rotation
        frame.add_updater(
            lambda m, dt: m.increment_theta(0.1 * dt)
        )
        
        # Add continuous updates
        points.add_updater(move_points)
        lines.add_updater(lambda m: update_lines(m))
        
        # Add axes for reference
        axes = ThreeDAxes()
        
        # Animation sequence
        self.play(
            ShowCreation(axes),
            ShowCreation(points),
            run_time=2
        )
        self.add(lines)
        
        # Let it run
        self.wait(30) 