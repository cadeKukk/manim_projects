from manimlib import *
import numpy as np
from itertools import combinations

class FruitEmbeddingVisualization(ThreeDScene):
    def construct(self):
        # Set up the 3D axes with similar range
        axes = ThreeDAxes(
            x_range=(-6, 6),
            y_range=(-6, 6),
            z_range=(-6, 6),
            axis_config={
                "include_tip": True,
                "include_numbers": False
            }
        )
        
        # Define positions (arranged by sweetness, size, and water content)
        positions = {
            'fruit': np.array([0, 0, 0]),
            'apple': np.array([1, 0.5, 1]),
            'banana': np.array([-0.5, 1, 0.5]),
            'watermelon': np.array([4, -3, 2]),
            'orange': np.array([0.8, -0.7, 0.9]),
            'grape': np.array([0.3, -1.2, 0.4]),
            'strawberry': np.array([0.5, -0.9, 0.6]),
            'mango': np.array([-0.8, 0.4, 2.0]),
            'pineapple': np.array([-0.4, 0.2, 1.8]),
            'peach': np.array([-0.6, 0.3, 1.9]),
            'lemon': np.array([0.2, 0.8, -1.5]),
            'lime': np.array([0.4, 0.6, -1.0]),
            'coconut': np.array([3, -2, -2]),
            'kiwi': np.array([-2, -1.5, -1]),
            'pear': np.array([-1.5, -1, -0.8]),
            'blueberry': np.array([1.5, -1.2, 1.2])
        }
        
        # Colors for different fruits
        colors = {
            'fruit': GREEN,
            'apple': RED,
            'banana': YELLOW,
            'watermelon': PINK,
            'orange': ORANGE,
            'grape': PURPLE,
            'strawberry': RED_A,
            'mango': GOLD,
            'pineapple': YELLOW_A,
            'peach': GOLD_A,
            'lemon': YELLOW_B,
            'lime': GREEN_A,
            'coconut': WHITE,
            'kiwi': GREEN_D,
            'pear': GREEN_B,
            'blueberry': BLUE
        }
        
        # Create points and labels
        points = {}
        labels = {}
        all_point_animations = []
        all_label_animations = []
        
        for fruit, pos in positions.items():
            points[fruit] = Sphere(radius=0.1).set_color(colors[fruit]).move_to(pos)
            label_text = f"{fruit.upper()}"
            labels[fruit] = Text(label_text, weight=BOLD).scale(0.4).next_to(points[fruit], RIGHT + UP)
            labels[fruit].rotate(90 * DEGREES, axis=RIGHT)
            
            all_point_animations.append(ShowCreation(points[fruit]))
            all_label_animations.append(Write(labels[fruit]))
        
        # Create all lines at once
        lines = {}
        fruit_lines = {}
        other_lines = {}
        all_fruits = sorted(list(positions.keys()))
        all_line_animations = []
        
        for f1, f2 in combinations(all_fruits, 2):
            key = f"{min(f1, f2)}_{max(f1, f2)}"
            if 'fruit' in [f1, f2]:
                fruit_lines[key] = Line(
                    start=positions[f1],
                    end=positions[f2],
                    stroke_opacity=0.3
                ).set_color(GREEN_C)
                all_line_animations.append(ShowCreation(fruit_lines[key]))
            else:
                other_lines[key] = Line(
                    start=positions[f1],
                    end=positions[f2],
                    stroke_opacity=0.3
                ).set_color(ORANGE)
                all_line_animations.append(ShowCreation(other_lines[key]))
        
        lines = {**fruit_lines, **other_lines}
        
        # Camera setup
        frame = self.camera.frame
        frame.set_euler_angles(
            theta=30 * DEGREES,
            phi=75 * DEGREES
        )
        frame.move_to(OUT * 2)
        frame.scale(1.5)
        
        frame.add_updater(
            lambda m, dt: m.increment_theta(0.2 * dt)
        )
        
        # Show initial configuration
        self.play(ShowCreation(axes))
        self.play(
            *all_point_animations,
            *all_label_animations,
            *all_line_animations,
            run_time=2
        )
        
        # Wait before moving nodes
        self.wait(5)
        
        # New position for apple
        new_apple_pos = np.array([3, 2, 3])
        
        # Move apple node and its label
        self.play(
            points['apple'].animate.move_to(new_apple_pos),
            labels['apple'].animate.next_to(new_apple_pos, RIGHT + UP),
            run_time=1.5
        )
        
        # Wait 5 seconds
        self.wait(5)
        
        # Calculate new positions for other fruits based on apple's movement
        displacement = new_apple_pos - positions['apple']
        scale_factor = 2.0  # Doubled from 1.0 to 2.0
        
        # Create animations for updating other nodes
        node_animations = []
        label_animations = []
        line_animations = []
        glow_animations = []
        
        # Keep track of new positions
        new_positions = positions.copy()
        new_positions['apple'] = new_apple_pos
        
        # Calculate connection weights for all nodes
        connection_weights = {}
        for fruit in positions.keys():
            connection_weights[fruit] = 0
            for key in lines.keys():
                if fruit in key:
                    connection_weights[fruit] += 1
        
        # First calculate all new positions based on network connections
        for fruit, pos in positions.items():
            if fruit != 'apple' and fruit != 'fruit':
                # Check direct connection to apple
                apple_connection = f"{min('apple', fruit)}_{max('apple', fruit)}"
                is_connected_to_apple = apple_connection in lines
                
                # Calculate weighted influence based on all connections
                total_weight = max(connection_weights[fruit], 1)
                apple_weight = 6 if is_connected_to_apple else 0  # Doubled from 3 to 6
                
                # Calculate distance to apple
                distance = np.linalg.norm(pos - positions['apple'])
                
                # Calculate influence based on connections and distance
                if is_connected_to_apple:
                    # Connected nodes are influenced more strongly
                    influence = (apple_weight / total_weight) * (1 / (1 + distance * 0.3))  # Reduced distance dampening
                    
                    # Add glow effect for connected nodes
                    glow = Sphere(radius=0.15).move_to(pos)
                    glow.set_color(YELLOW)
                    glow.set_opacity(0.3)
                    glow_animations.extend([
                        FadeIn(glow, run_time=1),
                        FadeOut(glow, run_time=3)
                    ])
                else:
                    # Increased minimal influence for unconnected nodes
                    influence = 0.2 / (1 + distance)  # Doubled from 0.1 to 0.2
                
                # New position based on apple's movement
                new_positions[fruit] = pos + displacement * influence * scale_factor
                
                # Add animations for nodes and labels
                node_animations.append(points[fruit].animate.move_to(new_positions[fruit]))
                label_animations.append(labels[fruit].animate.next_to(new_positions[fruit], RIGHT + UP))
        
        # Update all connecting lines using the new positions
        for key, line in lines.items():
            f1, f2 = key.split('_')
            start_pos = new_positions[f1]
            end_pos = new_positions[f2]
            line_animations.append(line.animate.put_start_and_end_on(start_pos, end_pos))
        
        # Play all update animations together with longer duration
        self.play(
            *node_animations,
            *label_animations,
            *line_animations,
            *glow_animations,
            run_time=4  # Increased animation duration
        )
        
        # Let it rotate for the remaining time
        self.wait(30)