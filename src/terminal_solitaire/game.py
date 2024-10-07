from terminal_solitaire.board import Board, Foundations, draw_board
from terminal_solitaire.deck import Card, Deck, shuffle_deck
from terminal_solitaire.rules import Rule, check_if_card_is_ace


class Game:
    def __init__(
        self, tableau: Board, foundations: Board, deck: Deck, rules: list[Rule]
    ) -> None:
        self.tableau_board = tableau
        self.foundation_board = foundations
        self.foundation_list = Foundations()
        self.deck = deck
        self.rules = rules

    def initialise_game(self) -> None:
        shuffled = shuffle_deck(self.deck)
        self.tableau_board.deal_initial_tableau(shuffled)
        draw_board(self.tableau_board, self.foundation_board)

    def run_game_loop(self) -> None:
        while True:
            try:
                move_from = int(input("\nEnter the column of the card to move: "))
                from_coordinates = self.tableau_board.find_coordinates_of_last_card(
                    move_from
                )
                card_to_move = self.tableau_board.select_card_on_board(from_coordinates)
                if check_if_card_is_ace(card_to_move):
                    self.foundation_board.move_card_to_foundations(
                        self.foundation_list, card_to_move
                    )
                    self.tableau_board.remove_card_from_board(from_coordinates)

                else:
                    move_to = int(input("Enter the destination column: "))
                    to_coordinates = self.tableau_board.find_coordinates_of_next_space(
                        move_to
                    )
                    card_at_destination_coordinates = (
                        self.tableau_board.find_coordinates_of_last_card(move_to)
                    )
                    card_at_destination = self.tableau_board.select_card_on_board(
                        card_at_destination_coordinates
                    )
                    self._apply_rules(card_to_move, card_at_destination)
                    self.tableau_board.remove_card_from_board(from_coordinates)
                    self.tableau_board.place_card_on_board(
                        card=card_to_move, coordinates=to_coordinates
                    )

                reveal_coordinates = self.tableau_board.find_coordinates_of_last_card(
                    move_from
                )
                self.tableau_board.reveal_card_on_board(reveal_coordinates)
                draw_board(self.tableau_board, self.foundation_board)

            except EOFError:
                break

            except ValueError:
                print("Invalid move, try a different one!")
                pass

    def _apply_rules(self, card_to_move: Card, card_at_destination: Card) -> None:
        for rule in self.rules:
            if not rule(card_to_move, card_at_destination):
                raise ValueError()
