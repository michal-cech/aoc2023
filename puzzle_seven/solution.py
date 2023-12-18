
from pathlib import Path
import time
from functools import reduce, total_ordering
from operator import mul
from enum import Enum


symbol_comparions = {

    "2" : 2,
    "3" :  3,
    "4" :  4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14
}


symbol_comparions2 = {
    "J": 1,
    "2" : 2,
    "3" :  3,
    "4" :  4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
 
    "Q": 12,
    "K": 13,
    "A": 14
}

@total_ordering
class Game:
    def __init__(self, hand: str, bid: int, joker: bool = False):
        self.hand = hand
        self.bid = bid
        self._joker = joker
        self._symbols = symbol_comparions if self._joker is False else symbol_comparions2


        self._strength = self._compute_strengh()
    
    def _compute_strengh(self) -> int:
        symbols = {}
        n_of_jokers = 0
        for symbol in self.hand:
            if symbol in symbols:
                symbols[symbol] += 1
            else:
                symbols[symbol] = 1

        if self._joker:
            if (n_of_jokers := symbols.get("J", 0)):
                if (n_of_jokers == 5):
                    return 6
                symbols.pop("J")
                    

        symbols_n = sorted(symbols.values(), reverse=True)

        if self._joker:
            symbols_n[0] += n_of_jokers

        if symbols_n[0] == 1:
            return 0
        elif symbols_n[0] == 2:
            if (symbols_n[1]) == 2:
                return 2
            return 1
        elif symbols_n[0] == 3:
            if symbols_n[1] == 2:
                return 4
            return 3
        elif symbols_n[0] == 4:
            return 5
        else:
            return 6
        
    def __eq__(self, __value: "Game") -> bool:
        if self._strength != __value._strength:
            return False
        for i in range(5):
            if self.hand[i] != __value.hand[i]:
                return False
        return True
    

    def __gt__(self, __value: "Game") -> bool: 
        if self._strength > __value._strength:
            return True
        elif self._strength < __value._strength:
            return False
        else:
            for i in range(5):
                m_symbol = self._symbols[self.hand[i]]
                o_symbol = self._symbols[__value.hand[i]]
                if m_symbol > o_symbol:
                    return True
                elif o_symbol > m_symbol:
                    return False
        return False


def part_1(games: list[str]):
    total = 0
    loaded_games: list[Game] = []
    for game in games:
        hand, bid = game.split(" ")
        loaded_games.append(Game(hand, int(bid)))
    loaded_games = sorted(loaded_games)
    for i, g in enumerate(loaded_games):
        total += (i+1) * g.bid
    return total

def part_2(games: list[str]):
    total = 0
    loaded_games: list[Game] = []
    for game in games:
        hand, bid = game.split(" ")
        loaded_games.append(Game(hand, int(bid), joker=True))
    loaded_games = sorted(loaded_games)
    for i, g in enumerate(loaded_games):
        total += (i+1) * g.bid
    return total
    



def main():
    start_time = time.time()
    with open(Path(__file__).parent / "input_file.txt", "r") as f:
        games = f.readlines()
    # result_1 =  part_1(games)
    result_2 = part_2(games)
    # print(f"Task 1 solution: {result_1}")
    print(f"Task 2 solution: {result_2}")
    print(time.time() - start_time)
    return 1

if __name__ == "__main__":
    print(main())