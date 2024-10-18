from terminal_solitaire.board import Foundations, Tableau, draw_board
from terminal_solitaire.deck import Card, Deck, EmptyDeckError, shuffle_deck
from terminal_solitaire.rules import Rule, RuleBreakError


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
        self.hand = None
        self.deck = deck
        self.rules = rules
        self.game_won = False

    def initialise_game(self) -> None:
        shuffled = shuffle_deck(self.deck)
        self.deck = shuffled
        self.tableau_board.deal_initial_tableau(self.deck)
        draw_board(self.tableau_board, self.foundation_board)

    def run_game_loop(self) -> None:
        while not self.game_won:
            try:
                action_input = str(input("\nSelect an action for this turn: ")).strip()
                _validate_user_input(action_input)
                if action_input == "f":
                    move_from = int(input("Enter the column of the card to move: "))
                    _validate_user_input(move_from)
                    last_card_coordinates = (
                        self.tableau_board.find_coordinates_of_last_card(move_from)
                    )
                    last_card_on_tableau = self.tableau_board.select_card_on_board(
                        last_card_coordinates
                    )
                    last_card_on_foundations = (
                        self.foundation_board.check_last_card_on_foundations(
                            last_card_on_tableau
                        )
                    )
                    self._apply_rules(
                        last_card_on_tableau, last_card_on_foundations, action_input
                    )
                    self.foundation_board.move_card_to_foundations(last_card_on_tableau)
                    self.tableau_board.remove_card_from_board(last_card_coordinates)
                    reveal_coordinates = (
                        self.tableau_board.find_coordinates_of_last_card(move_from)
                    )
                    self.tableau_board.reveal_card_on_board(reveal_coordinates)

                elif action_input == "t":
                    self._tableau_movement_pattern(action_input)

                elif action_input == "h":
                    hand_movement_input = str(
                        input(
                            "Enter 'f' to move to foundations, 't' to move to tableau: "
                        )
                    ).strip()
                    if hand_movement_input == "f":
                        first_card_in_hand = self.hand.pop(0)
                        last_card_on_foundations = (
                            self.foundation_board.check_last_card_on_foundations(
                                first_card_in_hand
                            )
                        )
                        self._apply_rules(
                            first_card_in_hand,
                            last_card_on_foundations,
                            hand_movement_input,
                        )
                        self.foundation_board.move_card_to_foundations(
                            first_card_in_hand
                        )
                    elif hand_movement_input == "t":
                        move_to = int(input("Enter the destination column: "))
                        _validate_user_input(move_to)
                        card_at_destination_coordinates = (
                            self.tableau_board.find_coordinates_of_last_card(move_to)
                        )
                        card_at_destination = self.tableau_board.select_card_on_board(
                            card_at_destination_coordinates
                        )
                        first_card_in_hand = self.hand[0]
                        self._apply_rules(
                            first_card_in_hand, card_at_destination, hand_movement_input
                        )
                        first_card_in_hand = self.hand.pop(0)
                        to_coordinates = (
                            self.tableau_board.find_coordinates_of_next_space(move_to)
                        )
                        self.tableau_board.place_card_on_board(
                            first_card_in_hand, coordinates=to_coordinates
                        )
                    for idx, card in enumerate(self.hand):
                        if idx == 0:
                            card.display_status = True
                        else:
                            card.display_status = False

                elif action_input == "d":
                    if self.hand is not None:
                        [self.deck.cards.insert(0, card) for card in self.hand[::-1]]

                    self.hand = self.deck.deal(3)
                    for idx, card in enumerate(self.hand):
                        if idx == 0:
                            card.display_status = True
                        else:
                            card.display_status = False

                draw_board(self.tableau_board, self.foundation_board)
                self._check_if_game_won()
                if self.hand is not None:
                    print(
                        "Hand: ",
                        " ".join([card.display_value for card in self.hand]),
                        f" Cards in deck: {len(self.deck.cards)}",
                    )

            except (
                ActionInputError,
                ColumnInputError,
                RuleBreakError,
                EmptyDeckError,
            ) as e:
                print(e.message)
                pass

            except ValueError:
                print("Column input must be an integer!")
                pass

            except EOFError:
                break

        if self.game_won:
            print("\n Congratulations, you won!")
        else:
            print("\n Better luck next time!")

    def _apply_rules(
        self, card_to_move: Card, card_at_destination: Card, action_input: str
    ) -> None:
        if action_input == "f":
            rules = self.rules["foundation"]
        elif action_input in ["t", "h"]:
            rules = self.rules["tableau"]

        for rule in rules:
            if not rule(card_to_move, card_at_destination):
                raise RuleBreakError

    def _tableau_movement_pattern(self, action_input: str) -> None:
        move_from = int(input("Enter the column of the card to move: "))
        _validate_user_input(move_from)
        cards_to_move = self.tableau_board.get_stack_of_revealed_cards(move_from)
        move_to = int(input("Enter the destination column: "))
        _validate_user_input(move_to)
        card_at_destination_coordinates = (
            self.tableau_board.find_coordinates_of_last_card(move_to)
        )
        card_at_destination = self.tableau_board.select_card_on_board(
            card_at_destination_coordinates
        )
        first_card = next(iter(cards_to_move.values()))
        self._apply_rules(first_card, card_at_destination, action_input)
        for coordinates, card in cards_to_move.items():
            to_coordinates = self.tableau_board.find_coordinates_of_next_space(move_to)
            self.tableau_board.remove_card_from_board(coordinates)
            self.tableau_board.place_card_on_board(card, coordinates=to_coordinates)

        reveal_coordinates = self.tableau_board.find_coordinates_of_last_card(move_from)
        self.tableau_board.reveal_card_on_board(reveal_coordinates)

    def _check_if_game_won(self) -> None:
        combined_foundations = (
            self.foundation_board.spade_foundations
            + self.foundation_board.club_foundations
            + self.foundation_board.heart_foundations
            + self.foundation_board.diamond_foundations
        )

        if len(combined_foundations) == 52:
            self.game_won = True


def _validate_user_input(input: str | int) -> None:
    if isinstance(input, int) and input not in range(0, 10):
        raise ColumnInputError(input)
    elif isinstance(input, str) and input not in ["t", "f", "d", "h"]:
        raise ActionInputError(input)


class ActionInputError(Exception):
    def __init__(self, input: str):
        self.input = input
        self.message = f"Action must be 't', 'f', 'd' or 'h', not {self.input}"


class ColumnInputError(Exception):
    def __init__(self, input: int):
        self.input = input
        self.message = f"Input must be a single digit integer when selecting columns, not {self.input}"
