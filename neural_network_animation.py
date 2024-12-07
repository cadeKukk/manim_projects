from manimlib import *
import random
import numpy as np

class NeuralNetworkAnimation(Scene):
    def construct(self):
        # Start with camera zoomed out 15%
        self.camera.frame.scale(1.15)
        
        # Network architecture
        layers = [4, 6, 6, 3]
        layer_colors = [BLUE_B, GREEN_C, PURPLE_B, ORANGE]
        network = VGroup()
        neurons = []
        
        # Create neurons with adjusted spacing
        for i, layer_size in enumerate(layers):
            layer = VGroup()
            for j in range(layer_size):
                neuron = Circle(radius=0.15)
                neuron.set_fill(layer_colors[i], opacity=1.0)
                neuron.set_stroke(opacity=0)
                x_pos = 2.5*i - 4
                y_pos = 1.8*j - (layer_size-1)*1.8/2
                neuron.move_to(np.array([x_pos, y_pos, 0]))
                layer.add(neuron)
            neurons.append(layer)
            network.add(layer)

        # Create labels
        input_labels = VGroup()
        for i, neuron in enumerate(neurons[0]):
            label = Text(f"X{i+1}", font_size=20, weight=BOLD)
            label.next_to(neuron, LEFT, buff=0.2)
            input_labels.add(label)

        output_labels = VGroup()
        for i, neuron in enumerate(neurons[-1]):
            label = Text(f"Y{i+1}", font_size=20, weight=BOLD)
            label.next_to(neuron, RIGHT, buff=0.2)
            output_labels.add(label)

        input_title = Text("INPUT LAYER", font_size=28, weight=BOLD)
        input_title.next_to(neurons[0], UP + LEFT, buff=0.5)
        output_title = Text("OUTPUT LAYER", font_size=28, weight=BOLD)
        output_title.next_to(neurons[-1], UP + RIGHT, buff=0.5)

        # Create edges and prepare equations
        edges = VGroup()
        all_edges = []
        equations = {i: [] for i in range(len(neurons[-1]))}  # Dictionary to store equation terms

        for i in range(len(layers)-1):
            layer_edges = []
            for n1_idx, neuron1 in enumerate(neurons[i]):
                neuron_edges = []
                for n2_idx, neuron2 in enumerate(neurons[i+1]):
                    edge = Line(
                        neuron1.get_center(),
                        neuron2.get_center(),
                    )
                    edge.set_stroke(opacity=0.2, width=1)
                    edges.add(edge)
                    neuron_edges.append(edge)
                    
                    # If this is connecting to output layer, store equation term
                    if i == len(layers)-2:
                        term = Tex(f"w_{{{n1_idx+1}}}^{{(3)}}a_{{{n1_idx+1}}}^{{(2)}}", font_size=24)
                        equations[n2_idx].append(term)
                layer_edges.append(neuron_edges)
            all_edges.append(layer_edges)

        # Create detailed equations for Y3, Y2, Y1 at the start
        output_equations = VGroup()
        for i in range(3):  # Y3, Y2, Y1
            eq_terms = VGroup()
            # Add Y_i = term
            start_term = Tex(f"Y_{3-i} = ", font_size=28)
            eq_terms.add(start_term)
            
            # Add summation terms
            for j in range(6):
                if j == 0:
                    term = Tex(f"w_{j+1}^{{(3)}}a_{j+1}^{{(2)}}", font_size=28)
                else:
                    plus = Tex("+", font_size=28)
                    term = Tex(f"w_{j+1}^{{(3)}}a_{j+1}^{{(2)}}", font_size=28)
                    plus.next_to(eq_terms[-1], RIGHT, buff=0.2)
                    term.next_to(plus, RIGHT, buff=0.2)
                    eq_terms.add(plus)
                eq_terms.add(term)
            
            # Position equation
            eq_terms.arrange(RIGHT, buff=0.2)
            eq_terms.move_to(RIGHT * 4 + UP * (1-i))
            eq_terms.set_opacity(0)  # Start invisible
            output_equations.add(eq_terms)

        self.add(output_equations)  # Add to scene but invisible

        # Scale entire network slightly smaller to account for initial zoom
        network_group = VGroup(network, edges, input_labels, output_labels, input_title, output_title)
        network_group.scale(0.9)  # Adjusted scale factor
        network_group.move_to(ORIGIN + LEFT * 2)

        # Initial animation sequence
        self.play(ShowCreation(edges), run_time=3)
        self.play(ShowCreation(network), run_time=3)
        self.play(
            Write(input_labels),
            Write(output_labels),
            Write(input_title),
            Write(output_title),
            run_time=3
        )

        # Animation for connections and equations
        for layer_idx, layer_edges in enumerate(all_edges):
            for neuron_idx, neuron_edges in enumerate(layer_edges):
                source_neuron = neurons[layer_idx][neuron_idx]
                
                # Collect all forward-connected nodes and edges through all paths
                forward_highlights = VGroup()
                forward_nodes = set()  # Using set to avoid duplicates
                
                # First layer of connections
                first_targets = []
                for edge_idx, edge in enumerate(neuron_edges):
                    highlight = edge.copy()
                    highlight.set_stroke(YELLOW, width=2, opacity=1)
                    forward_highlights.add(highlight)
                    # Get target node for this edge
                    target_node = neurons[layer_idx + 1][edge_idx % len(neurons[layer_idx + 1])]
                    first_targets.append(target_node)
                
                # Second layer of connections (if not at last layer)
                if layer_idx < len(layers) - 2:
                    for first_target in first_targets:
                        target_idx = list(neurons[layer_idx + 1]).index(first_target)
                        next_edges = all_edges[layer_idx + 1][target_idx]
                        for next_edge in next_edges:
                            highlight = next_edge.copy()
                            highlight.set_stroke(YELLOW, width=2, opacity=0.8)
                            forward_highlights.add(highlight)
                            # Get final target node
                            final_layer = neurons[-1]
                            for final_node in final_layer:
                                # Using numpy.linalg.norm for distance calculation
                                if np.linalg.norm(next_edge.get_end() - final_node.get_center()) < 0.1:
                                    forward_nodes.add(final_node)

                # Color animations for all affected nodes
                color_animations = []
                # Source node
                color_animations.append(
                    source_neuron.animate.set_fill(YELLOW_A, opacity=1.0)
                )
                # First layer targets
                for target in first_targets:
                    color_animations.append(
                        target.animate.set_fill(YELLOW_B, opacity=1.0)
                    )
                # Final layer targets
                for target in forward_nodes:
                    color_animations.append(
                        target.animate.set_fill(YELLOW_C, opacity=1.0)
                    )

                # Play highlight animations
                self.play(
                    ShowCreation(forward_highlights),
                    *color_animations,
                    run_time=0.8
                )

                # After highlighting, if we're at Y-layer, pan camera and show equations
                if layer_idx == len(layers)-2:
                    if neuron_idx == 0:
                        self.play(
                            self.camera.frame.animate.move_to(RIGHT * 4),
                            run_time=1.5
                        )
                    
                    # Show equation terms
                    eq_idx = min(neuron_idx, len(output_equations) - 1)
                    current_eq = output_equations[eq_idx]
                    
                    if len(current_eq) > 0:
                        self.play(
                            current_eq[0].animate.set_opacity(1),
                            run_time=0.5
                        )
                        
                        for term_idx in range(1, len(current_eq)):
                            self.play(
                                current_eq[term_idx].animate.set_opacity(1),
                                run_time=0.3
                            )

                # Reset colors
                reset_animations = []
                reset_animations.append(
                    source_neuron.animate.set_fill(layer_colors[layer_idx], opacity=1.0)
                )
                for target in first_targets:
                    reset_animations.append(
                        target.animate.set_fill(layer_colors[layer_idx + 1], opacity=1.0)
                    )
                for target in forward_nodes:
                    reset_animations.append(
                        target.animate.set_fill(layer_colors[-1], opacity=1.0)
                    )

                self.play(
                    FadeOut(forward_highlights),
                    *reset_animations,
                    run_time=0.5
                )

                # Node jiggle
                jiggle_animations = []
                for layer in neurons:
                    for neuron in layer:
                        jiggle_animations.append(
                            ApplyMethod(
                                neuron.move_to,
                                neuron.get_center() + np.array([
                                    random.uniform(-0.2, 0.2),
                                    random.uniform(-0.2, 0.2),
                                    0
                                ]),
                                rate_func=there_and_back,
                                run_time=random.uniform(0.5, 1.0)
                            )
                        )
                self.play(*jiggle_animations, run_time=1.0)

        self.wait(4)

        # After the main animation, create and show simplified equations
        simplified_equations = VGroup()
        
        # Create three simplified equations (one for each output)
        for i in range(3):
            eq = Tex(
                f"Y_{i+1}", "=", "\\sigma(", 
                "\\sum_{j=1}^{6}", "w_j^{(3)}", "a_j^{(2)}", ")",
                font_size=32
            )
            simplified_equations.add(eq)

        # Stack equations vertically with proper spacing, starting below OUTPUT LAYER
        for i, eq in enumerate(simplified_equations):
            eq.move_to(RIGHT * 7 + DOWN * (i + 1))  # Start below and go down

        # Create explanation labels
        explanation = VGroup()
        where_text = Tex("where:", font_size=28)
        sigma_text = Tex("\\sigma = \\text{activation function}", font_size=28)
        w_text = Tex("w_j^{(3)} = \\text{weights}", font_size=28)
        a_text = Tex("a_j^{(2)} = \\text{hidden layer activations}", font_size=28)

        # Position explanation text below equations
        where_text.next_to(simplified_equations, DOWN, buff=0.7)
        sigma_text.next_to(where_text, DOWN, buff=0.4)
        w_text.next_to(sigma_text, DOWN, buff=0.4)
        a_text.next_to(w_text, DOWN, buff=0.4)
        explanation.add(where_text, sigma_text, w_text, a_text)

        # Group all new elements
        final_equations = VGroup(simplified_equations, explanation)
        final_equations.move_to(RIGHT * 7)

        # Fade out detailed equations and show simplified ones
        self.play(
            FadeOut(output_equations),
            run_time=1
        )

        # Show simplified equations with staggered animation
        for eq in simplified_equations:
            self.play(Write(eq), run_time=0.8)

        # Show explanation text
        for text in explanation:
            self.play(Write(text), run_time=0.8)

        # Wait a moment to read
        self.wait(2)

        # Final camera movement adjusted for initial zoom
        self.play(
            self.camera.frame.animate.scale(1.3).shift(RIGHT * 2 + DOWN * 1),  # Adjusted scale factor
            run_time=2
        )

        # Add highlighting animations to show correspondence
        for i in range(3):
            output_node = neurons[-1][i]
            eq = simplified_equations[i]
            
            self.play(
                output_node.animate.set_fill(YELLOW_A),
                eq.animate.set_color(YELLOW_A),
                run_time=0.5
            )
            
            self.play(
                output_node.animate.set_fill(layer_colors[-1]),
                eq.animate.set_color(WHITE),
                run_time=0.5
            )

        # Final jiggle animation with everything visible
        jiggle_animations = []
        for layer in neurons:
            for neuron in layer:
                jiggle_animations.append(
                    ApplyMethod(
                        neuron.move_to,
                        neuron.get_center() + np.array([
                            random.uniform(-0.15, 0.15),
                            random.uniform(-0.15, 0.15),
                            0
                        ]),
                        rate_func=there_and_back,
                        run_time=random.uniform(0.4, 0.8)
                    )
                )
        self.play(*jiggle_animations, run_time=0.8)

        self.wait(3)

        # Pan back to original position without scaling
        self.play(
            self.camera.frame.animate.move_to(ORIGIN),
            run_time=2
        )

        # Final jiggle animation
        jiggle_animations = []
        for layer in neurons:
            for neuron in layer:
                jiggle_animations.append(
                    ApplyMethod(
                        neuron.move_to,
                        neuron.get_center() + np.array([
                            random.uniform(-0.15, 0.15),
                            random.uniform(-0.15, 0.15),
                            0
                        ]),
                        rate_func=there_and_back,
                        run_time=random.uniform(0.4, 0.8)
                    )
                )
        self.play(*jiggle_animations, run_time=0.8)

        self.wait(3)

        # Transition to larger network
        new_layers = [8, 12, 12, 6]  # Doubled size
        new_layer_colors = [BLUE_B, GREEN_C, PURPLE_B, ORANGE]
        new_network = VGroup()
        new_neurons = []
        
        # Create new neurons
        for i, layer_size in enumerate(new_layers):
            layer = VGroup()
            for j in range(layer_size):
                neuron = Circle(radius=0.15)
                neuron.set_fill(new_layer_colors[i], opacity=1.0)
                neuron.set_stroke(opacity=0)
                x_pos = 2.0*i - 3
                y_pos = 1.5*j - (layer_size-1)*1.5/2
                neuron.move_to(np.array([x_pos, y_pos, 0]))
                layer.add(neuron)
            new_neurons.append(layer)
            new_network.add(layer)

        # Create new edges
        new_edges = VGroup()
        new_all_edges = []
        for i in range(len(new_layers)-1):
            layer_edges = []
            for j in range(new_layers[i]):
                edges = VGroup()
                for k in range(new_layers[i+1]):
                    start = new_neurons[i][j].get_center()
                    end = new_neurons[i+1][k].get_center()
                    edge = Line(start, end)
                    edge.set_stroke(width=0.5, opacity=0.5)
                    edges.add(edge)
                    new_edges.add(edge)
                layer_edges.append(edges)
            new_all_edges.append(layer_edges)

        # Create new labels
        new_input_labels = VGroup()
        for i, neuron in enumerate(new_neurons[0]):
            label = Text(f"X{i+1}", font_size=18, weight=BOLD)
            label.next_to(neuron, LEFT, buff=0.1)
            new_input_labels.add(label)

        new_output_labels = VGroup()
        for i, neuron in enumerate(new_neurons[-1]):
            label = Text(f"Y{i+1}", font_size=18, weight=BOLD)
            label.next_to(neuron, RIGHT, buff=0.1)
            new_output_labels.add(label)

        # Transition animation
        self.play(
            FadeOut(network),
            FadeOut(edges),
            FadeOut(input_labels),
            FadeOut(output_labels),
            FadeOut(input_title),
            FadeOut(output_title),
            run_time=1.5
        )

        self.play(
            FadeIn(new_edges),
            FadeIn(new_network),
            FadeIn(new_input_labels),
            FadeIn(new_output_labels),
            run_time=2
        )

        # Create simplified counter display group
        counter_group = VGroup()
        
        # Title for the counter - moved right from -10 to -8
        counter_title = Text("ACTIVE PATH", font_size=28, color=BLUE)
        counter_title.move_to(LEFT * 8 + UP * 3)  # Adjusted from LEFT * 10 to LEFT * 8
        
        # Create simplified counter text elements
        from_text = Text("From → ", font_size=24)
        to_text = Text("To → ", font_size=24)
        
        # Position counter elements relative to adjusted title position
        from_text.next_to(counter_title, DOWN, buff=0.5)
        to_text.next_to(from_text, DOWN, buff=0.4)
        
        # Add to counter group
        counter_group.add(counter_title, from_text, to_text)
        
        # Add counter to scene
        self.add(counter_group)

        # Connection highlighting animations with counter updates
        for layer_idx in range(len(new_layers)-1):
            for neuron_idx in range(new_layers[layer_idx]):
                # Simplified source label
                source_label = Text(
                    f"X{neuron_idx + 1}" if layer_idx == 0 
                    else f"N{neuron_idx + 1}",  # Simplified node notation
                    font_size=24, 
                    color=YELLOW_A
                )
                source_label.next_to(from_text, RIGHT, buff=0.2)
                
                # Track paths and nodes
                path_highlights = VGroup()
                affected_nodes = set()
                target_nodes = set()
                
                # Start with source node
                source_neuron = new_neurons[layer_idx][neuron_idx]
                affected_nodes.add(source_neuron)
                
                # Track connections through all layers
                current_nodes = {source_neuron}
                all_target_labels = []
                connection_count = 0
                
                for next_layer_idx in range(layer_idx + 1, len(new_layers)):
                    next_nodes = set()
                    target_labels = []
                    
                    for current_node in current_nodes:
                        current_layer = new_neurons[next_layer_idx - 1]
                        current_idx = list(current_layer).index(current_node)
                        
                        if next_layer_idx - 1 < len(new_all_edges):
                            if current_idx < len(new_all_edges[next_layer_idx - 1]):
                                edges = new_all_edges[next_layer_idx - 1][current_idx]
                                for edge in edges:
                                    highlight = edge.copy()
                                    highlight.set_stroke(YELLOW, width=2, opacity=0.8)
                                    path_highlights.add(highlight)
                                    connection_count += 1
                                    
                                    next_layer = new_neurons[next_layer_idx]
                                    for target_node in next_layer:
                                        if np.linalg.norm(edge.get_end() - target_node.get_center()) < 0.1:
                                            next_nodes.add(target_node)
                                            affected_nodes.add(target_node)
                                            # Add target label
                                            target_idx = list(next_layer).index(target_node)
                                            target_labels.append(
                                                f"Y{target_idx + 1}" if next_layer_idx == len(new_layers) - 1
                                                else f"L{next_layer_idx + 1}N{target_idx + 1}"
                                            )
                    
                    current_nodes = next_nodes
                    if target_labels:
                        all_target_labels.append(target_labels)

                # Simplified target label
                final_targets = sorted(set([
                    f"Y{list(new_neurons[-1]).index(node) + 1}" 
                    for node in affected_nodes 
                    if node in new_neurons[-1]
                ]))
                target_label = Text(
                    ", ".join(final_targets),
                    font_size=24, 
                    color=YELLOW_C
                )
                target_label.next_to(to_text, RIGHT, buff=0.2)

                # Update counter display
                self.play(
                    FadeOut(counter_group[1:]),  # Remove old labels but keep title
                    FadeIn(source_label),
                    FadeIn(target_label),
                    ShowCreation(path_highlights),
                    *[node.animate.set_fill(YELLOW_A, opacity=1.0) for node in affected_nodes],
                    run_time=0.5
                )

                # Reset colors
                self.play(
                    FadeOut(path_highlights),
                    *[node.animate.set_fill(new_layer_colors[next(i for i, layer in enumerate(new_neurons) if node in layer)], opacity=1.0) for node in affected_nodes],
                    run_time=0.3
                )

                # Update counter group
                counter_group.remove(*counter_group[1:])
                counter_group.add(from_text, source_label, to_text, target_label)

        self.wait(2)

        # After creating larger network, fade out old equations
        self.play(
            FadeOut(output_equations),
            FadeOut(final_equations),
            run_time=1
        )

        # Create new simplified equations for the larger network (6 outputs)
        new_simplified_equations = VGroup()
        
        # Create six simplified equations (one for each output)
        for i in range(6):
            eq = Tex(
                f"Y_{i+1}", "=", "\\sigma(", 
                "\\sum_{j=1}^{12}", "w_j^{(3)}", "a_j^{(2)}", ")",
                font_size=24  # Smaller font size for more equations
            )
            new_simplified_equations.add(eq)

        # Stack equations vertically with proper spacing
        for i, eq in enumerate(new_simplified_equations):
            eq.move_to(RIGHT * 7 + UP * (2.5-i))  # Adjusted vertical spacing

        # Create explanation labels with smaller font
        new_explanation = VGroup()
        where_text = Tex("where:", font_size=22)
        sigma_text = Tex("\\sigma = \\text{activation function}", font_size=22)
        w_text = Tex("w_j^{(3)} = \\text{weights}", font_size=22)
        a_text = Tex("a_j^{(2)} = \\text{hidden layer activations}", font_size=22)

        # Position explanation text
        where_text.next_to(new_simplified_equations, DOWN, buff=0.4)
        sigma_text.next_to(where_text, DOWN, buff=0.3)
        w_text.next_to(sigma_text, DOWN, buff=0.3)
        a_text.next_to(w_text, DOWN, buff=0.3)
        new_explanation.add(where_text, sigma_text, w_text, a_text)

        # Group all new elements
        new_final_equations = VGroup(new_simplified_equations, new_explanation)
        new_final_equations.move_to(RIGHT * 7)

        # Pan camera to show equations
        self.play(
            self.camera.frame.animate.move_to(RIGHT * 4),
            run_time=1.5
        )

        # Show simplified equations with staggered animation
        for eq in new_simplified_equations:
            self.play(Write(eq), run_time=0.4)  # Faster animation for more equations

        # Show explanation text
        for text in new_explanation:
            self.play(Write(text), run_time=0.4)

        # Pan back to center
        self.play(
            self.camera.frame.animate.move_to(ORIGIN),
            run_time=1.5
        )

        # Add to scene for later reference
        self.add(new_final_equations)