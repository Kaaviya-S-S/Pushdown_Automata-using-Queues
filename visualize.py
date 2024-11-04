import io
from graphviz import Digraph
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import graphviz

pda_1 = {
    "states": ["q0", "q1", "q2", "Final"],
    "alphabet": ["a", "b", "c"],
    "start_state": "q0",
    "accept_states": ["Final"],
    "transitions": {
        ("q0", "a", "epsilon|a", "epsilon|epsilon"): "q0",
        ("q0", "a", "a|aa", "a|a"): "q0",
        ("q0", "b", "a|ab", "a|epsilon"): "q1",
        ("q1", "b", "b|bb", "a|epsilon"): "q1",
        ("q1", "c", "b|bb", "b|epsilon"): "q2",
        ("q2", "c", "epsilon|epsilon", "b|epsilon"): "q2",
        ("q2", "epsilon", "epsilon|epsilon", "epsilon|epsilon"): "Final",
    }
}

pda_2 = {
    "states": ["q0", "q1", "q2", "q3", "Final"],
    "alphabet": ["a", "b"],
    "start_state": "q0",
    "accept_states": ["Final"],
    "transitions": {
        ("q0", "a", "epsilon|a", "epsilon|epsilon"): "q0",
        ("q0", "a", "a|aa", "a|a"): "q0",
        ("q0", "b", "a|ab", "a|a"): "q1",
        ("q1", "b", "b|bb", "a|a"): "q1",
        ("q1", "a", "b|b", "a|epsilon"): "q2",
        ("q2", "a", "b|b", "a|epsilon"): "q2",
        ("q2", "b", "b|b", "b|epsilon"): "q3",
        ("q3", "b", "b|b", "b|epsilon"): "q3",
        ("q3", "epsilon", "epsilon|epsilon", "epsilon|epsilon"):"Final"
    }
}

pda_3 = {
    "states": ["q0", "q1", "q2", "q3", "Final"],
    "alphabet": ["a", "b"],
    "start_state": "q0",
    "accept_states": ["Final"],
    "transitions": {
        ("q0", "a", "epsilon|a", "epsilon|epsilon"): "q0",
        ("q0", "a", "a|aa", "a|a"): "q0",
        ("q0", "b", "a|a", "a|a"): "q1",
        ("q1", "b", "a|a", "a|a"): "q2",
        ("q2", "b", "a|a", "a|epsilon"): "q3",
        ("q3", "b", "a|a", "a|a"): "q2",
        ("q3", "epsilon", "epsilon|epsilon", "epsilon|epsilon"):"Final"
    }
}

pda_4 = {
    "states": ["q0", "q1", "q2", "Final"],
    "alphabet": ["a", "b", "c"],
    "start_state": "q0",
    "accept_states": ["Final"],
    "transitions": {
        ("q0", "a", "epsilon|a", "epsilon|epsilon"): "q0",
        ("q0", "a", "a|aa", "a|a"): "q0",
        ("q0", "b", "a|a0", "a|epsilon"): "q1",
        ("q1", "b", "0|00", "a|epsilon"): "q1",
        ("q1", "b", "0|00", "0|0"): "q1",
        ("q1", "c", "0|0", "0|epsilon"): "q2",
        ("q2", "c", "0|0", "0|epsilon"): "q2",
        ("q2", "epsilon", "0|0", "0|0"): "Final",
        ("q1", "epsilon", "0|0", "0|0"): "Final"
    }
}

def generate_pda_visualization(pda):
    dot = Digraph(engine="dot")

    for state in pda["states"]:
        shape = "ellipse" if state == pda["start_state"] else "doublecircle" if state in pda["accept_states"] else "circle"
        dot.node(state, state, shape=shape, style="filled", color="lightblue" if state == pda["start_state"] else "lightgrey")

    for (source_state, input_symbol, stack1_op, stack2_op), target_state in pda["transitions"].items():
        label = f"Input: {input_symbol}, Enqueue: {stack1_op}, Dequeue: {stack2_op}"
        dot.edge(source_state, target_state, label=label)

    return dot

def visualize_queue(steps, queue):
    fig, ax = plt.subplots(figsize=(10, 1))  # Adjusted size for a single row table

    # Draw a box for each item in the queue
    for index, value in enumerate(queue):
        x_position = index * 0.1  # Position each box directly next to the other
        ax.add_patch(plt.Rectangle((x_position, 0), 0.1, 1, edgecolor='black', facecolor='lightgray', linewidth=2))  # Box for each item
        ax.text(x_position + 0.05, 0.5, str(value), ha='center', va='center', fontsize=12)  # Label in the center of the box

    # Get the current step input character from steps list using a queue index
    current_step = steps[st.session_state.queue_index] if st.session_state.queue_index < len(steps) else None
    
    if current_step:
        st.write(f"Input Character: '{current_step[0]}'")  # Display the input character

    # Set the limits and remove y-ticks
    ax.set_xlim(0, len(queue) * 0.1)  # X limits based on the number of items
    ax.set_ylim(0, 1)  # Y limits for height of the row
    ax.set_xticks([])  # No x-ticks
    ax.set_yticks([])  # Remove y-ticks
    ax.set_title("Queue Visualization")
    ax.set_xlabel("Queue Index")
    
    return fig  # Return the figure object

def visualize_transition(pda, current_state, input_char, stack_ops=None, stack_symbols=None):
    dot = graphviz.Digraph()
    dot.attr(rankdir='LR')

    # Add nodes/states
    for state in pda['states']:
        shape = 'doublecircle' if state in pda['accept_states'] else 'circle'
        if state == current_state:
            dot.node(state, state, shape=shape, style='filled', fillcolor='lightblue')
        else:
            dot.node(state, state, shape=shape)

    # Add transitions
    for (from_state, char, ops, symbols), to_state in pda['transitions'].items():
        label = f"{char}\n{ops}\n{symbols}"
        
        # Check if this is the current transition
        is_current_transition = (
            from_state == current_state and
            (char == input_char or (char == 'epsilon' and input_char == '')) and
            (stack_ops is None or ops == stack_ops) and
            (stack_symbols is None or symbols == stack_symbols)
        )

        if is_current_transition:
            # Highlight current transition
            dot.edge(from_state, to_state, label=label, color='red', penwidth='2.0')
        else:
            dot.edge(from_state, to_state, label=label)

    return dot