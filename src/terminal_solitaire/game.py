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
                _validate_user_input(move_to_foundations)
                move_from = int(input("Enter the column of the card to move: "))
                _validate_user_input(move_from)
                last_coordinates = self.tableau_board.find_coordinates_of_last_card(
                    move_from
                )
                last_card_to_move = self.tableau_board.select_card_on_board(
                    last_coordinates
                )
                cards_to_move = self.tableau_board.get_stack_of_revealed_cards(
                    move_from
                )
                if move_to_foundations == "Y":
                    last_card = self.foundation_board.check_last_card_on_foundations(
                        last_card_to_move
                    )
                    self._apply_rules(last_card_to_move, last_card, move_to_foundations)
                    self.foundation_board.move_card_to_foundations(last_card_to_move)
                    self.tableau_board.remove_card_from_board(last_coordinates)

                elif move_to_foundations == "N":
                    move_to = int(input("Enter the destination column: "))
                    _validate_user_input(move_to)
                    card_at_destination_coordinates = (
                        self.tableau_board.find_coordinates_of_last_card(move_to)
                    )
                    card_at_destination = self.tableau_board.select_card_on_board(
                        card_at_destination_coordinates
                    )
                    first_card = next(iter(cards_to_move.values()))
                    self._apply_rules(
                        first_card, card_at_destination, move_to_foundations
                    )
                    for coordinates, card in cards_to_move.items():
                        to_coordinates = (
                            self.tableau_board.find_coordinates_of_next_space(move_to)
                        )
                        self.tableau_board.remove_card_from_board(coordinates)
                        self.tableau_board.place_card_on_board(
                            card, coordinates=to_coordinates
                        )

                reveal_coordinates = self.tableau_board.find_coordinates_of_last_card(
                    move_from
                )
                self.tableau_board.reveal_card_on_board(reveal_coordinates)
                draw_board(self.tableau_board, self.foundation_board)

            except (LocationInputError, ColumnInputError) as e:
                print(e.message)
                pass

            except EOFError:
                break

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


def _validate_user_input(input: str | int) -> None:
    if isinstance(input, int) and input not in range(0, 10):
        raise ColumnInputError(input)
    elif isinstance(input, str) and input not in ["Y", "N"]:
        raise LocationInputError(input)


class LocationInputError(Exception):
    def __init__(self, input: str):
        self.input = input
        self.message = (
            f"Input must be 'Y' or 'N' when selecting move location, not {self.input}"
        )


class ColumnInputError(Exception):
    def __init__(self, input: int):
        self.input = input
        self.message = f"Input must be a single digit integer when selecting columns, not {self.input}"
