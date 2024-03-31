import random


def generate_string():
    s = "L"
    print(s)
    s += "M" if random.randint(0, 1) == 0 else "N"
    print(s)
    s += "OOO"
    print(s)

    for i in range(random.randint(0, 5)):
        s += "p"
    print(s)

    s += "Q"
    print(s)
    s += "2" if random.randint(0, 1) == 0 else "3"

    return s


def explain_regex_processing():
    steps = [
        "1. Begin with an empty string.",
        "2. Append 'L' to the string as it is a fixed starting character.",
        "3. Add 'M' or 'N' to the string, randomly chosen, representing the (M|N) part of the regex.",
        "4. Append 'OOO' to the string to fulfill the exact three 'O's required by O^3.",
        "5. Append 'p' randomly 0 to 5 times to match the p* part, where * denotes zero or more occurrences.",
        "6. Append 'Q' which is a fixed character in the regex.",
        "7. Finish the string with '2' or '3', randomly chosen, to satisfy the (2|3) part.",
        "8. The final string satisfies the regular expression."
    ]
    return '\n'.join(steps)


# Generate and print a valid string
valid_string = generate_string()
print("Generated string:", valid_string)

# Print the explanation of the regex processing
process_explanation = explain_regex_processing()
print("\nExplanation of regex processing:")
print(process_explanation)
