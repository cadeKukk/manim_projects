from manimlib import *
import numpy as np

class ThreeBodyProblem(Scene):
    def construct(self):
        # Set up parameters
        dt = 0.01
        t_max = 40  # Longer time to show full evolution
        G = 0.5  # Gravitational constant

        # Initial positions - equilateral triangle
        r1 = np.array([-1.0, 0.0, 0.0])
        r2 = np.array([0.5, 0.866, 0.0])  # cos(60°), sin(60°)
        r3 = np.array([0.5, -0.866, 0.0])  # cos(60°), -sin(60°)

        # Initial velocities - tangential for orbital motion
        speed = 0.35  # Orbital speed
        v1 = np.array([0.1, -speed, 0.0])
        v2 = np.array([-speed*0.866, 0.1, 0.0])
        v3 = np.array([speed*0.866, 0.1, 0.0])

        # Equal masses for more stable initial orbits
        m1, m2, m3 = 1.0, 1.0, 1.0

        # Create bodies and trails
        body1 = Dot(point=r1, color=RED).scale(1.5)
        body2 = Dot(point=r2, color=BLUE).scale(1.5)
        body3 = Dot(point=r3, color=GREEN).scale(1.5)

        trail1 = VMobject(color=RED, stroke_opacity=0.8)
        trail2 = VMobject(color=BLUE, stroke_opacity=0.8)
        trail3 = VMobject(color=GREEN, stroke_opacity=0.8)

        # Create text that we'll transform to later
        text = Text(
            "THE THREE BODY PROBLEM",
            color=WHITE,
            weight=BOLD   # Make text bold
        ).scale(1.2)     # Make text slightly larger
        
        # Create underline
        underline = Line(
            text.get_left() + DOWN * 0.3,  # Slightly below text
            text.get_right() + DOWN * 0.3,
            color=WHITE
        )
        
        # Group all objects that will transform
        bodies_group = VGroup(body1, body2, body3, trail1, trail2, trail3)

        # Add everything to the scene
        self.add(bodies_group)

        # Keep track of trail points
        trail1_points = []
        trail2_points = []
        trail3_points = []
        max_points = 50  # Adjust this to control trail length

        def update_position(mob, dt):
            nonlocal r1, r2, r3, v1, v2, v3, trail1_points, trail2_points, trail3_points

            # Calculate distances
            r12 = r2 - r1
            r13 = r3 - r1
            r23 = r3 - r2

            # Calculate forces with distance protection to prevent extreme accelerations
            dist12 = max(np.linalg.norm(r12), 0.1)
            dist13 = max(np.linalg.norm(r13), 0.1)
            dist23 = max(np.linalg.norm(r23), 0.1)

            F12 = G * m1 * m2 * r12 / dist12**3
            F13 = G * m1 * m3 * r13 / dist13**3
            F23 = G * m2 * m3 * r23 / dist23**3

            # Update velocities
            v1 += dt * (F12 + F13) / m1
            v2 += dt * (-F12 + F23) / m2
            v3 += dt * (-F13 - F23) / m3

            # Gradually increasing drag to cause eventual destabilization
            # Start with almost no drag, increase over time
            time_passed = self.time
            drag = 1.0 - 0.0001 * (time_passed ** 2)  # Quadratic decay
            
            # Update velocities with drag
            v1 *= drag
            v2 *= drag
            v3 *= drag

            # Update positions
            r1 += dt * v1
            r2 += dt * v2
            r3 += dt * v3

            # Update dots
            body1.move_to(r1)
            body2.move_to(r2)
            body3.move_to(r3)

            # Update trail points
            trail1_points.append(np.array(body1.get_center()))
            trail2_points.append(np.array(body2.get_center()))
            trail3_points.append(np.array(body3.get_center()))

            # Limit number of points
            if len(trail1_points) > max_points:
                trail1_points = trail1_points[-max_points:]
                trail2_points = trail2_points[-max_points:]
                trail3_points = trail3_points[-max_points:]

            # Update trails
            if len(trail1_points) > 1:
                trail1.become(VMobject().set_points_smoothly(trail1_points))
                trail2.become(VMobject().set_points_smoothly(trail2_points))
                trail3.become(VMobject().set_points_smoothly(trail3_points))

                # Maintain trail properties
                trail1.set_color(RED).set_stroke(opacity=0.8)
                trail2.set_color(BLUE).set_stroke(opacity=0.8)
                trail3.set_color(GREEN).set_stroke(opacity=0.8)

        # Add updater to one of the bodies
        body1.add_updater(update_position)

        # Wait for 10 seconds
        self.wait(10)

        # Remove the updater
        body1.clear_updaters()

        # Transform to text
        self.play(
            Transform(bodies_group, text),
            run_time=3.5
        )

        # Create and animate the underline using ShowCreation
        self.play(
            ShowCreation(underline),
            run_time=1.5  # Duration of underline animation
        )
        
        # Wait a moment with the underline visible
        self.wait(1)
        
        # Make the underline disappear from left to right (same direction)
        self.play(
            Uncreate(underline),  # Uncreate will remove it in the same direction
            run_time=1.5
        )

        # Wait a bit more to show the final result
        self.wait(2)

        # Wait a bit after the underline disappears
        self.wait(2)

        # Transform text back into the dot
        self.play(
            Transform(bodies_group, Dot(color=WHITE).scale(2.0).move_to(ORIGIN)),
            run_time=3.5
        )

        # Final pause to show the dot
        self.wait(2)

        # Create second dot and set up orbital motion
        dot1 = Dot(color=BLUE).scale(2.0)
        dot2 = Dot(color=RED).scale(2.0)
        center_dot = Dot(color=WHITE).scale(2.0).move_to(ORIGIN)
        center_dot.set_z_index(2)  # Ensure center dot stays on top
        
        # Create trails with specific z-index
        trail1 = VMobject(color=BLUE, stroke_opacity=0.8)
        trail2 = VMobject(color=RED, stroke_opacity=0.8).set_z_index(0)  # Red trail goes behind
        
        # Remove the final_dot and add our new center_dot
        self.remove(bodies_group)
        self.add(center_dot)
        
        # Initial positions and velocities
        radius = 2.0
        dot1.move_to(RIGHT * radius)
        dot2.move_to(LEFT * radius)
        
        # Keep track of trail points
        trail1_points = []
        trail2_points = []
        max_points = 50  # Length of trails

        def update_orbital_motion(mob, dt):
            nonlocal trail1_points, trail2_points
            
            # Update positions in circular motion
            time = self.time
            angle = time * 0.5  # Controls speed of rotation
            
            # Update dot positions
            dot1.move_to(np.array([
                radius * np.cos(angle),
                radius * np.sin(angle),
                0
            ]))
            dot2.move_to(np.array([
                -radius * np.cos(angle),
                -radius * np.sin(angle),
                0
            ]))
            
            # Update trails
            trail1_points.append(np.array(dot1.get_center()))
            trail2_points.append(np.array(dot2.get_center()))
            
            # Limit trail length
            if len(trail1_points) > max_points:
                trail1_points = trail1_points[-max_points:]
                trail2_points = trail2_points[-max_points:]
            
            # Update trail visuals
            if len(trail1_points) > 1:
                trail1.become(VMobject().set_points_smoothly(trail1_points))
                trail2.become(VMobject().set_points_smoothly(trail2_points))
                
                trail1.set_color(BLUE).set_stroke(opacity=0.8)
                trail2.set_color(RED).set_stroke(opacity=0.8)

        # Add everything to scene
        self.add(dot1, dot2, trail1, trail2)
        dot1.add_updater(update_orbital_motion)
        
        # Let the orbital motion run for a while
        self.wait(5)  # Initial simple orbital motion

        def update_complex_motion(mob, dt):
            nonlocal trail1_points, trail2_points
            time = self.time
            
            # Center point motion
            center_x = np.sin(time * 0.3) * 1.0  # Slower, gentler center motion
            center_y = np.cos(time * 0.2) * 0.8
            
            # Primary orbit parameters
            base_radius = 2.0
            orbit_speed = 0.5
            
            # Create more complex orbits using multiple sinusoidal components
            dot1.move_to(np.array([
                center_x + base_radius * np.cos(time * orbit_speed) + 0.5 * np.sin(time * 0.8),
                center_y + base_radius * np.sin(time * orbit_speed) + 0.5 * np.cos(time * 0.8),
                0
            ]))
            
            dot2.move_to(np.array([
                center_x + base_radius * np.cos(time * orbit_speed + PI) * 0.8 + 0.7 * np.sin(time * 0.6),
                center_y + base_radius * np.sin(time * orbit_speed + PI) * 0.8 + 0.7 * np.cos(time * 0.6),
                0
            ]))
            
            # Update trails
            trail1_points.append(np.array(dot1.get_center()))
            trail2_points.append(np.array(dot2.get_center()))
            
            # Limit trail length
            if len(trail1_points) > max_points:
                trail1_points = trail1_points[-max_points:]
                trail2_points = trail2_points[-max_points:]
            
            # Update trail visuals
            if len(trail1_points) > 1:
                trail1.become(VMobject().set_points_smoothly(trail1_points))
                trail2.become(VMobject().set_points_smoothly(trail2_points))
                
                trail1.set_color(BLUE).set_stroke(opacity=0.8)
                trail2.set_color(RED).set_stroke(opacity=0.8)

        # Switch updaters smoothly
        dot1.clear_updaters()
        dot1.add_updater(update_complex_motion)
        
        # Let the complex motion run longer
        self.wait(20)  # Initial complex motion duration
        
        # Continue with the same motion for 20 more seconds
        self.wait(20)  # Additional duration with same pattern

        # Final cleanup
        dot1.clear_updaters()
