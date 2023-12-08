from copy import deepcopy
from pathlib import Path
from typing import Callable
import time
from re import match
from itertools import takewhile
from dataclasses import dataclass

@dataclass
class LineInformation:
    source_start: int
    destination_start: int
    offset: int

    def translate(self, source: int) -> int | None:
        if source >= self.source_start and source <= self.source_start + self.offset:
            return self.destination_start + (source - self.source_start)
        return None
    
@dataclass
class Section:
    information: list[LineInformation]

    def translate(self, source: int) -> int:
        for info in self.information:
            if (found := info.translate(source)) is not None:
                return found
        return source
        

def build_section(section: list[str]) -> dict[int, int]:

    known_information: list[LineInformation] =  []
    for line in section:
        destination, source, covered = [int(n) for n in line.removesuffix("\n").split(" ")]
        known_information.append(LineInformation(source_start=source, destination_start=destination, offset=covered))


    return Section(information=known_information) 


def _build_maps(content: list[str]) -> tuple[list[int], dict[str, Section]]:
    seeds: list[int] = []
    sections: dict[str, Section] = {}
    while content:
        section = list(takewhile(lambda x: x != "\n", content))
        #special case of seeds
        if section[0].startswith("seeds:"):
            seeds = [int(seed) for seed in section[0].removeprefix("seeds").removesuffix("\n").split(" ") if seed.isnumeric()]
        else:
            sections[section[0].removesuffix(" map:\n")] = build_section(section[1:])
        content = content[len(section)+1:]
    return seeds, sections

def compute_location(seed: int, sections: dict[str, Section]) -> int:
    soil = sections['seed-to-soil'].translate(seed)
    fertilizer = sections['soil-to-fertilizer'].translate(soil)
    water = sections['fertilizer-to-water'].translate(fertilizer)
    light = sections['water-to-light'].translate(water)
    temporature =sections['light-to-temperature'].translate(light)
    humidity = sections['temperature-to-humidity'].translate(temporature)
    return sections['humidity-to-location'].translate(humidity)

def part_1(seeds: list[int], sections: dict[str, Section]): 
    min_location = None
    for seed in seeds:
        location = compute_location(seed, sections)
        if min_location is None:
            min_location = location
        else:
            min_location = min(min_location, location)
    return min_location


# bruteforce
def part_2(seeds: list[int], sections: dict[str, Section]):
    min_location = None
    # just in case so that we do not compute something twice
    memory = {}
    for i in range(0, len(seeds),2):
        for seed_i in range(seeds[i+1]):
            if (location := memory.get(seeds[i] + seed_i)) is None:
                location = compute_location(seeds[i] + seed_i, sections)
                memory[seeds[i] + seed_i] = location
            if min_location is None:
                min_location = location
            else:
                min_location = min(min_location, location)
        
    return min_location


def main():
    start_time = time.time()
    with open(Path(__file__).parent / "input_file.txt", "r") as f:
        content = f.readlines()
    seeds, sections = _build_maps(content)
    #result_1 =  part_1(seeds, sections)
    result_2 = part_2(seeds, sections)
    #print(f"Task 1 solution: {result_1}")
    print(f"Task 2 solution: {result_2}")
    print(time.time() - start_time)
    return 1

if __name__ == "__main__":
    print(main())