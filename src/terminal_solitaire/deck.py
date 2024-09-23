import itertools
import random
from dataclasses import dataclass
from enum import StrEnum


class Suits(StrEnum):
    """Unicode values for each suit, spades, clubs, hearts and diamonds respectively."""

    SPADES = "\u2660"
    CLUBS = "\u2663"
    HEARTS = "\u2661"
    DIAMONDS = "\u2662"


class Values(StrEnum):
    ACE = "A"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "T"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"


@dataclass
class Card:
    suit: str
    value: str
    colour: str
    display_status: bool = False

    @property
    def display_value(self) -> str:
        """Sets the icon seen for the card on the tableau, either card value or card back."""
        if self.display_status is False:
            return 2 * "\u2587"
        else:
            return self.value + self.suit


@dataclass
class Deck:
    cards: list[Card]

    def deal(self, number_of_cards: int) -> list[Card]:
        """Deals cards from the deck using integer passed as argument."""
        return [self.cards.pop() for _ in range(number_of_cards)]


def _set_card_colour(suit: str) -> str:
    """Sets colour of card based on suit."""
    if suit in (Suits.HEARTS, Suits.DIAMONDS):
        return "Red"
    else:
        return "Black"


def build_deck() -> Deck:
    """Builds deck from product of all possible Suits and Values."""
    cards = []
    suits = [s for s in Suits]
    values = [v for v in Values]
    for suit, value in list(itertools.product(suits, values)):
        colour = _set_card_colour(suit)
        card = Card(suit, value, colour)
        cards.append(card)

    return Deck(cards)


def shuffle_deck(deck: Deck) -> Deck:
    """Shuffles given deck using shuffle method from random library."""
    cards = deck.cards
    random.shuffle(cards)

    return Deck(cards)
