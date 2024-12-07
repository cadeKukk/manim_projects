from manimlib import *
import numpy as np

class PixelToInputLayerMapping(Scene):
    def construct(self):
        # Create the pixel grid for a digit (e.g., "7")
        digit = self.create_mnist_digit()
        digit.scale(2).move_to(LEFT * 3)
        self.play(FadeIn(digit))
        self.wait(1)

        # Zoom out to fit the entire vertical strip of pixels
        self.camera.frame.scale(1.5)
        self.camera.frame.move_to(UP * 6)
        
        # Pan to the right 35% after panning up
        self.camera.frame.shift(RIGHT * 8)

        # Animate pixel to a more condensed linear arrangement
        condensed_positions = [UP * (i * 0.02) for i in range(28 * 28)]
        self.play(*[pixel.animate.move_to(condensed_positions[i]) for i, pixel in enumerate(digit)], run_time=2)

        self.wait(1)

        # Create a neural network layer representation
        neural_layer = self.create_neural_layer()
        self.play(FadeIn(neural_layer))

        # Connect pixels to the neural network layer
        self.connect_pixels_to_layer(digit, neural_layer)

        # After your animations, clear the scene
        self.clear_scene()

    def create_mnist_digit(self):
        # Create a simplified "7" digit
        pixel_array = np.zeros((28, 28))
        # Draw a "7" shape
        pixel_array[5:8, 5:20] = 1  # Top horizontal line
        pixel_array[7:20, 15:18] = 1  # Vertical line

        digit = VGroup()
        for i in range(28):
            for j in range(28):
                opacity = float(pixel_array[i][j])  # Convert to standard float
                square = Square(
                    side_length=0.1,
                    fill_opacity=opacity,
                    fill_color=BLUE_A,
                    stroke_width=0.5,
                    stroke_opacity=0.3
                )
                square.move_to([0.1 * i, 0.1 * j, 0])
                digit.add(square)
        return digit

    def create_neural_layer(self):
        # Create a simple neural network layer representation
        layer = VGroup()
        for i in range(10):  # Example: 10 neurons
            neuron = Circle(
                radius=0.12,
                fill_color=BLUE_A,  # Match the theme color
                fill_opacity=0.5,   # Adjust opacity to match theme
                stroke_color=BLUE_A,  # Set stroke color to match the fill color
                stroke_width=0       # Set stroke width to 0 to remove outlines
            )
            neuron.move_to(RIGHT * 3 + UP * (i * 0.5 - 2.25 + 6))  # Adjusted Y position
            layer.add(neuron)
        return layer

    def connect_pixels_to_layer(self, digit, neural_layer):
        # Create a list to hold connection lines
        connection_lines = []
        
        # Get the number of neurons and pixels
        num_neurons = len(neural_layer)
        num_pixels = len(digit)

        # Connect each pixel to a corresponding neuron
        for i in range(num_pixels):
            pixel = digit[i]
            neuron = neural_layer[i % num_neurons]  # Cycle through neurons if there are more pixels than neurons
            line = Line(pixel.get_center(), neuron.get_center(), color=BLUE_A)  # Set color to match NurNet
            connection_lines.append(line)  # Add line to the list
        
        # Add all lines to the scene and animate them together
        self.play(*[ShowCreation(line) for line in connection_lines], run_time=2)  # Animate all connections over 2 seconds

        # Fade out all connection lines with a longer duration
        self.play(*[FadeOut(line) for line in connection_lines], run_time=5)  # Fade out connections over 5 seconds

    def clear_scene(self):
        # Filter to get only valid Mobject instances
        valid_mobjects = [mob for mob in self.mobjects if isinstance(mob, Mobject)]
        
        if valid_mobjects:  # Check if there are any valid mobjects to fade out
            self.play(
                *[FadeOut(mob) for mob in valid_mobjects],  # Fade out only valid mobjects
                run_time=1  # Duration of the fade out
            )
