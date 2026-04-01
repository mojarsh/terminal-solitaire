from contextlib import contextmanager
from typing import Generator
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.table import Table
from rich.text import Text
from rich import box

from terminal_solitaire.board import Foundations, Tableau
from terminal_solitaire.deck import Card, Suits


console = Console()


def _card_text(value: str | Card) -> Text:
    """Render a card or empty space as a Rich Text object with colour."""
    if isinstance(value, Card):
        text = Text(value.display_value)
        if value.colour == "Red" and value.display_status:
            text.stylize("bold red")
        return text
    return Text(str(value))


def _build_hand_text(hand_str: str) -> Text:
    text = Text("Hand: ")
    for card in hand_str.split():
        # last character is the suit symbol
        if card[-1] in (Suits.HEARTS, Suits.DIAMONDS):
            text.append(card + " ", style="bold red")
        else:
            text.append(card + " ")
    return text


def _build_foundations_panel(foundations: Foundations) -> Panel:
    table = Table(box=box.SIMPLE, padding=(0, 1), show_header=False)
    for col in range(foundations.columns):
        table.add_column(str(col).zfill(2), justify="center", width=4)

    row_cells: list[Text] = []
    for col in range(foundations.columns):
        found = None
        for row, column, value in foundations:
            if row == 0 and column == col:
                found = value
                break
        row_cells.append(_card_text(found or "  "))
    table.add_row(*row_cells)
    return Panel(table, expand=False)


def _build_tableau_panel(tableau: Tableau) -> Panel:
    table = Table(box=box.SIMPLE, padding=(0, 1), show_header=True)
    for col in range(tableau.columns):
        table.add_column(str(col).zfill(2), justify="center", width=4)

    for i in range(tableau.rows + 1):
        row_cells: list[Text] = []
        for col in range(tableau.columns):
            found = None
            for row, column, value in tableau:
                if row == i and column == col:
                    found = value
                    break
            row_cells.append(_card_text(found or "  "))
        table.add_row(*row_cells)
    return Panel(table, expand=False)


def build_layout(
    tableau: Tableau,
    foundations: Foundations,
    hand_str: str,
    deck_count: int,
    seed: int | None,
    elapsed_time: float,
    message: str = "",
    prompt: str = "Select an action (t/f/d/h/r/q)",
) -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="foundations", size=4),
        Layout(name="tableau", size=24),
        Layout(name="status", size=3),
        Layout(name="prompt", size=3),
    )
    layout["foundations"].update(_build_foundations_panel(foundations))
    layout["tableau"].update(_build_tableau_panel(tableau))
    status = _build_hand_text(hand_str)
    status.append(f"  ·  Deck: {deck_count}")
    status.append(f"  ·  Timer: {round(elapsed_time, 2)}")
    text_prompt = Text(prompt)
    if seed is not None:
        status.append(f"  ·  Seed: {seed}")
    if message:
        text_prompt.append(f": {message}", style="yellow")
    layout["status"].update(Panel(status, expand=False))
    layout["prompt"].update(Panel(text_prompt, expand=False))
    return layout


class Renderer:
    def __init__(self) -> None:
        self._message: str = ""
        self._live: Live | None = None
        self._prompt: str = "Select an action (t/f/d/h/r/q)"

    def start(self) -> None:
        self._live = Live(
            console=console, refresh_per_second=4, vertical_overflow="crop"
        )
        self._live.start()

    def stop(self) -> None:
        if self._live:
            self._live.stop()

    @contextmanager
    def paused(self) -> Generator[None, None, None]:
        self.stop()
        try:
            yield
        finally:
            self.start()

    def refresh(
        self,
        tableau: Tableau,
        foundations: Foundations,
        hand_str: str,
        deck_count: int,
        elapsed_time: float,
        seed: int | None = None,
    ) -> None:
        if self._live:
            layout = build_layout(
                tableau,
                foundations,
                hand_str,
                deck_count,
                seed,
                elapsed_time,
                self._message,
                self._prompt,
            )
            self._live.update(layout)
        self._message = ""

    def show_message(self, message: str) -> None:
        self._message = message

    def show_welcome(self, message: str) -> None:
        console.print(message)

    def show_prompt(self, prompt: str) -> None:
        self._prompt = prompt
        if self._live:
            self._live.refresh()

    def show_rules(self, rules: str) -> None:
        self.stop()
        console.print(rules)

    def show_quit_message(self, message: str) -> None:
        console.print(message)

    def show_win_message(self, message: str) -> None:
        console.print(message)
