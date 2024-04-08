import random


def generate_from_pattern_with_steps(pattern):
    # Split the pattern into parts
    parts = pattern.split(' ')

    output = ""
    for part in parts:
        if '^' in part:  # Handle repetition factor
            base_part, repeat_factor = part.split('^')
            repeat_factor = int(repeat_factor)
        elif '*' in part:  # Handle 0 to n repetitions
            base_part = part.replace('*', '')
            repeat_factor = random.randint(0, 5)  # 0 to 5 repetitions
        elif '+' in part:  # Handle 1 to n repetitions
            base_part = part.replace('+', '')
            repeat_factor = random.randint(1, 5)  # 1 to 5 repetitions
        else:
            base_part = part
            repeat_factor = 1

        # Remove parentheses and split options, if any
        options = base_part.replace('(', '').replace(')', '').split('|')

        # If there are options, choose one and possibly repeat it
        if options:
            chosen_option = random.choice(options)
            new_output = chosen_option * repeat_factor
            output += new_output
            print(f"After processing '{part}': {output}")  # Print intermediate output

    return output


# Example patterR* S (T|U|V) W (x|y|z)^2n
pattern1 = "(S|T) (U|V) W* Y+ 24"
pattern2 = "L (M|N) O^3 p* Q (2|3)"
pattern3 = ""

# Generate sequence with step-by-step output
final_sequence = generate_from_pattern_with_steps(pattern1)
print(f"Final Sequence: {final_sequence}")
