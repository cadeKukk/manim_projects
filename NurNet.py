from manimlib import *
import numpy as np
from scipy.ndimage import gaussian_filter
from manimlib.constants import BOLD

class NeuralNetworkScene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layers = [784, 16, 16, 10]
        self.current_probs = [0.1] * 10
        self.connections_group = None
        self.bars_group = VGroup()

    def construct(self):
        # Configuration
        self.camera.background_color = "#000000"
        # Zoom out by 20% total (1.15 * 1.05)
        self.camera.frame.scale(1.20)
        # Move 5% to the right
        self.camera.frame.shift(RIGHT * 0.5)
        
        # Create network first
        network, self.connections_group = self.create_neural_network(self.layers)
        network.shift(LEFT * 2)
        
        # First sequence (7)
        digit = self.create_mnist_digit()
        digit.scale(2).move_to(LEFT * 5)
        self.play(FadeIn(digit))
        self.wait(2)
        
        # Update input layer and show network with more deliberate timing
        self.update_input_layer(network, digit)
        self.play(ShowCreation(network, run_time=3))
        self.wait(2.5)
        
        # Continue with first animation (7)
        self.current_probs = [0.05, 0.02, 0.03, 0.05, 0.02, 0.02, 0.05, 0.70, 0.04, 0.02]
        probabilities = self.create_probability_bars(network)
        self.animate_network_flow(network)
        self.animate_bars(probabilities, highlight_index=7)
        self.wait(2)
        
        # Clean up first sequence
        self.play(
            FadeOut(digit),
            *[FadeOut(bar) for bar in probabilities],
            *[FadeOut(label) for label in self.bars_group]
        )
        
        # Reset network for second sequence
        self.play(
            *[neuron.animate.set_fill(opacity=0.2) for layer in network for neuron in layer if isinstance(neuron, Circle)],
            *[connection.animate.set_stroke(opacity=0.1) for connections in self.connections_group for connection in connections]
        )
        
        # Second sequence (3)
        digit_3 = self.create_mnist_digit_3()
        self.update_input_layer(network, digit_3)
        digit_3.scale(2).move_to(LEFT * 5)
        self.play(FadeIn(digit_3))
        
        # Second animation (3)
        self.current_probs = [0.05, 0.02, 0.03, 0.65, 0.02, 0.02, 0.05, 0.10, 0.04, 0.02]
        probabilities = self.create_probability_bars(network)
        self.animate_network_flow(network)
        self.animate_bars(probabilities, highlight_index=3)
        self.wait(2)
        
        # Clean up second sequence
        self.play(
            FadeOut(digit_3),
            *[FadeOut(bar) for bar in probabilities],
            *[FadeOut(label) for label in self.bars_group]
        )
        
        # Reset network for third sequence
        self.play(
            *[neuron.animate.set_fill(opacity=0.2) for layer in network for neuron in layer if isinstance(neuron, Circle)],
            *[connection.animate.set_stroke(opacity=0.1) for connections in self.connections_group for connection in connections]
        )
        
        # Third sequence (5)
        digit_5 = self.create_mnist_digit_5()
        self.update_input_layer(network, digit_5)
        digit_5.scale(2).move_to(LEFT * 5)
        self.play(FadeIn(digit_5))
        
        # Third animation (5)
        self.current_probs = [0.05, 0.02, 0.03, 0.05, 0.02, 0.65, 0.05, 0.10, 0.02, 0.01]
        probabilities = self.create_probability_bars(network)
        self.animate_network_flow(network)
        self.animate_bars(probabilities, highlight_index=5)
        
        # Get the output layer and filter for neurons only
        output_neurons = [n for n in network[-1] if isinstance(n, Circle)]
        print(f"Number of output neurons: {len(output_neurons)}")  # Debug line
        
        highlight_box = Square(side_length=0.3, color=BLUE_A)
        # Make sure we're accessing a valid index (5 should be the 6th neuron, 0-based indexing)
        if len(output_neurons) > 5:
            highlight_box.move_to(output_neurons[5])
            self.play(ShowCreation(highlight_box))
        else:
            print(f"Error: Not enough neurons in output layer. Only found {len(output_neurons)}")
        
        # Keep final scene on screen (don't fade anything out)
        self.wait(3)
        
        # Remove highlight box immediately after creation (if it exists)
        if 'highlight_box' in locals():
            self.remove(highlight_box)
        
        # Clean up third sequence (5) - with immediate removal
        self.play(
            FadeOut(digit_5),
            *[FadeOut(bar) for bar in probabilities],
            *[FadeOut(label) for label in self.bars_group]
        )
        
        # Force remove ALL squares except network components
        for mob in list(self.mobjects):  # Use list to create a copy
            if isinstance(mob, Square):
                if not any(mob in layer for layer in network):
                    self.remove(mob)
                
        # Brief pause to ensure clean state
        self.wait(0.1)
        
        # Reset network for fourth sequence (9)
        self.play(
            *[neuron.animate.set_fill(opacity=0.2) for layer in network for neuron in layer if isinstance(neuron, Circle)],
            *[connection.animate.set_stroke(opacity=0.1) for connections in self.connections_group for connection in connections]
        )
        
        # Fourth sequence (9)
        digit_9 = self.create_mnist_digit_9()
        self.update_input_layer(network, digit_9)
        digit_9.scale(2).move_to(LEFT * 5)
        self.play(FadeIn(digit_9))
        
        # Fourth animation (9)
        self.current_probs = [0.02, 0.03, 0.04, 0.05, 0.02, 0.03, 0.55, 0.06, 0.05, 0.65]
        probabilities = self.create_probability_bars(network)
        self.animate_network_flow(network)
        self.animate_bars(probabilities, highlight_index=9)
        
        # Get the output layer and filter for neurons only
        output_neurons = [n for n in network[-1] if isinstance(n, Circle)]
        
        # Create highlight box for the number 9 with yellow color
        highlight_box = Square(
            side_length=0.3,
            color=YELLOW,
            stroke_width=2
        )
        
        # Highlight the neuron for 9 (last neuron in output layer)
        if len(output_neurons) > 9:
            # Move box to the 9 neuron position
            highlight_box.move_to(output_neurons[9])
            # Make the neuron glow yellow
            self.play(
                ShowCreation(highlight_box),
                output_neurons[9].animate.set_fill(YELLOW, opacity=0.8)
            )
        
        # Final wait
        self.wait(2)
        
        # Add highlight for number 9 at the end
        highlight_9 = self.highlight_output_number(network, 9)
        self.play(FadeIn(highlight_9, run_time=0.6))
        self.wait(8)  # Wait 8 seconds
        
        # Fade out the 9 highlight
        self.play(FadeOut(highlight_9, run_time=0.6))
        
        # Add highlight for number 6
        highlight_6 = self.highlight_output_number(network, 6)
        self.play(FadeIn(highlight_6, run_time=0.6))
        self.wait(12)  # Increased from 8 to 12 seconds for final highlight
        
        # Fade out the 6 highlight
        self.play(FadeOut(highlight_6, run_time=0.6))
        self.wait(1)  # Final brief pause

    def animate_network_flow(self, network):
        for layer_idx in range(len(self.layers) - 1):
            current_layer = network[layer_idx]
            next_layer = network[layer_idx + 1]
            
            # For the last layer, use current probabilities
            if layer_idx == len(self.layers) - 2:
                activations = self.current_probs
            else:
                activations = np.random.rand(len([n for n in next_layer if isinstance(n, Circle)]))
            
            # Single animation for connections and neurons
            self.play(
                *[connection.animate.set_stroke(color=BLUE_D, opacity=0.8, width=2)
                  for connection in self.connections_group[layer_idx]],
                *[neuron.animate.set_fill(color=BLUE_A, opacity=activation)
                  for neuron, activation in zip([n for n in next_layer if isinstance(n, Circle)], activations)],
                run_time=0.8
            )
            
            # Fade connections only
            self.play(
                *[connection.animate.set_stroke(color=BLUE_A, opacity=0.1, width=1)
                  for connection in self.connections_group[layer_idx]],
                run_time=0.5
            )

    def animate_bars(self, probabilities, highlight_index):
        # Clear previous bars group
        self.bars_group = VGroup()
        
        # Animate each probability bar
        for i, (bar, prob) in enumerate(zip(probabilities, self.current_probs)):
            if i == highlight_index:
                bar.set_fill(BLUE_D, opacity=0.8)
                bar.set_stroke(BLUE_A, width=2)
            else:
                bar.set_fill(BLUE_A, opacity=0.3)
                bar.set_stroke(WHITE, width=1)
            
            self.play(
                bar.animate.set_width(prob * 3, stretch=True, about_edge=LEFT),
                run_time=0.3
            )
            
            label = Text(f"{prob:.2f}", font_size=16, 
                        color=WHITE if i != highlight_index else BLUE_D,
                        weight=BOLD)
            label.next_to(bar, RIGHT, buff=0.1)
            self.bars_group.add(label)
        
        self.play(FadeIn(self.bars_group))
    
    def create_mnist_digit(self):
        # Create a simplified "7" digit
        pixel_array = np.zeros((28, 28))
        # Draw a "7" shape
        pixel_array[5:8, 5:20] = 1  # Top horizontal line
        pixel_array[7:20, 15:18] = 1  # Vertical line
        
        digit = VGroup()
        for i in range(28):
            for j in range(28):
                opacity = pixel_array[i][j]
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
    
    def create_mnist_digit_3(self):
        pixel_array = np.zeros((28, 28))
        # Base "3" shape
        pixel_array[5:8, 5:20] = 1    # Top horizontal
        pixel_array[13:16, 5:20] = 1  # Middle horizontal
        pixel_array[21:24, 5:20] = 1  # Bottom horizontal
        pixel_array[5:24, 17:20] = 1  # Right vertical
        
        # Add random variations
        for i in range(28):
            for j in range(28):
                if pixel_array[i][j] == 1:
                    # Add random variation to lit pixels
                    pixel_array[i][j] = np.random.uniform(0.7, 1.0)
                else:
                    # Add some noise to dark areas
                    if np.random.random() < 0.1:  # 10% chance of noise
                        pixel_array[i][j] = np.random.uniform(0, 0.3)
        
        # Add some blur effect
        pixel_array = gaussian_filter(pixel_array, sigma=0.5)
        
        digit = VGroup()
        for i in range(28):
            for j in range(28):
                opacity = pixel_array[i][j]
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
    
    def create_mnist_digit_5(self):  # New method for creating a "5"
        pixel_array = np.zeros((28, 28))
        # Base "5" shape
        pixel_array[5:8, 5:20] = 1    # Top horizontal
        pixel_array[5:13, 5:8] = 1    # Left vertical (upper)
        pixel_array[13:16, 5:20] = 1  # Middle horizontal
        pixel_array[16:24, 17:20] = 1 # Right vertical (lower)
        pixel_array[21:24, 5:20] = 1  # Bottom horizontal
        
        # Add random variations
        for i in range(28):
            for j in range(28):
                if pixel_array[i][j] == 1:
                    pixel_array[i][j] = np.random.uniform(0.7, 1.0)
                else:
                    if np.random.random() < 0.1:
                        pixel_array[i][j] = np.random.uniform(0, 0.3)
        
        # Add blur effect
        pixel_array = gaussian_filter(pixel_array, sigma=0.5)
        
        digit = VGroup()
        for i in range(28):
            for j in range(28):
                opacity = pixel_array[i][j]
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
    
    def create_mnist_digit_9(self):  # New method for creating a "9"
        pixel_array = np.zeros((28, 28))
        # Base "9" shape
        pixel_array[5:8, 5:20] = 1     # Top horizontal
        pixel_array[5:13, 5:8] = 1     # Left vertical (upper)
        pixel_array[5:24, 17:20] = 1   # Right vertical
        pixel_array[13:16, 5:20] = 1   # Middle horizontal
        
        # Add random variations
        for i in range(28):
            for j in range(28):
                if pixel_array[i][j] == 1:
                    pixel_array[i][j] = np.random.uniform(0.7, 1.0)
                else:
                    if np.random.random() < 0.1:
                        pixel_array[i][j] = np.random.uniform(0, 0.3)
        
        # Add blur effect
        pixel_array = gaussian_filter(pixel_array, sigma=0.5)
        
        digit = VGroup()
        for i in range(28):
            for j in range(28):
                opacity = pixel_array[i][j]
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
    
    def create_neural_network(self, layers):
        network = VGroup()
        neurons = []
        connections_group = VGroup()
        
        # Create layers
        x_spacing = 2.5
        for i, n_neurons in enumerate(layers):
            layer = VGroup()
            y_spacing = 4.5 / min(n_neurons, 16)
            n_display = min(n_neurons, 16)
            
            for j in range(n_display):
                neuron = Circle(
                    radius=0.12,
                    fill_color=WHITE,
                    fill_opacity=0.2,  # Start dim
                    stroke_width=0
                )
                y_pos = (j - n_display/2) * y_spacing
                neuron.move_to([i * x_spacing, y_pos, 0])
                layer.add(neuron)
            
            neurons.append(layer)
            network.add(layer)
        
        # Create connections between layers
        for i in range(len(layers) - 1):
            layer_connections = VGroup()
            for n1 in neurons[i]:
                for n2 in neurons[i + 1]:
                    connection = Line(
                        n1.get_center(),
                        n2.get_center(),
                        stroke_opacity=0.1,  # Increased initial opacity
                        stroke_width=1,      # Increased line width
                        stroke_color=BLUE_A  # Changed color for better visibility
                    )
                    layer_connections.add(connection)
            connections_group.add(layer_connections)
        
        # Add output labels (0-9)
        for i, neuron in enumerate(neurons[-1]):
            label = Text(str(i).upper(), font_size=20, color=WHITE, weight=BOLD)
            label.next_to(neuron, RIGHT, buff=0.1)
            network.add(label)
        
        network.add(connections_group)
        return network, connections_group
    
    def create_probability_bars(self, network):
        bars = VGroup()
        output_layer = network[len(self.layers)-1]
        
        for i in range(10):
            bar = Rectangle(
                height=0.2,
                width=0.01,
                fill_color=WHITE,
                fill_opacity=0.8,
                stroke_color=WHITE,
                stroke_width=1
            )
            neuron = output_layer[i]
            # Position bar to the right of each output neuron
            bar.next_to(neuron, RIGHT, buff=0.5)
            # Set the transform_anchor to LEFT so it grows rightward only
            bar.generate_target()
            bar.target.set_width(0.01, stretch=True, about_edge=LEFT)
            bars.add(bar)
        return bars
    
    def highlight_output_number(self, network, number):
        output_layer = network[len(self.layers)-1]
        neuron = output_layer[number]
        
        # Find the label by position rather than direct indexing
        labels = [mob for mob in network 
                 if isinstance(mob, Text) and mob.get_center()[0] > neuron.get_center()[0]]
        label = [lab for lab in labels if lab.text == str(number)][0]
        
        # Create highlights
        neuron_highlight = neuron.copy()
        neuron_highlight.set_fill(YELLOW, opacity=0.8)
        neuron_highlight.set_stroke(YELLOW, width=2)
        
        label_highlight = Rectangle(
            width=label.get_width() + 0.1,
            height=label.get_height() + 0.1,
            stroke_color=YELLOW,
            stroke_width=2,
            fill_opacity=0
        ).move_to(label)
        
        return VGroup(neuron_highlight, label_highlight)
    
    def update_network_state(self, network, probabilities):
        # Update the final layer neurons directly to match current probabilities
        output_layer = network[len(self.layers)-1]
        for neuron, prob in zip([n for n in output_layer if isinstance(n, Circle)], probabilities):
            neuron.set_fill(opacity=prob)
    
    def animate_probabilities(self, network, probabilities):
        # Set probabilities for number 7
        self.current_probs = [0.05, 0.02, 0.03, 0.05, 0.02, 0.02, 0.05, 0.70, 0.04, 0.02]
        
        # Single network flow animation
        self.animate_network_flow(network, self.connections_group)
        
        # Single probability bars animation
        self.bars_group = VGroup()
        for i, (bar, prob) in enumerate(zip(probabilities, self.current_probs)):
            if i == 7:  # Highlight the 7
                bar.set_fill(BLUE_D, opacity=0.8)
                bar.set_stroke(BLUE_A, width=2)
            else:
                bar.set_fill(BLUE_A, opacity=0.3)
                bar.set_stroke(WHITE, width=1)
            
            self.play(
                bar.animate.set_width(prob * 3, stretch=True, about_edge=LEFT),
                run_time=0.3
            )
            
            label = Text(f"{prob:.2f}", font_size=16, color=WHITE if i != 7 else BLUE_D, weight=BOLD)
            label.next_to(bar, RIGHT, buff=0.1)
            self.bars_group.add(label)
        
        self.play(FadeIn(self.bars_group))
        
        highlight = self.highlight_output_number(network, 7)
        self.play(FadeIn(highlight, run_time=0.6))
        self.wait(1.2)
        self.play(FadeOut(highlight, run_time=0.6))
    
    def animate_probabilities_for_three(self, network, probabilities):
        # Set probabilities for number 3
        final_probs = [0.05, 0.02, 0.03, 0.65, 0.05, 0.02, 0.01, 0.10, 0.05, 0.02]
        self.current_probs = final_probs
        
        # Update network state first
        self.update_network_state(network, final_probs)
        
        # Then do network flow animation
        self.animate_network_flow(network, self.connections_group)
        
        self.bars_group = VGroup()
        for i, (bar, prob) in enumerate(zip(probabilities, final_probs)):
            if i == 3:  # Highlight the 3
                bar.set_fill(BLUE_D, opacity=0.8)
                bar.set_stroke(BLUE_A, width=2)
            else:
                bar.set_fill(BLUE_A, opacity=0.3)
                bar.set_stroke(WHITE, width=1)
            
            self.play(
                bar.animate.set_width(prob * 3, stretch=True, about_edge=LEFT),
                run_time=0.3
            )
            
            label = Text(f"{prob:.2f}", font_size=16, color=WHITE if i != 3 else BLUE_D, weight=BOLD)
            label.next_to(bar, RIGHT, buff=0.1)
            self.bars_group.add(label)
        
        self.play(FadeIn(self.bars_group))
        
        highlight = self.highlight_output_number(network, 3)
        self.play(FadeIn(highlight, run_time=0.6))
        self.wait(1.2)
        self.play(FadeOut(highlight, run_time=0.6))
    
    def animate_probabilities_for_five(self, network, probabilities):
        # Set probabilities for number 5
        final_probs = [0.05, 0.02, 0.03, 0.05, 0.02, 0.65, 0.01, 0.10, 0.05, 0.02]
        self.current_probs = final_probs
        
        # Update network state first
        self.update_network_state(network, final_probs)
        
        # Then do network flow animation
        self.animate_network_flow(network, self.connections_group)
        
        self.bars_group = VGroup()
        for i, (bar, prob) in enumerate(zip(probabilities, final_probs)):
            if i == 5:  # Highlight the 5
                bar.set_fill(BLUE_D, opacity=0.8)
                bar.set_stroke(BLUE_A, width=2)
            else:
                bar.set_fill(BLUE_A, opacity=0.3)
                bar.set_stroke(WHITE, width=1)
            
            self.play(
                bar.animate.set_width(prob * 3, stretch=True, about_edge=LEFT),
                run_time=0.3
            )
            
            label = Text(f"{prob:.2f}", font_size=16, color=WHITE if i != 5 else BLUE_D, weight=BOLD)
            label.next_to(bar, RIGHT, buff=0.1)
            self.bars_group.add(label)
        
        self.play(FadeIn(self.bars_group))
        
        highlight = self.highlight_output_number(network, 5)
        self.play(FadeIn(highlight, run_time=0.6))
        self.wait(1.2)
        self.play(FadeOut(highlight, run_time=0.6))
    
    def animate_pixel_mapping(self, digit, network):
        input_layer = network[0]
        
        # Create a grid to store all arrows
        arrows_matrix = []
        pixel_highlights = VGroup()
        
        # Select a few representative pixels to demonstrate the mapping
        selected_pixels = []
        for i in range(0, 28, 7):  # Take every 7th pixel to avoid overcrowding
            for j in range(0, 28, 7):
                pixel_idx = i * 28 + j
                pixel = digit[pixel_idx]
                if pixel.get_fill_opacity() > 0.1:
                    selected_pixels.append((pixel, pixel.get_fill_opacity()))
                    
                    # Highlight the selected pixel
                    pixel_highlight = pixel.copy()
                    pixel_highlight.set_stroke(YELLOW, width=2)
                    pixel_highlights.add(pixel_highlight)
                    
                    # Create arrows to first few input nodes
                    pixel_arrows = []
                    for neuron_idx in range(min(16, len(input_layer))):  # Limit to visible neurons
                        opacity = pixel.get_fill_opacity()
                        arrow = Arrow(
                            pixel.get_center(),
                            input_layer[neuron_idx].get_center(),
                            buff=0.1,
                            stroke_width=1,
                            stroke_opacity=opacity * 0.8,  # Opacity based on pixel value
                            color=BLUE_A,
                            max_tip_length_to_length_ratio=0.15
                        )
                        pixel_arrows.append(arrow)
                    arrows_matrix.append(pixel_arrows)
        
        # Animate each pixel's influence
        for pixel_idx, (pixel, opacity) in enumerate(selected_pixels):
            # Highlight the source pixel
            self.play(ShowCreation(pixel_highlights[pixel_idx]), run_time=0.3)
            
            # Show arrows spreading to input layer
            arrows = arrows_matrix[pixel_idx]
            
            # Create neuron highlights with opacity based on pixel value
            neuron_highlights = VGroup()
            for neuron_idx in range(len(arrows)):
                neuron = input_layer[neuron_idx]
                highlight = neuron.copy()
                highlight.set_fill(BLUE_A, opacity=opacity * 0.8)
                highlight.set_stroke(BLUE_A, width=2, opacity=opacity * 0.8)
                neuron_highlights.add(highlight)
            
            # Animate arrows and neuron highlights
            self.play(
                *[ShowCreation(arrow) for arrow in arrows],
                *[FadeIn(highlight) for highlight in neuron_highlights],
                run_time=0.5
            )
            
            # Brief pause to show the connection
            self.wait(0.2)
            
            # Fade out arrows but keep the highlights
            self.play(
                *[FadeOut(arrow) for arrow in arrows],
                run_time=0.3
            )
        
        # Final fade out of all elements
        self.play(
            FadeOut(pixel_highlights),
            *[FadeOut(mob) for mob in self.mobjects if isinstance(mob, Arrow)],
            run_time=0.5
        )
    
    def update_input_layer(self, network, digit):
        input_layer = network[0]
        # Update each input neuron's opacity based on the corresponding pixel value
        for i, neuron in enumerate(input_layer):
            if isinstance(neuron, Circle):  # Make sure we're only updating neurons
                pixel = digit[i] if i < len(digit) else None
                if pixel:
                    opacity = pixel.get_fill_opacity()
                    self.play(
                        neuron.animate.set_fill(opacity=opacity),
                        run_time=0.1
                    )