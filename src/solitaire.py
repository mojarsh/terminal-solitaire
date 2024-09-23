from pprint import pprint

from terminal_solitaire.deck import build_deck, shuffle_deck
from terminal_solitaire.game_board import Board, draw_board, place_cards_on_tableau
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
    board = Board(13, 7)
    tableau = board.generate_tableau_board()
    foundations = board.generate_foundations_board()
    dealt_cards = generate_original_tableau(shuffled, board)
    place_cards_on_tableau(dealt_cards, tableau)
    draw_board(foundations, tableau)
    while True:
        try:
            move_from = input("\nEnter the coordinates of the card to move (R, C): ")
            move_to = input("Enter the destination coordinates (R, C): ")
            move_from_coordinates = tuple(int(x) for x in move_from.split(","))
            move_to_coordinates = tuple(int(x) for x in move_to.split(","))
            selected_card = select_card_on_board(
                tableau,
                row_index=move_from_coordinates[0],
                column_index=move_from_coordinates[1],
            )
            remove_card_on_board(
                tableau,
                row_index=move_from_coordinates[0],
                column_index=move_from_coordinates[1],
            )
            place_card_on_board(
                card=selected_card,
                tableau=tableau,
                row_index=move_to_coordinates[0],
                column_index=move_to_coordinates[1],
            )
            reveal_card_on_board(
                tableau,
                row_index=move_from_coordinates[0],
                column_index=move_from_coordinates[1],
            )
            draw_board(foundations, tableau)

        except EOFError:
            break


if __name__ == "__main__":
    main()
