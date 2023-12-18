
from pathlib import Path
import time
from functools import reduce, total_ordering
from operator import mul
from enum import Enum
import re
from math import lcm

def build_directions(raw_directions) -> dict[str, tuple[str, str]]:
    dirs = {}
    for line in raw_directions:
        dir = re.match("^(?P<start>[A-Z]+)\s*=\s*\((?P<left>[A-Z]+),\s*(?P<right>[A-Z]+)\)$", line).groupdict()
        dirs[dir['start']] = (dir['left'], dir['right'])
    return dirs





def part_1(instructions: str, directions: dict[str, tuple[str, str]]):
    steps = 0
    dest = "AAA"
    while dest != "ZZZ":
        for ins in instructions:
            steps += 1
            if ins == "L":
                dest = directions[dest][0]
            else:
                dest = directions[dest][1]
            if dest == "ZZZ":
                break
    return steps

# calculate for each
# find lowest common multiple
def part_2(instructions: str, directions: dict[str, tuple[str, str]]):
    starting_nodes = [node for node in directions.keys() if node.endswith("A")]
    all_steps = [0] * len(starting_nodes)
    for i, starting_node in enumerate(starting_nodes): 
        dest = starting_node
        steps = 0
        while not dest.endswith("Z"):
            for ins in instructions:
                steps += 1
                if ins == "L":
                    dest = directions[dest][0]
                else:
                    dest = directions[dest][1]
                if  dest.endswith("Z"):
                    break
        all_steps[i] = steps
    return lcm(*all_steps)
    



def main():
    start_time = time.time()
    with open(Path(__file__).parent / "input_file.txt", "r") as f:
        instructions, _, *map_directions = f.readlines()
    instructions = instructions.removesuffix("\n")
    directions_struct = build_directions(map_directions)
    result_1 =  part_1(instructions, directions_struct)
    result_2 = part_2(instructions, directions_struct)
    print(f"Task 1 solution: {result_1}")
    print(f"Task 2 solution: {result_2}")
    print(time.time() - start_time)
    return 1

if __name__ == "__main__":
    print(main())