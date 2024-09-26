from typing import Callable

from terminal_solitaire.board import Board
from terminal_solitaire.deck import Card, Values

type Rule = Callable[[Board, tuple[int, int], Card], bool]


def alternating_colour_rule(
    board: Board, coordinates: tuple[int, int], card: Card
) -> bool:
    previous_card_coordinates = board.find_coordinates_of_last_card(coordinates[1])
    previous_card = board.select_card_on_board(previous_card_coordinates)
    if previous_card.colour != card.colour:
        return True
    else:
        return False


def lower_value_rule(board: Board, coordinates: tuple[int, int], card: Card) -> bool:
    value_index = {value.value: idx for idx, value in enumerate(Values)}
    previous_card_coordinates = board.find_coordinates_of_last_card(coordinates[1])
    previous_card = board.select_card_on_board(previous_card_coordinates)
    previous_card_index = value_index[previous_card.value]
    current_card_index = value_index[card.value]

    if previous_card_index - current_card_index == 1:
        return True

    else:
        return False


def place_ace_on_foundations_rule(
    board: Board, coordinates: tuple[int, int], card: Card
) -> bool: ...
