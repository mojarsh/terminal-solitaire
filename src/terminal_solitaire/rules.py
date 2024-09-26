from typing import Callable

from terminal_solitaire.board import Board
from terminal_solitaire.deck import Card, Values

type Rule = Callable[[Card, Card], bool]


def alternating_colour_rule(card_to_move: Card, card_at_destination: Card) -> bool:
    if card_to_move.colour != card_at_destination.colour:
        return True
    else:
        return False


def lower_value_rule(card_to_move: Card, card_at_destination: Card) -> bool:
    value_index = {value.value: idx for idx, value in enumerate(Values)}
    previous_card_index = value_index[card_at_destination.value]
    current_card_index = value_index[card_to_move.value]

    if previous_card_index - current_card_index == 1:
        return True

    else:
        return False


def place_ace_on_foundations_rule(
    board: Board, coordinates: tuple[int, int], card: Card
) -> bool: ...
