from terminal_solitaire.board import Foundations, Tableau
from terminal_solitaire.hand import Hand
from terminal_solitaire.config import GameConfig
from terminal_solitaire.renderer import draw_board
from terminal_solitaire.deck import Card, Deck, EmptyDeckError, shuffle_deck
from terminal_solitaire.rules import Rule, RuleBreakError
import sys

WELCOME_MESSAGE = """
Welcome to Terminal Solitaire! 

Your goal is to move all cards to the four foundation piles, arranged by suit and ascending rank (Ace to King).

Press 'r' if you need to see the rules and controls.
"""

GAME_RULES = """
Rules:

 - Move face-up tableau cards onto opposite-colour cards of one-higher rank
 - Sequences of descending, alternating-colour cards can be moved together
 - Empty tableau spots can only be filled by Kings or sequences starting with Kings
 - Draw cards from the deck to play when no other moves are possible

Controls:

 - Use 'd' to draw from the deck
 - Use 'h' to access your hand
 - Use 't' to place cards on the tableau
 - Use 'f' to place cards on the foundations
 - Use 'r' for a reminder of these rules and controls
 - Use 'q' to quit the game
"""


class Game:
    def __init__(
        self,
        tableau: Tableau,
        foundations: Foundations,
        deck: Deck,
        config: GameConfig
    ) -> None:
        self.tableau_board = tableau
        self.foundation_board = foundations
        self.hand = Hand()
        self.deck = deck
        self.config = config
        self.game_won = False
        self.actions = {
            "f": self._foundation_action,
            "t": self._tableau_action,
            "h": self._hand_action,
            "d": self._draw_action,
            "q": _quit_game,
            "r": _display_rules,
        }

    def initialise_game(self) -> None:
        shuffled = shuffle_deck(self.deck)
        self.deck = shuffled
        self.tableau_board.deal_initial_tableau(self.deck)
        print(WELCOME_MESSAGE)
        draw_board(self.tableau_board, self.foundation_board)

    def run_game_loop(self) -> None:
        while not self.game_won:
            try:
                action_input = str(input("\nSelect an action for this turn: ")).strip()
                _validate_user_input(action_input)
                self.actions[action_input]()
                draw_board(self.tableau_board, self.foundation_board)
                self._check_if_game_won()
                print(
                    f"Hand: {self.hand.display()}",
                    f" Cards in deck: {len(self.deck.cards)}",
                )

            except (
                ActionInputError,
                ColumnInputError,
                RuleBreakError,
                EmptyHandError,
                EmptyDeckError,
            ) as e:
                print(e.message)
                pass

            except ValueError:
                print("Column input must be an integer!")
                pass

        if self.game_won:
            print("\nCongratulations, you won!")

    def _apply_rules(
        self, card_to_move: Card, card_at_destination: Card, action_input: str
    ) -> None:
        if action_input == "f":
            rules = self.config.rules["foundation"]
        elif action_input in ["t", "h"]:
            rules = self.config.rules["tableau"]
        else:
            raise ValueError(f"Unknown action input for rules: {action_input!r}")

        for rule in rules:
            if not rule(card_to_move, card_at_destination):
                raise RuleBreakError

    def _foundation_action(self) -> None:
        """Handles operations when foundation action is selected by user."""

        move_from = int(input("Enter the column of the card to move: "))
        _validate_user_input(move_from)
        last_card_coordinates = self.tableau_board.find_coordinates_of_last_card(
            move_from
        )
        last_card_on_tableau = self.tableau_board.select_card_on_board(
            last_card_coordinates
        )
        last_card_on_foundations = self.foundation_board.check_last_card_on_foundations(
            last_card_on_tableau
        )
        self._apply_rules(last_card_on_tableau, last_card_on_foundations, "f")
        self.foundation_board.move_card_to_foundations(last_card_on_tableau)
        self.tableau_board.remove_card_from_board(last_card_coordinates)
        reveal_coordinates = self.tableau_board.find_coordinates_of_last_card(move_from)
        self.tableau_board.reveal_card_on_board(reveal_coordinates)

    def _tableau_action(self) -> None:
        """Handles operations when tableau action is selected by user."""

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
        self._apply_rules(first_card, card_at_destination, "t")
        for coordinates, card in cards_to_move.items():
            to_coordinates = self.tableau_board.find_coordinates_of_next_space(move_to)
            self.tableau_board.remove_card_from_board(coordinates)
            self.tableau_board.place_card_on_board(card, coordinates=to_coordinates)

        reveal_coordinates = self.tableau_board.find_coordinates_of_last_card(move_from)
        self.tableau_board.reveal_card_on_board(reveal_coordinates)

    def _hand_action(self) -> None:
        """Handles operations when hand action is selected by user."""

        if self.hand.is_empty:
            raise EmptyHandError

        hand_movement_input = str(
            input("Enter 'f' to move to foundations, 't' to move to tableau: ")
        ).strip()

        if hand_movement_input == "f":
            first_card_in_hand = self.hand.top()
            last_card_on_foundations = (
                self.foundation_board.check_last_card_on_foundations(first_card_in_hand)
            )
            self._apply_rules(
                first_card_in_hand,
                last_card_on_foundations,
                hand_movement_input,
            )
            self.hand.pop()
            self.foundation_board.move_card_to_foundations(first_card_in_hand)
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
                first_card_in_hand,
                card_at_destination,
                hand_movement_input,
            )
            first_card_in_hand = self.hand.pop(0)
            to_coordinates = self.tableau_board.find_coordinates_of_next_space(move_to)
            self.tableau_board.place_card_on_board(
                first_card_in_hand, coordinates=to_coordinates
            )


    def _draw_action(self) -> None:
        """Handles operations when draw action is selected by user."""
        if len(self.deck.cards) == 0 and self.hand.is_empty:
            raise EmptyDeckError

        if not self.hand.is_empty:
            self.hand.return_to_deck(self.deck)

        self.hand.draw(self.deck.deal(3))

    def _check_if_game_won(self) -> None:
        """Set game won status to True when hand and deck are empty and all cards on tableau are revealed."""
        tableau_display_status = [
            value.display_status
            for _, _, value in self.tableau_board
            if isinstance(value, Card)
        ]
        if (
            self.hand == []
            and len(self.deck.cards) == 0
            and all(tableau_display_status)
        ):
            self.game_won = True

def _display_rules() -> None:
    print(GAME_RULES)


def _quit_game() -> None:
    """Handles operations when quit action is selected by user."""

    user_sure = input("Are you sure you want to quit (y/n): ")
    if user_sure == "y":
        print("\nBetter luck next time...")
        sys.exit(0)


def _validate_user_input(input: str | int) -> None:
    if isinstance(input, int) and input not in range(7):
        raise ColumnInputError(input)
    elif isinstance(input, str) and input not in ["t", "f", "d", "h", "q", "r"]:
        raise ActionInputError(input)


class ActionInputError(Exception):
    def __init__(self, input: str):
        self.input = input
        self.message = (
            f"Action must be 't', 'f', 'd', 'h', 'r' or 'q', not {self.input}"
        )


class EmptyHandError(Exception):
    def __init__(self):
        self.message = "There are no cards in your hand."


class ColumnInputError(Exception):
    def __init__(self, input: int):
        self.input = input
        self.message = (
            f"Column input must be a number between 0 and 6, not {self.input}"
        )
