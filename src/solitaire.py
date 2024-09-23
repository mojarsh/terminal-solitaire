from pprint import pprint

from terminal_solitaire.deck import build_deck, shuffle_deck
from terminal_solitaire.game_board import Board, assign_tableau_display_icon
from terminal_solitaire.tableau import (
    generate_original_tableau,
    place_card_on_board,
    remove_card_on_board,
    reveal_card_on_board,
    select_card_on_board,
)


def main() -> None:

    deck = build_deck()
    shuffled = shuffle_deck(deck)
    board = Board(7, 13)
    original_tableau = generate_original_tableau(shuffled, board)
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
            pprint(original_tableau)
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
