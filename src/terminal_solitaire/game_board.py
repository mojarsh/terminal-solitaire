import itertools
from dataclasses import dataclass

from terminal_solitaire.deck import Card


@dataclass
class Board:
    rows: int
    columns: int

    def generate_tableau_board(self) -> dict[str | Card]:
        tableau_rows = [_ for _ in range(self.rows + 1)]
        tableau_columns = [_ for _ in range(self.columns)]

        return {
            k: "  " for k in tuple(itertools.product(tableau_rows, tableau_columns))
        }

    def generate_foundations_board(self) -> dict[str | Card]:
        foundation_rows = [_ for _ in range(1)]
        foundation_columns = [_ for _ in range(self.columns)]

        return {
            k: "  "
            for k in tuple(itertools.product(foundation_rows, foundation_columns))
        }


def draw_board(
    foundations_board: dict[tuple : str | Card], tableau_board: dict[tuple : str | Card]
) -> None:
    print("\n    00 01 02 03 04 05 06  ")
    print("  + -------------------- +")
    for i in range(1):
        print("  |", end=" ")
        for k, v in foundations_board.items():
            if k[0] == i and isinstance(v, Card):
                print(v.display_value, end=" ")
            elif k[0] == i and isinstance(v, str):
                print(v, end=" ")
        print("|\r")
    print("  + -------------------- +")
    for i in range(14):
        print(f"{i:02}|", end=" ")
        for k, v in tableau_board.items():
            if k[0] == i and isinstance(v, Card):
                print(v.display_value, end=" ")
            elif k[0] == i and isinstance(v, str):
                print(v, end=" ")
        print("|\r")
    print("  + -------------------- +")


def place_cards_on_tableau(
    dealt_cards: list[list[Card]], tableau: dict[str | Card]
) -> None:
    for row in dealt_cards:
        row_index = dealt_cards.index(row)
        for idx, card in enumerate(row):
            if idx == 0:
                card.display_status = True

            tableau[(row_index, idx + row_index)] = card
