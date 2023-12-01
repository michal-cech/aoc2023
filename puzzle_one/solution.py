from pathlib import Path

VALID_NUMBERS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}

def main():
    sum = 0
    with open(Path(__file__).parent / "input_file.txt", "r") as f:
        content = f.readlines()
    for line in content:
        if len(line) == 0:
            continue
        first_digit = None
        last_digit = None 
        while first_digit is None:
            if line[0].isdigit():
                first_digit = int(line[0]) * 10
                break
            elif (first_digit := VALID_NUMBERS.get(line[0:3])) or (first_digit := VALID_NUMBERS.get(line[0:4])) or (first_digit := VALID_NUMBERS.get(line[0:5])):
                first_digit = 10*first_digit
                break
            line = line[1:]
        while last_digit is None:
            if line[-1].isdigit():
                last_digit = int(line[-1])
                break
            elif (last_digit := VALID_NUMBERS.get(line[-3:])) or (last_digit := VALID_NUMBERS.get(line[-4:])) or (last_digit := VALID_NUMBERS.get(line[-5:])):
                break
            line = line[:-1]
        sum += first_digit+last_digit
    return sum

if __name__ == "__main__":
    print(main())