import itertools
import random
from dataclasses import dataclass


@dataclass
class Card:
    suit: str
    value: str
    colour: str


class Deck:
    def __init__(self, values: list, suits: list) -> None:
        self.values = values
        self.suits = suits

    def build(self) -> list:
        list(itertools.product(self.suits, self.values))
        deck = []
        for suit, value in list(itertools.product(self.suits, self.values)):
            colour = set_card_colour(suit)
            card = Card(suit, value, colour)
            deck.append(card)

        return deck

    def shuffle(self) -> list:
        deck = self.build()
        random.shuffle(deck)
        return deck


def deal(deck: list, number_of_cards: int) -> list:
    return [deck.pop() for _ in range(number_of_cards)]


def set_card_colour(suit: str) -> str:
    if suit in ("\u2661", "\u2662"):
        return "Red"
    else:
        return "Black"
