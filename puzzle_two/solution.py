from pathlib import Path

RED_C = 12
GREEN_C = 13
BLUE_C = 14

limits = {
    "green": GREEN_C,
    "red": RED_C,
    "blue": BLUE_C
}

def validate_round(round: str):
    round = round.strip()
    cubes = round.split(',')
    for cube in cubes:
        number, color = cube.strip().split(' ')
        if int(number) > limits[color]:
            return False
    return True

def part_1(games: list[str]):
    sum = 0
    for game in games:
        game_id, round_summary = game.split(":")
        game_id = int(game_id.removeprefix("Game").strip())
        rounds = round_summary.split(";")
        if all([validate_round(rnd) for rnd in rounds]):
            sum += game_id
    return sum

def compute_game_power(round_summary: str):
    max_red = 0
    max_blue = 0
    max_green = 0

    rounds = round_summary.split(';')
    for rnd in rounds:
        cubes = rnd.split(',')
        for cube in cubes:
            number, color = cube.strip().split(' ')
            match color:
                case "green":
                    max_green = max(max_green, int(number))
                case "blue":
                    max_blue = max(max_blue, int(number))
                case "red":
                    max_red = max(max_red, int(number))
    return max_red * max_blue * max_green


def part_2(games: list[str]):
    sum = 0
    for game in games:
        _, round_summary = game.split(":")
        game_power = compute_game_power(round_summary)
        sum += game_power
    return sum

def main():
    with open(Path(__file__).parent / "input_file.txt", "r") as f:
        content = f.readlines()
    result_1 =  part_1(content)
    result_2 = part_2(content)
    print(f"Task 1 solution: {result_1}")
    print(f"Task 1 solution: {result_2}")
    return 1

if __name__ == "__main__":
    print(main())