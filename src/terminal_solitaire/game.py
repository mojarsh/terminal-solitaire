from terminal_solitaire.board import Foundations, Tableau, draw_board
from terminal_solitaire.deck import Card, Deck, shuffle_deck
from terminal_solitaire.rules import Rule


class Game:
    def __init__(
        self,
        tableau: Tableau,
        foundations: Foundations,
        deck: Deck,
        rules: dict[str : list[Rule]],
    ) -> None:
        self.tableau_board = tableau
        self.foundation_board = foundations
        self.deck = deck
        self.rules = rules

    def initialise_game(self) -> None:
        shuffled = shuffle_deck(self.deck)
        self.tableau_board.deal_initial_tableau(shuffled)
        draw_board(self.tableau_board, self.foundation_board)

    def run_game_loop(self) -> None:
        while True:
            try:
                move_to_foundations = str(input("\nMove card to foundations (Y/N): "))
                move_from = int(input("Enter the column of the card to move: "))
                from_coordinates = self.tableau_board.find_coordinates_of_last_card(
                    move_from
                )
                card_to_move = self.tableau_board.select_card_on_board(from_coordinates)
                if move_to_foundations == "Y":
                    last_card = self.foundation_board.check_last_card_on_foundations(
                        card_to_move
                    )
                    self._apply_rules(card_to_move, last_card, move_to_foundations)
                    self.foundation_board.move_card_to_foundations(card_to_move)
                    self.tableau_board.remove_card_from_board(from_coordinates)

                elif move_to_foundations == "N":
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
                    self._apply_rules(
                        card_to_move, card_at_destination, move_to_foundations
                    )
                    self.tableau_board.remove_card_from_board(from_coordinates)
                    self.tableau_board.place_card_on_board(
                        card=card_to_move, coordinates=to_coordinates
                    )

                else:
                    raise ValueError

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

    def _apply_rules(
        self, card_to_move: Card, card_at_destination: Card, move_to_foundations: str
    ) -> None:
        if move_to_foundations == "Y":
            rules = self.rules["foundation"]
        else:
            rules = self.rules["tableau"]

        for rule in rules:
            if not rule(card_to_move, card_at_destination):
                raise ValueError
