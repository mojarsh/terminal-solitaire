from terminal_solitaire.board import Board, draw_board
from terminal_solitaire.deck import Card, Deck, shuffle_deck
from terminal_solitaire.rules import Rule


class Game:
    def __init__(
        self, tableau: Board, foundations: Board, deck: Deck, rules: list[Rule]
    ) -> None:
        self.tableau = tableau
        self.foundations = foundations
        self.deck = deck
        self.rules = rules

    def initialise_game(self) -> None:
        shuffled = shuffle_deck(self.deck)
        self.tableau.deal_initial_tableau(shuffled)
        draw_board(self.tableau, self.foundations)

    def _get_movement_input(self) -> None:
        move_from = int(input("\nEnter the column of the card to move: "))
        move_to = int(input("Enter the destination column: "))

        return move_from, move_to

    def run_game_loop(self) -> None:
        while True:
            try:
                move_from, move_to = self._get_movement_input()
                from_coordinates = self.tableau.find_coordinates_of_last_card(move_from)
                to_coordinates = self.tableau.find_coordinates_of_next_space(move_to)
                card_to_move = self.tableau.select_card_on_board(from_coordinates)
                card_at_destination_coordinates = (
                    self.tableau.find_coordinates_of_last_card(move_to)
                )
                card_at_destination = self.tableau.select_card_on_board(
                    card_at_destination_coordinates
                )
                self._apply_rules(card_to_move, card_at_destination)
                self.tableau.remove_card_from_board(from_coordinates)
                self.tableau.place_card_on_board(
                    card=card_to_move, coordinates=to_coordinates
                )
                reveal_coordinates = self.tableau.find_coordinates_of_last_card(
                    move_from
                )
                self.tableau.reveal_card_on_board(reveal_coordinates)
                draw_board(self.tableau, self.foundations)

            except EOFError:
                break

            except ValueError:
                print("Invalid move, try a different one!")
                pass

    def _apply_rules(self, card_to_move: Card, card_at_destination: Card) -> None:
        for rule in self.rules:
            if not rule(card_to_move, card_at_destination):
                raise ValueError()
