from terminal_solitaire.board import Board, draw_board
from terminal_solitaire.deck import Deck, shuffle_deck


class Game:
    def __init__(self, tableau: Board, foundations: Board, deck: Deck):
        self.tableau = tableau
        self.foundations = foundations
        self.deck = deck

    def initialise_game(self):
        shuffled = shuffle_deck(self.deck)
        self.tableau.deal_initial_tableau(shuffled)
        draw_board(self.tableau, self.foundations)

    def run_game_loop(self):
        while True:
            try:
                move_from = int(input("\nEnter the column of the card to move: "))
                move_to = int(input("Enter the destination column: "))
                from_coordinates = self.tableau.find_coordinates_of_last_card(move_from)
                to_coordinates = self.tableau.find_coordinates_of_next_space(move_to)
                selected_card = self.tableau.select_card_on_board(from_coordinates)
                self.tableau.remove_card_from_board(from_coordinates)
                self.tableau.place_card_on_board(
                    card=selected_card, coordinates=to_coordinates
                )
                reveal_coordinates = self.tableau.find_coordinates_of_last_card(
                    move_from
                )
                self.tableau.reveal_card_on_board(reveal_coordinates)
                draw_board(self.tableau, self.foundations)

            except EOFError:
                break
