import itertools
import random


class Deck:
    def __init__(self, values: list, suits: list) -> None:
        self.values = values
        self.suits = suits

    def build(self) -> list:
        combinations = list(itertools.product(self.values, self.suits))
        return [suit + value for suit, value in combinations]

    def shuffle(self) -> list:
        deck = self.build()
        random.shuffle(deck)
        return deck
