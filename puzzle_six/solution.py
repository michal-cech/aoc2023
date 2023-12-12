
from pathlib import Path
import time
from re import match
from functools import reduce 
from operator import mul

# it is symetric, it is enou
def naive_race_calculation(race: tuple[int, int]):
    total_time = race[0]
    distance = race[1]
    ways = 0
    for i in range(1, total_time - 1):
        if i * (total_time - i) > distance:
            ways +=1
    return ways


def part_1(races: list[tuple[int, int]]):
    ways = []
    for race in races:
        ways.append(naive_race_calculation(race))
    return reduce(mul, ways)

# i guess bruteforce works here
def part_2(races: list[tuple[int, int]]):
    total_time = ""
    distance = ""
    for race in races:
        total_time = f"{total_time}{race[0]}"
        distance = f"{distance}{race[1]}"
    return naive_race_calculation((int(total_time), int(distance)))
    



def main():
    start_time = time.time()
    with open(Path(__file__).parent / "input_file.txt", "r") as f:
        times, distances = f.readlines()
    races = list(zip([int(duration) for duration in times.removeprefix("Time:").removesuffix("\n").strip().split(" ") if duration.isnumeric()],
                [int(distance) for distance in distances.removeprefix("Distance:").removesuffix("\n").strip().split(" ") if distance.isnumeric()]))
    result_1 =  part_1(races)
    result_2 = part_2(races)
    print(f"Task 1 solution: {result_1}")
    print(f"Task 2 solution: {result_2}")
    print(time.time() - start_time)
    return 1

if __name__ == "__main__":
    print(main())