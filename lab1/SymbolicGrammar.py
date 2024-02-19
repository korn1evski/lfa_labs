import random

from StateMachine import StateMachine


class SymbolicGrammar:
    def __init__(self):
        self.non_terminals = ['S', 'L', 'D']
        self.terminals = ['a', 'b', 'c', 'd', 'e', 'f', 'j']
        self.rules = {
            'S': ['aS', 'bS', 'cD', 'dL'],
            'L': ['eL', 'fL', 'jD'],
            'D': ['eD'],
        }
        self.end_symbols = {
            'S': ['e'],
            'L': ['e'],
            'D': ['d']
        }
        self.start_symbol = 'S'

    def create_string(self):
        sequence = [self.start_symbol]
        while any(sym in self.non_terminals for sym in sequence):
            for idx, sym in enumerate(sequence):
                if sym in self.non_terminals:
                    options = self.rules.get(sym, []) + self.end_symbols.get(sym, [])
                    selected_path = random.choice(options)
                    sequence[idx:idx + 1] = selected_path
                    break
        return ''.join(sequence)

    def trace_string_creation(self):
        sequence = [self.start_symbol]
        path_trace = [self.start_symbol]
        lower_bound, upper_bound = 5, 10
        current_step = 0
        while current_step < upper_bound:
            change_made = False
            for idx, sym in enumerate(sequence):
                if sym in self.non_terminals:
                    options = self.rules.get(sym, [])
                    if current_step >= lower_bound - 1:
                        options += self.end_symbols.get(sym, [])
                    if options:
                        selected_path = random.choice(options)
                        sequence[idx:idx + 1] = selected_path
                        path_trace.append(' -> ' + ''.join(sequence))
                        change_made = True
                        break
            if not change_made:
                break
            current_step += 1
        return ''.join(sequence), '\n'.join(path_trace)

    def convert_to_automaton(self):
        automaton = StateMachine(set(self.terminals))
        for nt in self.non_terminals:
            automaton.register_state(nt)
        automaton.register_state("Finish", True)
        for symbol, paths in self.rules.items():
            for path in paths:
                trigger = path[0]
                destination = path[1] if len(path) > 1 else "Finish"
                automaton.create_link(symbol, trigger, destination)
        for symbol, paths in self.end_symbols.items():
            for path in paths:
                automaton.create_link(symbol, path[0], "Finish")
        automaton.define_initial_state(self.start_symbol)
        return automaton
