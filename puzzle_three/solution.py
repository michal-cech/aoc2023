from copy import deepcopy
from pathlib import Path
from typing import Callable

class Coordinates:

    def __init__(self, number_pointer_coordinates, pointer_coordinates, symbol_coordinates) -> None:
        self.number_pointer_coordinates: dict[tuple[int, int], int] = number_pointer_coordinates
        self.pointer_coordinates: dict[int, int] = pointer_coordinates
        self.symbol_coordinates: list[tuple[int, int]] = symbol_coordinates

def construct_mapping(lines):
    number_pointer_coordinates = {}
    symbol_coordinates = []
    pointer_coordinates = {}
    number_counter = 0
    for i, line in enumerate(lines):
        j = 0
        while j < len(line):
            if line[j]  in ['.', "\n"]:
                j += 1
                continue
            elif line[j].isdigit():
                number = 0
                start_index = j
                end_index = j
                while line[j].isdigit():
                    number = number*10+int(line[j])
                    end_index = j
                    j +=1
                pointer_coordinates[number_counter] = number
                for k in range(start_index, end_index + 1):
                    number_pointer_coordinates[(i, k)] = number_counter
                number_counter += 1
            else:
                symbol_coordinates.append((i, j))
                j+=1
    return Coordinates(number_pointer_coordinates=number_pointer_coordinates, symbol_coordinates=symbol_coordinates, pointer_coordinates=pointer_coordinates)

def sum_locally(local_space: list[tuple[int, int]], coordinates: Coordinates):
    sum = 0
    for coordinate in local_space:
        if (pointer := coordinates.number_pointer_coordinates.pop(coordinate, None)) is not None:
            if (number := coordinates.pointer_coordinates.pop(pointer, None)) is not None:
                sum += number
    return sum

def power_locally(local_space: list[tuple[int, int]], coordinates: Coordinates):
    adjanced_numbers = []
    for coordinate in local_space:
        if (pointer := coordinates.number_pointer_coordinates.pop(coordinate, None)) is not None:
            if (number := coordinates.pointer_coordinates.pop(pointer, None)) is not None:
                adjanced_numbers.append(number)
                if len(adjanced_numbers) > 2:
                    return 0
    if len(adjanced_numbers) == 2:
        return adjanced_numbers[0] * adjanced_numbers[1]
    return 0


def _generic_solution(lines: list[str], coordinates: Coordinates, computation: Callable[[list[tuple[int, int]], Coordinates], int]):
    sum = 0
    max_len = len(lines[0])
    for symbol in coordinates.symbol_coordinates:
        symbol_local_space = []
        # look above
        if symbol[0] > 0:
            # strictly above
            symbol_local_space.append((symbol[0]-1, symbol[1]))
          
            if symbol[1] > 0:
                symbol_local_space.append((symbol[0]-1, symbol[1]-1))
            if symbol[1] < max_len -2:
                symbol_local_space.append((symbol[0]-1, symbol[1]+1))
        # look to the right
        if symbol[1] > 0:
            symbol_local_space.append((symbol[0], symbol[1]-1))
        # look to the left
        if symbol[1] > 0:
            symbol_local_space.append((symbol[0], symbol[1]+1))

        # look below
        if symbol[0] < len(lines) - 1:
            # strictly above
            symbol_local_space.append((symbol[0]+1, symbol[1]))
            if symbol[1] > 0:
                symbol_local_space.append((symbol[0]+1, symbol[1]-1))
            if symbol[1] < max_len -2:
                symbol_local_space.append((symbol[0]+1, symbol[1]+1))
                #strictly below
        sum += computation(symbol_local_space, coordinates=coordinates)
    return sum

def part_1(lines: list[str], coordinates: Coordinates):
    return _generic_solution(lines, coordinates, sum_locally)


def part_2(lines: list[str], coordinates: Coordinates):
    return _generic_solution(lines, coordinates, power_locally)

def main():
    with open(Path(__file__).parent / "input_file.txt", "r") as f:
        content = f.readlines()
    coordinates = construct_mapping(content)
    result_1 =  part_1(content, deepcopy(coordinates))
    result_2 = part_2(content, deepcopy(coordinates))
    print(f"Task 1 solution: {result_1}")
    print(f"Task 2 solution: {result_2}")
    return 1

if __name__ == "__main__":
    print(main())