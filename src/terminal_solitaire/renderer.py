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

def _build_foundations_table(foundations: Foundations) -> Table:
    table = Table(box=box.SIMPLE, padding=(0, 1), show_header=True)
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
    return table

def _build_tableau_table(tableau: Tableau) -> Table:
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
    return table

def build_layout(
    tableau: Tableau,
    foundations: Foundations,
    hand_str: str,
    deck_count: int,
    seed: int | None,
    message: str = "",
) -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="foundations", size=4),
        Layout(name="tableau", size=30),
        Layout(name="status", size=3),
    )
    layout["foundations"].update(_build_foundations_table(foundations))
    layout["tableau"].update(_build_tableau_table(tableau))

    status_parts = [f"Hand: {hand_str}", f"Deck: {deck_count}"]
    if seed is not None:
        status_parts.append(f"Seed: {seed}")
    if message:
        status_parts.append(f"  {message}")

    layout["status"].update(Text("  ·  ".join(status_parts)))
    return layout

class Renderer:
    def __init__(self) -> None:
        self._message: str = ""
        self._live: Live | None = None

    def start(self) -> None:
        self._live = Live(console=console, refresh_per_second=4)
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
        seed: int | None = None,
    ) -> None:
        if self._live:
            layout = build_layout(
                tableau, foundations, hand_str, deck_count, seed, self._message
            )
            self._live.update(layout)
        self._message = ""

    def show_message(self, message: str) -> None:
        self._message = message

    def show_welcome(self, message: str) -> None:
        console.print(message)

    def show_rules(self, rules: str) -> None:
        self.stop()
        console.print(rules)

    def show_quit_message(self, message: str) -> None:
        console.print(message)

    def show_win_message(self, message: str) -> None:
        console.print(message)
