import csv
import click
from rich.console import Console

console = Console()

def load_votes(filename: str = "test.csv") -> list[list[str]]:
    choices = []
    with open(filename, "r") as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader:
            timestamp, *votes = row
            choices.append(votes)
    return choices


def count_up_votes(all_choices: list[list[str]], preference_ind: int = 0) -> dict[str, int]:
    choice_counts = {candidate: 0 for candidate in all_choices[0]}
    for choices in all_choices:
        choice = choices[preference_ind]
        choice_counts[choice] += 1
    return choice_counts


def remove_candidate(all_choices: list[list[str]], candidate: str) -> list[list[str]]:
    return [[choice for choice in choices if choice != candidate] for choices in all_choices]


def run_round(all_choices: list[list[str]], threshold: float) -> str:
    # Runs one seat election

    choice_counts = count_up_votes(all_choices)
    total_count = len(all_choices)

    curr_all_choices = all_choices

    winner = None

    while winner is None:
        max_votes = max(choice_counts.values())
        winners = [candidate for candidate, count in choice_counts.items()
                   if count == max_votes and count > total_count * threshold]
        if len(winners) == 1:
            console.print(f"{winners[0]} HAS WON A SEAT - WITH {max_votes} VOTES!")
            winner = winners[0]
        else:
            min_count = min(choice_counts.values())
            losers = [candidate for candidate, count in choice_counts.items() if count == min_count]
            if len(losers) > 1:
                loser = input(f"\nWHO GETS ELIMINATED? {losers}\n")
                if len(choice_counts) == 2:
                    winner = (choice_counts.keys() - {loser}).pop()
                    console.print(f"{winner} HAS WON A SEAT - WITH {choice_counts[winner] + 1} VOTES!")
                    continue
            else:
                loser = losers[0]
            curr_all_choices = remove_candidate(curr_all_choices, loser)
            choice_counts = count_up_votes(curr_all_choices)
    return winner


def run(all_choices: list[list[str]], seats: int, threshold: float):
    winners = []

    while len(winners) < seats:
        winner = run_round(all_choices, threshold)
        winners.append(winner)
        all_choices = remove_candidate(all_choices, winner)


@click.command()
@click.option('--seats', '-s', help='the number of seats to run our ranked choice voting algorithm on', required=True,
              type=int)
@click.option('--file', '-f', help='the csv file representing the fraternity\'s ballots in this standards election',
              type=click.Path(exists=True), required=True)
def main(seats: int, file: str):
    console.print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", style="bold green")
    console.print("  Standards Election Script (For AKS)")
    console.print("      --------------------------")
    console.print("    Brought to you by: David Malakh")
    console.print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n", style="bold green")
    data = load_votes(file)
    run(data, seats, threshold=0.5)


if __name__ == '__main__':
    main()
