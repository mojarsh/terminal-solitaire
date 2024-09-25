from terminal_solitaire.board import draw_board, generate_board
from terminal_solitaire.deck import build_deck, shuffle_deck


def main() -> None:

    deck = build_deck()
    shuffled = shuffle_deck(deck)
    tableau = generate_board(13, 7)
    foundations = generate_board(1, 7)
    tableau.deal_initial_tableau(shuffled)
    draw_board(tableau, foundations)
    while True:
        try:
            move_from = int(input("\nEnter the column of the card to move: "))
            move_to = int(input("Enter the destination column: "))
            from_coordinates = tableau.find_coordinates_of_last_card(move_from)
            to_coordinates = tableau.find_coordinates_of_next_space(move_to)
            selected_card = tableau.select_card_on_board(from_coordinates)
            tableau.remove_card_from_board(from_coordinates)
            tableau.place_card_on_board(card=selected_card, coordinates=to_coordinates)
            reveal_coordinates = tableau.find_coordinates_of_last_card(move_from)
            tableau.reveal_card_on_board(reveal_coordinates)
            draw_board(tableau, foundations)

        except EOFError:
            break


if __name__ == "__main__":
    main()
