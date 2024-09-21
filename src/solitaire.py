from terminal_solitaire.deck import Deck
from terminal_solitaire.game_board import Board, assign_tableau_display_icon
from terminal_solitaire.tableau import (
    generate_original_tableau,
    place_card_on_board,
    remove_card_on_board,
    reveal_card_on_board,
    select_card_on_board,
)

VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
# Unicode values for each suit, spades, clubs, hearts and diamonds respectively
SUITS = ["\u2660", "\u2663", "\u2661", "\u2662"]


def main() -> None:

    deck = Deck(VALUES, SUITS).shuffle()
    board = Board(7, 13)
    original_tableau = generate_original_tableau(deck, board)
    assign_tableau_display_icon(original_tableau, board)
    board.draw_board()
    while True:
        try:
            move_from = input("\nEnter the coordinates of the card to move (R, C): ")
            move_to = input("Enter the destination coordinates (R, C): ")
            move_from_coordinates = tuple(int(x) for x in move_from.split(","))
            move_to_coordinates = tuple(int(x) for x in move_to.split(","))
            selected_card = select_card_on_board(
                board,
                row_index=move_from_coordinates[0],
                column_index=move_from_coordinates[1],
            )
            remove_card_on_board(
                board,
                row_index=move_from_coordinates[0],
                column_index=move_from_coordinates[1],
            )
            place_card_on_board(
                card=selected_card,
                board=board,
                row_index=move_to_coordinates[0],
                column_index=move_to_coordinates[1],
            )
            reveal_card_on_board(
                board,
                original_tableau,
                row_index=move_from_coordinates[0],
                column_index=move_from_coordinates[1],
            )
            board.draw_board()

        except EOFError:
            break


if __name__ == "__main__":
    main()
