import itertools
from dataclasses import dataclass

from terminal_solitaire.deck import Card, Deck


@dataclass
class BoardElement:
    board: dict[tuple : str | Card]
    rows: int
    columns: int


def generate_board_element(rows: int, columns: int) -> BoardElement:
    element_rows = [_ for _ in range(rows + 1)]
    element_columns = [_ for _ in range(columns)]

    board = {k: "  " for k in tuple(itertools.product(element_rows, element_columns))}
    return BoardElement(board, rows, columns)


@dataclass
class Board:
    foundations: BoardElement
    tableau: BoardElement

    def deal_initial_tableau(self, deck: Deck) -> list[list[Card]]:
        return [
            deck.deal(number_of_cards=self.tableau.columns - i)
            for i in range(self.tableau.columns)
        ]

    def find_last_card_in_tableau_column(self, column_index: int) -> tuple[int, int]:
        row_indices = [
            k[0]
            for k, v in self.tableau.board.items()
            if k[1] == column_index and isinstance(v, Card)
        ]
        last_row_index = max(row_indices)

        return (last_row_index, column_index)

    def find_next_free_space_in_tableau_column(
        self, column_index: int
    ) -> tuple[int, int]:
        last_card = self.find_last_card_in_tableau_column(column_index)
        return (last_card[0] + 1, column_index)

    def select_card_on_tableau(self, coordinates: tuple[int, int]) -> Card:
        return self.tableau.board[coordinates]

    def remove_card_on_tableau(self, coordinates: tuple[int, int]) -> None:
        self.tableau.board[coordinates] = "  "

    def place_card_on_tableau(self, card: Card, coordinates: tuple[int, int]) -> None:
        self.tableau.board[coordinates] = card

    def reveal_card_on_tableau(self, coordinates: tuple[int, int]) -> None:
        card = self.tableau.board[coordinates]
        card.display_status = True


def draw_board(board: Board) -> None:
    print("\n  00 01 02 03 04 05 06  ")
    print("+ -------------------- +")
    for i in range(board.foundations.rows):
        print("|", end=" ")
        for k, v in board.foundations.board.items():
            if k[0] == i and isinstance(v, Card):
                print(v.display_value, end=" ")
            elif k[0] == i and isinstance(v, str):
                print(v, end=" ")
        print("|\r")
    print("+ -------------------- +")
    for i in range(board.tableau.rows + 1):
        print(f"|", end=" ")
        for k, v in board.tableau.board.items():
            if k[0] == i and isinstance(v, Card):
                print(v.display_value, end=" ")
            elif k[0] == i and isinstance(v, str):
                print(v, end=" ")
        print("|\r")
    print("+ -------------------- +")


def place_cards_on_tableau(
    dealt_cards: list[list[Card]], tableau: BoardElement
) -> None:
    for row in dealt_cards:
        row_index = dealt_cards.index(row)
        for idx, card in enumerate(row):
            if idx == 0:
                card.display_status = True

            tableau[(row_index, idx + row_index)] = card
