from SymbolicGrammar import SymbolicGrammar

if __name__ == "__main__":
    script_grammar = SymbolicGrammar()
    automaton = script_grammar.convert_to_automaton()

    while True:
        print("\nInteractive Menu:")
        print("1. Produce strings from the grammar")
        print("2. Validate a string with the automaton")
        print("3. Terminate Program")
        user_selection = input("Please select an option (1/2/3): ")

        if user_selection == '1':
            print("Strings produced by the grammar:")
            for _ in range(5):
                print(script_grammar.create_string())
            print("\nDetailed string generation process:")
            for _ in range(5):
                generated_string, generation_process = script_grammar.trace_string_creation()
                print("Generated String:", generated_string)
                print("Generation Steps:", generation_process)
        elif user_selection == '2':
            test_sequence = input("Enter a sequence to validate: ")
            is_accepted = automaton.validate_string(test_sequence)
            print(f'The sequence "{test_sequence}" is {"validated" if is_accepted else "rejected"} by the automaton.')
        elif user_selection == '3':
            print("Program terminated.")
            break
        else:
            print("Invalid input. Please choose 1, 2, or 3.")
