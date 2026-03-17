from terminal_solitaire.renderer import console, Renderer

class InputHandler:
    def __init__(self, renderer: "Renderer | None" = None) -> None:
        self._renderer = renderer

    def _prompt(self, prompt: str) -> str:
        if self._renderer:
            self._renderer.stop()
        result = console.input(prompt)
        if self._renderer:
            self._renderer.start()
        return result

    def get_action(self) -> str:
        return self._prompt("\nSelect an action for this turn: ").strip()

    def get_column(self, prompt: str) -> int:
        return int(self._prompt(prompt))

    def get_hand_movement(self) -> str:
        return self._prompt("Enter 'f' to move to foundations, 't' to move to tableau: ").strip()

    def get_quit_confirmation(self) -> str:
        return self._prompt("Are you sure you want to quit (y/n): ")

    def wait_for_enter(self) -> None:
        return console.input("\nPress Enter to start, or 'r' to view the rules: ")
