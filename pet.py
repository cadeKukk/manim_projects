from manimlib import *
import numpy as np
from itertools import combinations

class WordEmbeddingVisualization(ThreeDScene):
    def construct(self):
        # Set up the 3D axes with wider range
        axes = ThreeDAxes(
            x_range=(-6, 6),
            y_range=(-6, 6),
            z_range=(-6, 6),
            axis_config={
                "include_tip": True,
                "include_numbers": False
            }
        )
        
        # Define all positions
        positions = {
            'pet': np.array([0, 0, 0]),
            'cat': np.array([1, 0.5, 1.5]),
            'dog': np.array([-0.5, 1, 0.5]),
            'cow': np.array([4, -3, -3]),
            'rabbit': np.array([0.8, -0.7, 0.9]),
            'hamster': np.array([0.3, -1.2, 0.4]),
            'guinea_pig': np.array([0.5, -0.9, 0.6]),
            'parrot': np.array([-0.8, 0.4, 2.0]),
            'canary': np.array([-0.4, 0.2, 1.8]),
            'parakeet': np.array([-0.6, 0.3, 1.9]),
            'fish': np.array([0.2, 0.8, -1.5]),
            'turtle': np.array([0.4, 0.6, -1.0]),
            'horse': np.array([3, -2, -2]),
            'snake': np.array([-2, -1.5, -1]),
            'lizard': np.array([-1.5, -1, -0.8]),
            'squirrel': np.array([1.5, -1.2, 1.2])
        }
        
        # Colors for different animal types
        colors = {
            'pet': GREEN,
            'cat': BLUE,
            'dog': RED,
            'cow': PURPLE,
            'rabbit': PINK,
            'hamster': GOLD,
            'guinea_pig': ORANGE,
            'parrot': YELLOW,
            'canary': YELLOW_A,
            'parakeet': YELLOW_B,
            'fish': BLUE_A,
            'turtle': GREEN_A,
            'horse': PURPLE_A,
            'snake': RED_A,
            'lizard': RED_B,
            'squirrel': GOLD_A
        }
        
        # Create points and labels
        points = {}
        labels = {}
        
        for animal, pos in positions.items():
            points[animal] = Sphere(radius=0.1).set_color(colors[animal]).move_to(pos)
            
            # Just the animal name without coordinates
            label_text = f"{animal.upper()}"
            labels[animal] = Text(label_text, weight=BOLD).scale(0.4).next_to(points[animal], RIGHT + UP)
            labels[animal].rotate(90 * DEGREES, axis=RIGHT)
        
        # Create all connecting lines
        lines = {}
        pet_lines = {}  # Separate dictionary for pet connections
        other_lines = {}  # Separate dictionary for other connections
        all_animals = sorted(list(positions.keys()))
        
        for a1, a2 in combinations(all_animals, 2):
            key = f"{min(a1, a2)}_{max(a1, a2)}"
            if 'pet' in [a1, a2]:
                # Pet connections in blue
                pet_lines[key] = Line(
                    start=positions[a1],
                    end=positions[a2],
                    stroke_opacity=0.3
                ).set_color(BLUE_C)
            else:
                # Other connections in yellow (to be shown later)
                other_lines[key] = Line(
                    start=positions[a1],
                    end=positions[a2],
                    stroke_opacity=0.3
                ).set_color(YELLOW)
        
        # Combine all lines for easier reference
        lines = {**pet_lines, **other_lines}
        
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
        
        # Initial animations
        self.play(ShowCreation(axes))
        
        # Initial elements (cat, dog, pet, cow)
        initial_animals = ['cat', 'dog', 'pet', 'cow']
        self.play(*[ShowCreation(points[a]) for a in initial_animals],
                 *[Write(labels[a]) for a in initial_animals])
        
        # Initial connections (only pet connections)
        initial_connections = ['dog_pet', 'cat_pet', 'cow_pet']
        self.play(*[ShowCreation(lines[conn]) for conn in initial_connections])
        
        # Wait 10 seconds
        self.wait(10)
        
        # Add rabbit with slower timing (but 25% faster than previous)
        self.wait(3)  # Changed from 4 to 3
        self.play(
            ShowCreation(points['rabbit']),
            Write(labels['rabbit']),
            run_time=1.5  # Changed from 2 to 1.5
        )
        
        # Add rabbit-pet connection
        pet_connection = f"{min('rabbit', 'pet')}_{max('rabbit', 'pet')}"
        self.play(ShowCreation(lines[pet_connection]), run_time=1.5)  # Changed from 2 to 1.5
        
        # Add remaining animals one by one with adjusted timing
        remaining_animals = [a for a in all_animals 
                           if a not in initial_animals + ['rabbit']]
        
        for animal in remaining_animals:
            # Adjusted wait time between animals
            self.wait(3)  # Changed from 4 to 3
            
            # Adjusted animation time for each animal
            self.play(
                ShowCreation(points[animal]),
                Write(labels[animal]),
                run_time=1.5  # Changed from 2 to 1.5
            )
            
            # Adjusted animation time for pet connections
            pet_connection = f"{min(animal, 'pet')}_{max(animal, 'pet')}"
            self.play(ShowCreation(lines[pet_connection]), run_time=1.5)  # Changed from 2 to 1.5
        
        # Wait until 50 seconds have passed
        self.wait(50 - self.time)
        
        # Show all other (yellow) connections
        other_connections = list(other_lines.keys())
        for i in range(0, len(other_connections), 10):
            group = other_connections[i:i+10]
            self.play(*[ShowCreation(lines[conn]) for conn in group], run_time=0.5)
        
        # Let the scene rotate indefinitely
        self.wait(30)