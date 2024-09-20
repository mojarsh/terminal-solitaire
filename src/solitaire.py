from terminal_solitaire.deck import Deck
from terminal_solitaire.game_board import Board, assign_tableau_display_icon
from terminal_solitaire.tableau import generate_original_tableau, move_card

VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
# Unicode values for each suit, spades, clubs, hearts and diamonds respectively
SUITS = ["\u2660", "\u2663", "\u2661", "\u2662"]


def main() -> None:

    deck = Deck(VALUES, SUITS).shuffle()
    board = Board(7, 13)
    original_tableau = generate_original_tableau(deck, board)
    assign_tableau_display_icon(original_tableau, board)
    board.draw_board()
    move_card(board, tableau=original_tableau, row_index=1, column_index=0)
    board.draw_board()


if __name__ == "__main__":
    main()
