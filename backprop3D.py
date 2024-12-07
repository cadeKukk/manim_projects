from manimlib import *
import numpy as np

class BackpropagationDemo3D(Scene):
    def construct(self):
        # Network architecture
        self.layers = [4, 5, 3]
        
        # Same vibrant colors
        self.layer_colors = [
            "#00FFFF",  # Cyan (input layer)
            "#00FF00",  # Bright Green (hidden layer)
            "#FF1493"   # Deep Pink (output layer)
        ]
        
        # Set up the 3D camera
        frame = self.camera.frame
        frame.set_euler_angles(
            theta=0 * DEGREES,
            phi=0 * DEGREES,
        )
        frame.move_to(OUT * 3.25)  # Adjusted zoom
        
        # Create neural network visualization and shift it down
        network = self.create_network()
        network.shift(DOWN * 1.5)  # Move network down to make room for text
        
        # Forward pass animation with text
        forward_text = Text("FORWARD PASS: COMPUTING PREDICTIONS", font_size=32.4, weight=BOLD)
        forward_text.to_edge(UP, buff=1.2)  # Increased buffer from top
        self.play(Write(forward_text))
        self.forward_pass(network)
        self.play(FadeOut(forward_text))
        
        # Backpropagation animation with explanation
        backprop_text = Text("BACKPROPAGATION: UPDATING WEIGHTS", font_size=32.4, weight=BOLD)
        backprop_text.to_edge(UP, buff=1.2)  # Increased buffer from top
        explanation = Text(
            "ORANGE LINES SHOW GRADIENTS FLOWING BACKWARDS\nNUMBERS SHOW WEIGHT UPDATES",
            font_size=27,
            color=ORANGE,
            weight=BOLD
        )
        explanation.next_to(backprop_text, DOWN, buff=0.3)
        
        self.play(Write(backprop_text), Write(explanation))
        
        # Single backward pass
        self.backward_pass(network)
        
        self.play(FadeOut(backprop_text), FadeOut(explanation))
        
        # Repeat fast forward and backward pass 5 times
        for i in range(5):
            iteration_text = Text(f"ITERATION {i+1}", font_size=32, weight=BOLD)
            iteration_text.to_edge(UP, buff=1.2)  # Increased buffer from top
            
            forward_label = Text("FORWARD PASS: COMPUTING PREDICTIONS", font_size=28, color=YELLOW, weight=BOLD)
            forward_label.next_to(iteration_text, DOWN, buff=0.3)
            
            self.play(Write(iteration_text), Write(forward_label))
            self.fast_forward_pass(network)
            
            backward_label = Text("BACKWARD PASS: UPDATING WEIGHTS", font_size=28, color=ORANGE, weight=BOLD)
            backward_label.next_to(iteration_text, DOWN, buff=0.3)
            
            self.play(
                ReplacementTransform(forward_label, backward_label)
            )
            
            self.second_backward_pass(network)
            
            self.play(
                FadeOut(iteration_text),
                FadeOut(backward_label)
            )
        
        self.wait(4)

    def create_network(self):
        neurons = VGroup()
        connections = VGroup()
        self.weight_labels = VGroup()
        
        # Calculate layer positions
        x_spacing = 4  # Horizontal spacing between layers
        max_neurons = max(self.layers)
        y_spacing = 1.5  # Vertical spacing between neurons in a layer
        
        for l, layer_size in enumerate(self.layers):
            layer = VGroup()  # Group for this layer's neurons
            
            # Calculate vertical positions for neurons in this layer
            y_positions = np.linspace(
                -(layer_size - 1) * y_spacing / 2,
                (layer_size - 1) * y_spacing / 2,
                layer_size
            )
            
            for i, y_pos in enumerate(y_positions):
                # Create neuron as Circle (VMobject) instead of Dot
                neuron = Circle(
                    radius=0.15,
                    fill_color=self.layer_colors[l],
                    fill_opacity=1,
                    stroke_width=2,
                    stroke_color=WHITE
                )
                
                # Position the neuron
                neuron.move_to(np.array([
                    l * x_spacing - (len(self.layers) - 1) * x_spacing / 2,
                    y_pos,
                    0
                ]))
                
                # Add weight label
                weight = np.random.randn() * 0.1
                weight_label = DecimalNumber(
                    weight,
                    num_decimal_places=2,
                    font_size=32,
                    color=WHITE
                )
                weight_label.next_to(neuron, RIGHT, buff=0.2)
                self.weight_labels.add(weight_label)
                
                layer.add(neuron)
            neurons.add(layer)
            
            # Add connections after creating each layer (except first)
            if l > 0:
                prev_layer = neurons[l-1]
                for curr_neuron in layer:
                    for prev_neuron in prev_layer:
                        connection = Line(
                            prev_neuron.get_center(),
                            curr_neuron.get_center(),
                            stroke_opacity=0.2
                        )
                        connections.add(connection)
        
        network = VGroup(neurons, self.weight_labels)
        
        # Show neurons and weights first
        self.play(ShowCreation(network), run_time=4.0)
        
        # Then animate the connections
        self.play(ShowCreation(connections), run_time=4.0)
        
        return VGroup(connections, neurons, self.weight_labels)

    def forward_pass(self, network):
        neurons = network[1]
        connections = network[0]
        
        # Highlight each layer in sequence
        for i in range(len(self.layers)):
            layer = neurons[i]
            layer_connections = VGroup()
            
            # Get connections from this layer to next layer
            if i < len(self.layers) - 1:
                next_layer = neurons[i + 1]
                for start_neuron in layer:
                    for end_neuron in next_layer:
                        connection = Line(
                            start_neuron.get_center(),
                            end_neuron.get_center(),
                            stroke_width=4,
                            stroke_opacity=1,
                            color=YELLOW
                        )
                        layer_connections.add(connection)
            
            # Highlight neurons
            self.play(
                *[neuron.animate.set_fill(YELLOW, opacity=0.8) for neuron in layer],
                run_time=0.625
            )
            
            # Show connections if they exist
            if len(layer_connections) > 0:
                self.play(ShowCreation(layer_connections), run_time=1.25)
                self.play(FadeOut(layer_connections), run_time=0.625)
            
            # Return neurons to original color
            self.play(
                *[neuron.animate.set_fill(self.layer_colors[i], opacity=1) for neuron in layer],
                run_time=0.625
            )

    def fast_forward_pass(self, network):
        neurons = network[1]
        connections = network[0]
        
        for i in range(len(self.layers)):
            layer = neurons[i]
            layer_connections = VGroup()
            
            if i < len(self.layers) - 1:
                next_layer = neurons[i + 1]
                for start_neuron in layer:
                    for end_neuron in next_layer:
                        connection = Line(
                            start_neuron.get_center(),
                            end_neuron.get_center(),
                            stroke_width=4,
                            stroke_opacity=1,
                            color=YELLOW
                        )
                        layer_connections.add(connection)
            
            self.play(
                *[neuron.animate.set_fill(YELLOW, opacity=0.8) for neuron in layer],
                run_time=0.3125
            )
            
            if len(layer_connections) > 0:
                self.play(ShowCreation(layer_connections), run_time=0.625)
                self.play(FadeOut(layer_connections), run_time=0.3125)
            
            self.play(
                *[neuron.animate.set_fill(self.layer_colors[i], opacity=1) for neuron in layer],
                run_time=0.3125
            )

    def backward_pass(self, network):
        learning_rate = 0.1
        neurons = network[1]
        
        for i in reversed(range(len(self.layers))):
            layer = neurons[i]
            connections_to_highlight = VGroup()
            weight_updates = VGroup()
            
            start_idx = sum(self.layers[:i])
            
            # Store original positions for animation
            original_positions = {neuron: neuron.get_center() for neuron in layer}
            
            if i > 0:
                prev_layer = neurons[i-1]
                for start_neuron in layer:
                    for end_neuron in prev_layer:
                        connection = Line(
                            start_neuron.get_center(),
                            end_neuron.get_center(),
                            stroke_width=4,
                            stroke_opacity=1,
                            color=ORANGE
                        )
                        connections_to_highlight.add(connection)
            
            # Calculate new positions based on weight changes
            new_positions = {}
            for j, neuron in enumerate(layer):
                old_weight = float(self.weight_labels[start_idx + j].number)
                gradient = np.random.randn() * 0.1
                new_weight = old_weight - learning_rate * gradient
                
                # Calculate new position with slight z-offset based on weight change
                original_pos = original_positions[neuron]
                new_pos = original_pos + np.array([
                    0,  # x stays same
                    0,  # y stays same
                    gradient * learning_rate  # z changes based on weight update
                ])
                new_positions[neuron] = new_pos
                
                update_text = DecimalNumber(
                    new_weight,
                    num_decimal_places=2,
                    font_size=32,
                    color=YELLOW
                )
                update_text.next_to(neuron, RIGHT, buff=0.2)
                weight_updates.add(update_text)
            
            # Create animations for node movement and connection updates
            node_animations = [
                neuron.animate.move_to(new_pos)
                for neuron, new_pos in new_positions.items()
            ]
            
            # Update connections during movement
            if len(connections_to_highlight) > 0:
                self.play(
                    ShowCreation(connections_to_highlight),
                    *node_animations,
                    Transform(
                        self.weight_labels[start_idx:start_idx + len(layer)],
                        weight_updates,
                        path_arc=PI/4
                    ),
                    run_time=1.875
                )
                
                # Update connection positions after movement
                new_connections = VGroup()
                for start_neuron in layer:
                    for end_neuron in prev_layer:
                        connection = Line(
                            start_neuron.get_center(),
                            end_neuron.get_center(),
                            stroke_width=4,
                            stroke_opacity=1,
                            color=ORANGE
                        )
                        new_connections.add(connection)
                
                self.play(
                    Transform(connections_to_highlight, new_connections),
                    run_time=0.9375
                )
                
                self.play(
                    FadeOut(connections_to_highlight),
                    run_time=0.9375
                )
            else:
                self.play(
                    *node_animations,
                    Transform(
                        self.weight_labels[start_idx:start_idx + len(layer)],
                        weight_updates,
                        path_arc=PI/4
                    ),
                    run_time=1.875
                )

    def second_backward_pass(self, network):
        # Same as backward_pass but with faster animations
        learning_rate = 0.1
        neurons = network[1]
        
        for i in reversed(range(len(self.layers))):
            layer = neurons[i]
            connections_to_highlight = VGroup()
            weight_updates = VGroup()
            
            start_idx = sum(self.layers[:i])
            
            if i > 0:
                prev_layer = neurons[i-1]
                for j, start_neuron in enumerate(layer):
                    for k, end_neuron in enumerate(prev_layer):
                        connection = Line(
                            start_neuron.get_center(),
                            end_neuron.get_center(),
                            stroke_width=4,
                            stroke_opacity=1,
                            color=ORANGE
                        )
                        connections_to_highlight.add(connection)
            
            for j, neuron in enumerate(layer):
                old_weight = float(self.weight_labels[start_idx + j].number)
                gradient = np.random.randn() * 0.1
                new_weight = old_weight - learning_rate * gradient
                
                update_text = DecimalNumber(
                    new_weight,
                    num_decimal_places=2,
                    font_size=32,
                    color=YELLOW
                )
                update_text.next_to(neuron, RIGHT, buff=0.2)
                weight_updates.add(update_text)
            
            animations = []
            if len(connections_to_highlight) > 0:
                animations.append(ShowCreation(connections_to_highlight))
            
            animations.append(
                Transform(
                    self.weight_labels[start_idx:start_idx + len(layer)],
                    weight_updates,
                    path_arc=PI/4
                )
            )
            
            self.play(*animations, run_time=0.9375)
            
            if len(connections_to_highlight) > 0:
                self.play(FadeOut(connections_to_highlight), run_time=0.46875)