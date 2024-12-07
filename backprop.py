from manimlib import *
import numpy as np

class BackpropagationDemo(Scene):
    def construct(self):
        # Network architecture
        self.layers = [4, 5, 3]
        
        # More vibrant colors using hex codes for precise control
        self.layer_colors = [
            "#00FFFF",  # Cyan (input layer)
            "#00FF00",  # Bright Green (hidden layer)
            "#FF1493"   # Deep Pink (output layer)
        ]
        
        # Alternative vibrant color schemes you could try:
        # Option 1 - Neon:
        # self.layer_colors = ["#39FF14", "#FF1493", "#00FFFF"]  # Neon green, pink, cyan
        
        # Option 2 - Electric:
        # self.layer_colors = ["#00FF00", "#FF00FF", "#FFFF00"]  # Electric green, magenta, yellow
        
        # Option 3 - Deep RGB:
        # self.layer_colors = ["#FF0000", "#00FF00", "#0000FF"]  # Pure red, green, blue
        
        # Create neural network visualization
        network = self.create_network()
        
        # Forward pass animation with text
        forward_text = Text("FORWARD PASS: COMPUTING PREDICTIONS", font_size=32.4, weight=BOLD)
        forward_text.to_edge(UP)
        self.play(Write(forward_text))
        self.forward_pass(network)
        self.play(FadeOut(forward_text))
        
        # Backpropagation animation with explanation
        backprop_text = Text("BACKPROPAGATION: UPDATING WEIGHTS", font_size=32.4, weight=BOLD)
        backprop_text.to_edge(UP)
        explanation = Text(
            "ORANGE LINES SHOW GRADIENTS FLOWING BACKWARDS\nNUMBERS SHOW WEIGHT UPDATES",
            font_size=27,
            color=ORANGE,
            weight=BOLD
        )
        explanation.next_to(backprop_text, DOWN)
        
        self.play(Write(backprop_text), Write(explanation))
        
        # Single backward pass
        self.backward_pass(network)
        
        self.play(FadeOut(backprop_text), FadeOut(explanation))
        
        # Repeat fast forward and backward pass 5 times
        for i in range(5):
            # Create iteration label
            iteration_text = Text(f"ITERATION {i+1}", font_size=32, weight=BOLD)
            iteration_text.to_edge(UP)
            
            # Forward pass label
            forward_label = Text("FORWARD PASS: COMPUTING PREDICTIONS", font_size=28, color=YELLOW, weight=BOLD)
            forward_label.next_to(iteration_text, DOWN)
            
            # Show iteration number and forward pass label
            self.play(Write(iteration_text), Write(forward_label))
            
            # Do forward pass
            self.fast_forward_pass(network)
            
            # Change to backward pass label
            backward_label = Text("BACKWARD PASS: UPDATING WEIGHTS", font_size=28, color=ORANGE, weight=BOLD)
            backward_label.next_to(iteration_text, DOWN)
            
            # Switch labels
            self.play(
                ReplacementTransform(forward_label, backward_label)
            )
            
            # Do backward pass
            self.second_backward_pass(network)
            
            # Fade out labels
            self.play(
                FadeOut(iteration_text),
                FadeOut(backward_label)
            )
        
        # Final wait
        self.wait(4)

    def ensure_double_updates(self, network):
        learning_rate = 0.1
        neurons = network[1]

        # Create weight updates for all neurons
        weight_updates = VGroup()
        for i in range(len(self.layers)):
            layer = neurons[i]
            start_idx = sum(self.layers[:i])
            for j, neuron in enumerate(layer):
                old_weight = float(self.weight_labels[start_idx + j].number)
                gradient = np.random.randn() * 0.1
                new_weight = old_weight - learning_rate * gradient

                # Create new weight label
                update_text = DecimalNumber(
                    new_weight,
                    num_decimal_places=2,
                    font_size=32,
                    color=WHITE
                )
                update_text.next_to(neuron, RIGHT, buff=0.2)
                weight_updates.add(update_text)

        # Animate the weight updates with Transform
        self.play(
            Transform(
                self.weight_labels,
                weight_updates,
                path_arc=PI/4
            ),
            run_time=1.0
        )

    def fast_forward_pass(self, network):
        neurons = network[1]
        all_connections = VGroup()

        # Create connections from each layer to the next layer only
        for i in range(len(self.layers) - 1):
            layer = neurons[i]
            next_layer = neurons[i + 1]  # Only connect to the next layer
            for start in layer:
                for end in next_layer:
                    connection = Line(
                        start.get_center(),
                        end.get_center(),
                        stroke_width=4,
                        stroke_opacity=1,
                        color=YELLOW
                    )
                    all_connections.add(connection)

        # Animate all connections at once, 50% slower
        self.play(ShowCreation(all_connections), run_time=1.875)  # Slowed down by 50%
        self.play(FadeOut(all_connections), run_time=0.9375)  # Slowed down by 50%

    def second_backward_pass(self, network):
        learning_rate = 0.1
        neurons = network[1]
        all_connections = VGroup()

        # Create connections from each layer to the directly previous layer
        for i in reversed(range(1, len(self.layers))):
            layer = neurons[i]
            prev_layer = neurons[i - 1]
            for start_neuron in layer:
                for end_neuron in prev_layer:
                    connection = Line(
                        start_neuron.get_center(),
                        end_neuron.get_center(),
                        stroke_width=4,
                        stroke_opacity=1,
                        color=ORANGE
                    )
                    all_connections.add(connection)

        # Animate all connections at once
        self.play(ShowCreation(all_connections), run_time=1.875)

        # Create animations for node movements and weight updates
        node_animations = []
        weight_updates = VGroup()
        
        for i in range(len(self.layers)):
            layer = neurons[i]
            start_idx = sum(self.layers[:i])
            for j, neuron in enumerate(layer):
                # Create weight update
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

        # Play the weight updates
        self.play(
            Transform(
                self.weight_labels,
                weight_updates,
                path_arc=PI/4
            ),
            run_time=1.0
        )

        # Fade out the connections
        self.play(FadeOut(all_connections), run_time=0.9375)

    def create_network(self):
        neurons = VGroup()
        connections = VGroup()
        self.weight_labels = VGroup()
        
        x_spacing = 4
        y_spacing = 0.8
        
        # Create layers
        for l, layer_size in enumerate(self.layers):
            layer = VGroup()
            for i in range(layer_size):
                neuron = Circle(radius=0.2)
                neuron.set_fill(self.layer_colors[l], opacity=1)
                neuron.set_stroke(self.layer_colors[l], opacity=1)
                neuron.move_to(np.array([l * x_spacing - 4, (i - layer_size/2) * y_spacing, 0]))
                
                # Add weight label for ALL neurons (including input layer)
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
        
        # Return VGroup without connections
        network = VGroup(neurons, self.weight_labels)
        
        # Show neurons and weights first
        self.play(ShowCreation(network), run_time=4.0)
        
        # Then animate the connections appearing
        self.play(ShowCreation(connections), run_time=4.0)
        
        # Return complete network
        return VGroup(connections, neurons, self.weight_labels)

    def forward_pass(self, network):
        neurons = network[1]
        for i in range(len(self.layers) - 1):
            layer = neurons[i]
            next_layer = neurons[i + 1]
            
            # Highlight all connections from the current layer to the next
            connections_to_highlight = VGroup()
            for start in layer:
                for end in next_layer:
                    connection = Line(
                        start.get_center(),
                        end.get_center(),
                        stroke_width=4,
                        stroke_opacity=1,
                        color=YELLOW
                    )
                    connections_to_highlight.add(connection)
            
            # Animate the connections
            self.play(ShowCreation(connections_to_highlight), run_time=2.5)  # Slowed down by 25%
            self.play(FadeOut(connections_to_highlight), run_time=1.25)  # Slowed down by 25%

    def backward_pass(self, network):
        learning_rate = 0.1
        neurons = network[1]
        
        for i in reversed(range(len(self.layers))):  # Changed to include input layer
            layer = neurons[i]
            
            # Create all connections for this layer
            connections_to_highlight = VGroup()
            weight_updates = VGroup()
            
            # Calculate start index for weight labels in this layer
            start_idx = sum(self.layers[:i])
            
            # Create connections to previous layer (if not input layer)
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
            
            # Update weights for all neurons in current layer
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
            
            # Animate the connections and weight updates
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
            
            self.play(
                *animations,
                run_time=1.875
            )
            
            # Fade out the connections if they exist
            if len(connections_to_highlight) > 0:
                self.play(
                    FadeOut(connections_to_highlight),
                    run_time=0.9375
                )