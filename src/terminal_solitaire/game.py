import sys
import time
import random
from terminal_solitaire.board import Foundations, Tableau
from terminal_solitaire.hand import Hand
from terminal_solitaire.config import GameConfig
from terminal_solitaire.renderer import Renderer
from terminal_solitaire.deck import Card, Deck, EmptyDeckError, shuffle_deck
from terminal_solitaire.rules import RuleBreakError, can_move_to_foundations
from terminal_solitaire.input_handler import InputHandler

WELCOME_MESSAGE = """
Welcome to Terminal Solitaire! 

Your goal is to move all cards to the four foundation piles, arranged by suit and ascending rank (Ace to King).
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
        config: GameConfig,
        renderer: Renderer | None = None,
        input_handler: InputHandler | None = None
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
            "q": self._quit_game,
            "r": self._display_rules,
        }
        self.renderer = renderer or Renderer()
        self.input_handler = input_handler or InputHandler(self.renderer)

    def initialise_game(self) -> None:
        if self.config.seed is None:
            self.config.seed = random.randint(0, 10_000_000)
        shuffled = shuffle_deck(self.deck, seed=self.config.seed)
        self.deck = shuffled
        self.tableau_board.deal_initial_tableau(self.deck)

        self.renderer.show_welcome(WELCOME_MESSAGE)
        while True:
            response = self.input_handler.wait_for_enter()
            if response.strip().lower() == "r":
                self.renderer.show_rules(GAME_RULES)
            else:
                break

        self.renderer.start()
        self.renderer.refresh(
            self.tableau_board,
            self.foundation_board,
            self.hand.display(),
            len(self.deck.cards),
            self.config.seed,
        )

    def run_game_loop(self) -> None:
        while not self.game_won:
            try:
                action_input = self.input_handler.get_action()
                _validate_user_input(action_input)
                self.actions[action_input]()
                self.renderer.refresh(
                    self.tableau_board,
                    self.foundation_board,
                    self.hand.display(),
                    len(self.deck.cards),
                    self.config.seed,
                )
                if self._ready_to_clear_board:
                    self._clear_board()

                self._check_if_game_won()

            except (
                ActionInputError,
                ColumnInputError,
                RuleBreakError,
                EmptyHandError,
                EmptyDeckError,
            ) as e:
                self.renderer.show_message(e.args[0])

            except ValueError:
                self.renderer.show_message("Column input must be an integer!")

        self.renderer.stop()
        self.renderer.show_win_message("\nCongratulations, you won!")

    def _apply_rules(
        self, card_to_move: Card, card_at_destination: Card | None, action_input: str
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

        move_from = self.input_handler.get_column("Enter the column of the card to move")
        _validate_user_input(move_from)
        last_card_coordinates = self.tableau_board.find_coordinates_of_last_card(
            move_from
        )
        last_card_on_tableau = self.tableau_board.select_card_on_board(
            last_card_coordinates
        )
        if last_card_coordinates is None or last_card_on_tableau is None:

            raise ColumnInputError(move_from)
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

        move_from = self.input_handler.get_column("Enter the column of the card to move")
        number_of_cards = self.input_handler.get_number_of_cards("Specify number of cards, then press 'Enter' (leave blank to move full stack)")
        _validate_user_input(move_from)
        cards_to_move = self.tableau_board.get_stack_of_revealed_cards(move_from, number_of_cards)
        if not cards_to_move:
            raise ColumnInputError(move_from)
        move_to = self.input_handler.get_column("Enter the destination column")
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

        hand_movement_input = self.input_handler.get_hand_movement()

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
            move_to = self.input_handler.get_column("Enter the destination column")
            _validate_user_input(move_to)
            card_at_destination_coordinates = (
                self.tableau_board.find_coordinates_of_last_card(move_to)
            )
            card_at_destination = self.tableau_board.select_card_on_board(
                card_at_destination_coordinates
            )
            first_card_in_hand = self.hand.top()
            self._apply_rules(
                first_card_in_hand,
                card_at_destination,
                hand_movement_input,
            )
            first_card_in_hand = self.hand.pop()
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
        """Set game status to won if all cards are on foundations."""
        total_on_foundations = sum([
            len(self.foundation_board.spade_foundations),
            len(self.foundation_board.heart_foundations),
            len(self.foundation_board.club_foundations),
            len(self.foundation_board.diamond_foundations),
        ])
        if total_on_foundations == 52:
            self.game_won = True

    @property
    def _ready_to_clear_board(self) -> bool:
        tableau_display_status = [
            value.display_status
            for _, _, value in self.tableau_board
            if isinstance(value, Card)
        ]
        if (
            self.hand.is_empty
            and len(self.deck.cards) == 0
            and all(tableau_display_status)
        ):
            return True

        else:
            return False
    
    def _clear_board(self) -> None:
        """Move all cards from tableau to foundations when all cards are revealed."""
        clear_board_confirmation = self.input_handler.get_clear_board_confirmation()
        
        if clear_board_confirmation == "y":
            progress = True
            while progress and not self.game_won:
                progress = False
                for col in range(self.tableau_board.columns):
                    last_card_coordinates = self.tableau_board.find_coordinates_of_last_card(col)
                    last_card_coordinates = self.tableau_board.find_coordinates_of_last_card(col)
                    last_card_on_tableau = self.tableau_board.select_card_on_board(
                        last_card_coordinates
                    )

                    if last_card_coordinates is None or not isinstance(last_card_on_tableau, Card):
                        continue
                    last_card_on_foundations = self.foundation_board.check_last_card_on_foundations(
                        last_card_on_tableau
                    )
                    can_move = can_move_to_foundations(last_card_on_tableau, last_card_on_foundations, self.config.rules["foundation"])

                    if can_move:
                        self.foundation_board.move_card_to_foundations(last_card_on_tableau)
                        self.tableau_board.remove_card_from_board(last_card_coordinates)
                        reveal_coordinates = self.tableau_board.find_coordinates_of_last_card(col)
                        self.tableau_board.reveal_card_on_board(reveal_coordinates)
                        self.renderer.refresh(
                            self.tableau_board,
                            self.foundation_board,
                            self.hand.display(),
                            len(self.deck.cards),
                            self.config.seed,
                        )
                        time.sleep(0.25)
                        progress = True

                self._check_if_game_won()


    def refresh(self) -> None:
        self.renderer.refresh(
            self.tableau_board,
            self.foundation_board,
            self.hand.display(),
            len(self.deck.cards),
            self.config.seed,
        )

    def _quit_game(self) -> None:
        """Handles operations when quit action is selected by user."""

        user_sure = self.input_handler.get_quit_confirmation()
        if user_sure == "y":
            self.renderer.stop()
            self.renderer.show_quit_message("\nBetter luck next time...")
            sys.exit(0)

    def _display_rules(self) -> None:
        with self.renderer.paused():
                self.renderer.show_rules(GAME_RULES)
                self.input_handler.wait_for_enter()

def _validate_user_input(user_input: str | int) -> None:
    if isinstance(user_input, int) and user_input not in range(7):
        raise ColumnInputError(user_input)
    elif isinstance(user_input, str) and user_input not in ["t", "f", "d", "h", "q", "r"]:
        raise ActionInputError(user_input)

class ActionInputError(Exception):
    def __init__(self, input: str):
        self.input = input
        self.message = (
            f"Action must be 't', 'f', 'd', 'h', 'r' or 'q', not {self.input}"
        )
        super().__init__(self.message)


class EmptyHandError(Exception):
    def __init__(self):
        self.message = "There are no cards in your hand."
        super().__init__(self.message)


class ColumnInputError(Exception):
    def __init__(self, input: int):
        self.input = input
        self.message = (
            f"Column input must be a number between 0 and 6, not {self.input}"
        )
        super().__init__(self.message)
