from terminal_solitaire.board import (
    Board,
    draw_board,
    generate_board_element,
    place_cards_on_tableau,
)
from terminal_solitaire.deck import build_deck, shuffle_deck


def main() -> None:

    deck = build_deck()
    shuffled = shuffle_deck(deck)
    tableau = generate_board_element(13, 7)
    foundations = generate_board_element(1, 7)
    board = Board(foundations, tableau)
    dealt_cards = board.deal_initial_tableau(shuffled)
    place_cards_on_tableau(dealt_cards, tableau.board)
    draw_board(board)
    while True:
        try:
            move_from = int(input("\nEnter the column of the card to move: "))
            move_to = int(input("Enter the destination column: "))
            from_coordinates = board.find_last_card_in_tableau_column(move_from)
            to_coordinates = board.find_next_free_space_in_tableau_column(move_to)
            selected_card = board.select_card_on_tableau(from_coordinates)
            board.remove_card_on_tableau(from_coordinates)
            board.place_card_on_tableau(card=selected_card, coordinates=to_coordinates)
            reveal_coordinates = board.find_last_card_in_tableau_column(move_from)
            board.reveal_card_on_tableau(reveal_coordinates)
            draw_board(board)

        except EOFError:
            break


if __name__ == "__main__":
    main()
