from manimlib import *
import numpy as np
from scipy.integrate import odeint

class LorenzAttractor(Scene):
    def construct(self):
        # Set up the camera
        frame = self.camera.frame
        frame.set_euler_angles(
            theta=30 * DEGREES,
            phi=75 * DEGREES,
        )
        frame.scale(0.75)
        frame.shift(UP * 2)
        
        # Lorenz system parameters
        sigma, rho, beta = 10, 28, 8/3
        
        # Time points (increased points for smoother animation)
        t = np.linspace(0, 50, 20000)
        
        # Initial conditions
        initial_state = [1, 1, 1]
        
        # Lorenz system differential equations
        def lorenz(state, t):
            x, y, z = state
            dx = sigma * (y - x)
            dy = x * (rho - z) - y
            dz = x * y - beta * z
            return [dx, dy, dz]
        
        # Solve the system
        solution = odeint(lorenz, initial_state, t)
        
        # Create the curve with color gradient
        curve = VMobject()
        points = [np.array([x/10, y/10, z/10]) for x, y, z in solution]
        curve.set_points_smoothly(points)
        
        # Set color gradient from BLUE_A to PURPLE
        curve.set_color_by_gradient(BLUE_A, PURPLE)
        curve.set_stroke(width=3)
        
        # Start camera rotation
        frame.add_updater(
            lambda m, dt: m.increment_theta(0.05 * dt)  # Slower rotation
        )
        
        # Add axes with smaller numbers
        axes = ThreeDAxes(
            x_range=(-3, 3, 1),
            y_range=(-3, 3, 1),
            z_range=(-3, 3, 1),
            axis_config={
                "include_tip": True,
                "include_ticks": True,
                "line_to_number_buff": SMALL_BUFF,
                "decimal_number_config": {
                    "num_decimal_places": 0,
                    "font_size": 16,  # Smaller font size for axis numbers
                },
            }
        )
        axes.scale(3)
        
        # Create dynamic labels that follow the axes
        def create_dynamic_labels():
            labels = VGroup()
            for axis in [axes.x_axis, axes.y_axis, axes.z_axis]:
                for number in range(-3, 4):
                    if number != 0:  # Skip zero
                        label = Text(str(number), font_size=48)  # Doubled from 24 to 48
                        label.scale(0.8)  # Doubled from 0.4 to 0.8
                        # Create updater for each label
                        def update_label(mob, axis=axis, number=number):
                            point = axis.n2p(number)
                            offset = np.array([0.4, 0.4, 0])  # Doubled offset for larger numbers
                            mob.move_to(point + offset)
                        label.add_updater(update_label)
                        labels.add(label)
            return labels
        
        # Create axis labels that follow the axes
        x_label = Text("X", font_size=64).scale(1.0)  # Doubled size
        y_label = Text("Y", font_size=64).scale(1.0)
        z_label = Text("Z", font_size=64).scale(1.0)
        
        def update_x_label(mob):
            mob.next_to(axes.x_axis.get_end(), RIGHT, buff=0.6)  # Doubled buffer
        def update_y_label(mob):
            mob.next_to(axes.y_axis.get_end(), UP, buff=0.6)
        def update_z_label(mob):
            mob.next_to(axes.z_axis.get_end(), OUT+UP, buff=0.6)
            
        x_label.add_updater(update_x_label)
        y_label.add_updater(update_y_label)
        z_label.add_updater(update_z_label)
        
        # Create and add the dynamic labels
        number_labels = create_dynamic_labels()
        axis_labels = VGroup(x_label, y_label, z_label)
        
        # Animation sequence
        self.play(ShowCreation(axes))
        self.add(number_labels, axis_labels)
        self.wait()
        
        # Animate the curve creation (longer duration)
        self.play(ShowCreation(curve), run_time=40, rate_func=linear)
        
        # Keep rotating for longer
        self.wait(20)