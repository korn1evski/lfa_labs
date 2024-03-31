import random

def generate_string():
    s = ""

    # Append 'R' between 0 to 5 times
    for i in range(random.randint(0, 5)):
        s += "R"
    print(s)

    # Append 'S'
    s += "S"
    print(s)

    # Append one of 'T', 'U', 'V'
    temp = random.randint(0, 2)
    s += "T" if temp == 0 else ("U" if temp == 1 else "V")
    print(s)

    # Append 'W'
    s += "W"
    print(s)

    # Choose one of 'X', 'Y', 'Z' and append it twice
    temp = random.randint(0, 2)
    temp2 = "X" if temp == 0 else ("Y" if temp == 1 else "Z")
    s += temp2
    s += temp2

    return s

def explain_regex_processing():
    steps = [
        "1. Begin with an empty string.",
        "2. Append 'R' 0 to 5 times, chosen randomly, to match the R* part of the regex.",
        "3. Append 'S' as a fixed character.",
        "4. Add one of 'T', 'U', or 'V' randomly, matching the (T|U|V) part.",
        "5. Append 'W' as a fixed character.",
        "6. Randomly choose one of 'X', 'Y', or 'Z' and append it twice, to match X^2, Y^2, or Z^2 if we assume ^2 means exactly two occurrences.",
        "7. The constructed string matches the regular expression pattern."
    ]
    return '\n'.join(steps)

# Generate and print a valid string
valid_string = generate_string()
print("Generated string:", valid_string)

# Print the explanation of the regex processing
process_explanation = explain_regex_processing()
print("\nExplanation of regex processing:")
print(process_explanation)
