import blessed
from typing import Callable
from terminal_solitaire.renderer import console, Renderer

term = blessed.Terminal()

class InputHandler:
    def __init__(self, renderer: Renderer, on_prompt: Callable[[str], None] | None = None) -> None:
        self._renderer = renderer
        self._on_prompt = on_prompt

    def _show_and_refresh(self, prompt: str) -> None:
        self._renderer.show_prompt(prompt)
        if self._on_prompt:
            self._on_prompt(prompt)

    def get_action(self) -> str:
        self._show_and_refresh("Select an action (t/f/d/h/r/q)")
        with term.cbreak():
            return str(term.inkey())

    def get_column(self, prompt: str) -> int:
        self._show_and_refresh(prompt)
        with term.cbreak():
            return int(str(term.inkey()))

    def get_number_of_cards(self, prompt: str) -> int | None:
        self._show_and_refresh(prompt)
        number_input: list[str] = []
        with term.cbreak():
            key = term.inkey()
            while key.name != "KEY_ENTER":
                if key.name == "KEY_BACKSPACE" and number_input:
                    number_input.pop()
                elif str(key).isdigit():
                    number_input.append(str(key))
                # update prompt to show what's been typed so far
                self._show_and_refresh(f"{prompt} {''.join(number_input)}")
                key = term.inkey()
        return int("".join(number_input)) if number_input else None

    def get_hand_movement(self) -> str:
        self._show_and_refresh("Select destination (f/t)")
        with term.cbreak():
            return str(term.inkey())

    def get_quit_confirmation(self) -> str:
        self._show_and_refresh("Are you sure you want to quit? (y/n)")
        with term.cbreak():
            return str(term.inkey())

    def wait_for_enter(self) -> str:
        return console.input("\nPress Enter to start, or 'r' to view the rules")

