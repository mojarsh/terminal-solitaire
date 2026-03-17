# tests/conftest.py
import pytest
from terminal_solitaire.board import generate_tableau, generate_foundations
from terminal_solitaire.deck import build_deck, shuffle_deck
from terminal_solitaire.config import GameConfig
from terminal_solitaire.game import Game
from terminal_solitaire.input_handler import InputHandler


class StubInputHandler(InputHandler):
    def __init__(self, responses: list[str]) -> None:
        self._responses = iter(responses)

    def _next(self) -> str:
            try:
                return next(self._responses)
            except StopIteration:
                raise RuntimeError("StubInputHandler ran out of responses") from None

    def get_action(self) -> str:
        return next(self._responses)

    def get_column(self, prompt: str) -> int:
        return int(next(self._responses))

    def get_hand_movement(self) -> str:
        return next(self._responses)

    def get_quit_confirmation(self) -> str:
        return next(self._responses)

    def wait_for_enter(self) -> str:
        return "" # simulates user pressing enter

@pytest.fixture
def game() -> Game:
    tableau = generate_tableau(20, 7)
    foundations = generate_foundations(1, 7)
    deck = shuffle_deck(build_deck(), seed=42)
    g = Game(
        tableau,
        foundations,
        deck,
        GameConfig(),
        input_handler=StubInputHandler([]),
    )
    g.initialise_game()
    return g
