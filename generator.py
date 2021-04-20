import csv
import random


def generate(names: list[str], num_votes: int) -> list[list[str]]:
    generated = []
    for _ in range(num_votes):
        choices = list(names)
        random.shuffle(choices)
        generated.append(choices)
    return generated

def write_file(all_choices: list[list[str]], filename: str = "test.csv"):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(["Timestamp", *[f"vote [{ind}]" for ind in range(len(all_names))]])

        for choices in all_choices:
            writer.writerow(["blah", *choices])


if __name__ == '__main__':
    all_names = ["Hani", "Varun", "Beckmann", "Tom Hughes"]
    _all_choices = generate(all_names, 20)
    write_file(_all_choices)

