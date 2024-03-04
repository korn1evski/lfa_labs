import networkx as nx
import matplotlib.pyplot as plt

class Automaton:
    def __init__(self, states, alphabet, final_states, transitions):
        self.states = states
        self.alphabet = alphabet
        self.final_states = final_states
        self.transitions = transitions

    def is_dfa(self):
        for state in self.states:
            for symbol in self.alphabet:
                transitions = self.transitions.get((state, symbol), None)
                if transitions is None or len(transitions) != 1:
                    return False
        return True

    def convert_to_dfa(self):
        if self.is_dfa():
            return self

        new_states = []
        new_transitions = {}
        new_final_states = []

        initial_state = ('q0',)
        new_states.append(initial_state)
        queue = [initial_state]

        while queue:
            current = queue.pop(0)
            for symbol in self.alphabet:
                next_state = sum([self.transitions.get((state, symbol), []) for state in current], [])
                next_state = tuple(sorted(set(next_state)))
                if next_state not in new_states and next_state:
                    new_states.append(next_state)
                    queue.append(next_state)

                new_transitions[(current, symbol)] = next_state

                if any(state in self.final_states for state in next_state):
                    new_final_states.append(next_state)

        return Automaton(new_states, self.alphabet, new_final_states, new_transitions)

    def draw(self):
        G = nx.DiGraph()

        for state in self.states:
            G.add_node(state, label=str(state))

        edge_labels = {}

        for (src, symbol), dst in self.transitions.items():
            if (src, dst) in edge_labels:
                edge_labels[(src, dst)] += ', ' + symbol
            else:
                edge_labels[(src, dst)] = symbol
                G.add_edge(src, dst)

        pos = nx.spring_layout(G)
        plt.figure(figsize=(12, 8))

        nx.draw_networkx_nodes(G, pos, node_size=3000, node_color='white', edgecolors='black')
        nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20)

        nx.draw_networkx_labels(G, pos, labels={node: node for node in G.nodes()})
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        initial_state = 'q0'
        if initial_state in pos:
            initial_pos = (pos[initial_state][0] - 0.1, pos[initial_state][1])
            G.add_node('start', pos=initial_pos, label='')
            G.add_edge('start', initial_state, label='')

        for final_state in self.final_states:
            nx.draw_networkx_nodes(G, pos, nodelist=[final_state], node_shape='o', node_size=3500, edgecolors='black',
                                   linewidths=2)

        plt.axis('off')
        plt.show()

    def __repr__(self):
        return f'States: {self.states}\nAlphabet: {self.alphabet}\nFinal States: {self.final_states}\nTransitions: {self.transitions}'


# Example usage:
states = {'q0', 'q1', 'q2', 'q3'}
alphabet = {'a', 'b'}
final_states = {'q3'}
transitions = {
    ('q0', 'a'): ['q1', 'q2'],
    ('q1', 'b'): ['q1'],
    ('q1', 'a'): ['q2'],
    ('q2', 'a'): ['q1'],
    ('q2', 'b'): ['q3'],
}

automaton = Automaton(states, alphabet, final_states, transitions)
print("The automaton is a DFA." if automaton.is_dfa() else "The automaton is an NFA.")

if not automaton.is_dfa():
    dfa = automaton.convert_to_dfa()
    print("Converted to DFA:")
    print(dfa)
    dfa.draw()
