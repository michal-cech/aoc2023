from copy import deepcopy
from pathlib import Path
from typing import Callable
import time
from re import match

def _get_overlap(line: str):
    numbers = match("^Card\s+\d+:\s*(?P<winning>(\d+\s+)+)\|\s*(?P<my>(\d+\s*)+)\n?$", line)
    winning_numbers = {int(n) for n in numbers.groupdict()['winning'].split(' ') if n.isnumeric()}
    my_numbers = {int(n) for n in numbers.groupdict()['my'].removesuffix('\n').split(' ') if n.isnumeric()}
    collected_numbers = winning_numbers.intersection(my_numbers)
    return collected_numbers

def part_1(lines: list[str]):
    sum = 0
    for line in lines:
        collected_numbers = _get_overlap(line)
        if len(collected_numbers ) > 0:
            card_points = pow(2, len(collected_numbers) - 1)
            sum += card_points
    return sum

def part_2(lines: list[str]):
    number_of_cards = [0 for _ in range(len(lines))]
    for index, line in enumerate(lines):
        collected_numbers = _get_overlap(line)
        # count original
        number_of_cards[index] += 1
        for i in range(1, len(collected_numbers)+ 1):
            if index + i < len(lines):
                # add the number of current card to the following card (2 instances -> growth by 2)
                number_of_cards[index + i] += number_of_cards[index]
    return sum(number_of_cards)


# def part_2(lines: list[str], coordinates: Coordinates):
#     return _generic_solution(lines, coordinates, power_locally)

def main():
    start_time = time.time()
    with open(Path(__file__).parent / "input_file.txt", "r") as f:
        content = f.readlines()
    result_1 =  part_1(deepcopy(content))
    result_2 = part_2(deepcopy(content))
    print(f"Task 1 solution: {result_1}")
    print(f"Task 2 solution: {result_2}")
    print(time.time() - start_time)
    return 1

if __name__ == "__main__":
    print(main())