import pytest
from typing import Generator
from contextlib import contextmanager
from terminal_solitaire.board import generate_tableau, generate_foundations
from terminal_solitaire.deck import build_deck, shuffle_deck
from terminal_solitaire.config import GameConfig
from terminal_solitaire.game import Game
from terminal_solitaire.input_handler import InputHandler
from terminal_solitaire.renderer import Renderer


class NoOpRenderer(Renderer):
    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def refresh(self, *args, **kwargs) -> None:
        pass

    def show_message(self, message: str) -> None:
        pass

    def show_welcome(self, message: str) -> None:
        pass

    def show_rules(self, rules: str) -> None:
        pass

    def show_prompt(self, prompt: str) -> None:
        pass

    def show_quit_message(self, message: str) -> None:
        pass

    def show_win_message(self, message: str) -> None:
        pass

    @contextmanager
    def paused(self) -> Generator[None, None, None]:
        yield


class StubInputHandler(InputHandler):
    def __init__(self, responses: list[str]) -> None:
        self._responses = iter(responses)
        self._on_prompt = None
        self._renderer = NoOpRenderer()

    def _next(self) -> str:
        try:
            return next(self._responses)
        except StopIteration:
            raise RuntimeError("StubInputHandler ran out of responses") from None

    def get_action(self) -> str:
        return next(self._responses)

    def get_column(self, prompt: str) -> int:
        return int(next(self._responses))

    def get_number_of_cards(self, prompt: str) -> int | None:
        value = self._next()
        return None if value == "" else int(value)

    def get_hand_movement(self) -> str:
        return next(self._responses)

    def get_quit_confirmation(self) -> str:
        return next(self._responses)

    def wait_for_enter(self) -> str:
        return ""  # simulates user pressing enter


@pytest.fixture
def game() -> Game:
    tableau = generate_tableau(20, 7)
    foundations = generate_foundations(1, 7)
    deck = shuffle_deck(build_deck(), seed=42)
    g = Game(
        tableau,
        foundations,
        deck,
        GameConfig(seed=42),
        input_handler=StubInputHandler([]),
        renderer=NoOpRenderer(),
    )
    # manually deal without starting the renderer
    g.tableau_board.deal_initial_tableau(g.deck)
    return g
