class StateMachine:
    def __init__(self, alphabet):
        self.all_states = set()
        self.alphabet = alphabet
        self.state_links = {}
        self.initial_state = None
        self.final_states = set()

    def define_initial_state(self, initial):
        self.initial_state = initial
        self.all_states.add(initial)

    def register_state(self, state_name, is_final=False):
        self.all_states.add(state_name)
        if is_final:
            self.final_states.add(state_name)
        self.state_links.setdefault(state_name, {})

    def create_link(self, source, trigger, destination):
        self.state_links.setdefault(source, {})
        self.state_links[source][trigger] = destination

    def validate_string(self, test_string):
        position = self.initial_state
        for char in test_string:
            if char not in self.alphabet or char not in self.state_links.get(position, {}):
                return False
            position = self.state_links[position][char]
        return position in self.final_states
