from terminal_solitaire.deck import Card, Deck
from terminal_solitaire.game_board import Board


def generate_original_tableau(deck: Deck, board: Board) -> list[list]:
    return [deck.deal(number_of_cards=board.columns - i) for i in range(board.columns)]


def select_card_on_board(board: Board, row_index: int, column_index: int) -> str:
    return board.tableau[(column_index, row_index)]


def remove_card_on_board(board: Board, row_index: int, column_index: int) -> None:
    board.tableau[(column_index, row_index)] = "  "


def place_card_on_board(
    card: str, board: Board, row_index: int, column_index: int
) -> None:
    board.tableau[(column_index, row_index)] = card


def reveal_card_on_board(
    board: Board, original_tableau: list[list[Card]], row_index: int, column_index: int
) -> None:
    # Column index offset by 2 when mapping to original tableau, as there are no empyt placeholders at start of list
    if row_index != 0:
        card = original_tableau[row_index][column_index - 2]
        setattr(card, "display_status", True)
        board.tableau[(column_index, row_index - 1)] = card.display_value
