from terminal_solitaire.deck import Card, Deck
from terminal_solitaire.game_board import Board


def generate_original_tableau(deck: Deck, board: Board) -> list[list[Card]]:
    return [deck.deal(number_of_cards=board.columns - i) for i in range(board.columns)]


def select_card_on_board(tableau: dict, row_index: int, column_index: int) -> Card:
    return tableau[(row_index, column_index)]


def remove_card_on_board(tableau: dict, row_index: int, column_index: int) -> None:
    tableau[(row_index, column_index)] = "  "


def place_card_on_board(
    card: Card, tableau: dict, row_index: int, column_index: int
) -> None:
    tableau[(row_index, column_index)] = card


def reveal_card_on_board(
    tableau: dict[tuple : Card | str], row_index: int, column_index: int
) -> None:
    board_location = select_card_on_board(tableau, row_index - 1, column_index)
    board_location.display_status = True
