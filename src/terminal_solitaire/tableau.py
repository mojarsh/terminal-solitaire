from terminal_solitaire.deck import Deck, deal
from terminal_solitaire.game_board import Board


def generate_original_tableau(deck: Deck, board: Board) -> list[list]:
    return [
        deal(deck=deck, number_of_cards=board.columns - i) for i in range(board.columns)
    ]


def move_card(board: Board, tableau: list[list], row_index: int, column_index: int):
    selected_card = tableau[row_index].pop(column_index)
    board.tableau[(column_index, row_index)] = selected_card
