import itertools
from dataclasses import dataclass, field
from typing import Generator

from terminal_solitaire.deck import Card, Deck, Suits


@dataclass
class Foundations:
    spade_foundations: list[Card] = field(default_factory=list)
    heart_foundations: list[Card] = field(default_factory=list)
    club_foundations: list[Card] = field(default_factory=list)
    diamond_foundations: list[Card] = field(default_factory=list)


@dataclass
class Board:
    board: dict[tuple : str | Card]
    rows: int
    columns: int

    def __iter__(self) -> Generator[int, int, str | Card]:
        for key, value in self.board.items():
            row = key[0]
            column = key[1]
            yield row, column, value

    def move_card_to_foundations(self, foundations: Foundations, card: Card) -> None:
        if card.suit == Suits.SPADES:
            foundations.spade_foundations.append(card)
            self.board[(0, 3)] = foundations.spade_foundations[-1]
        elif card.suit == Suits.HEARTS:
            foundations.heart_foundations.append(card)
            self.board[(0, 4)] = foundations.heart_foundations[-1]
        elif card.suit == Suits.CLUBS:
            foundations.club_foundations.append(card)
            self.board[(0, 5)] = foundations.club_foundations[-1]
        elif card.suit == Suits.DIAMONDS:
            foundations.diamond_foundations.append(card)
            self.board[(0, 6)] = foundations.diamond_foundations[-1]

    def deal_initial_tableau(self, deck: Deck) -> None:
        dealt_cards = [
            deck.deal(number_of_cards=self.columns - i) for i in range(self.columns)
        ]
        for row in dealt_cards:
            row_index = dealt_cards.index(row)
            for idx, card in enumerate(row):
                if idx == 0:
                    card.display_status = True

                self.board[(row_index, idx + row_index)] = card

    def find_coordinates_of_last_card(
        self, column_index: int
    ) -> tuple[int, int] | None:
        row_indices = [
            row
            for row, column, value in self
            if column == column_index and isinstance(value, Card)
        ]
        if row_indices != []:
            last_row_index = max(row_indices)
            return (last_row_index, column_index)

        else:
            return None

    def find_coordinates_of_next_space(self, column_index: int) -> tuple[int, int]:
        last_card = self.find_coordinates_of_last_card(column_index)
        if last_card is None:
            return (0, column_index)
        else:
            return (last_card[0] + 1, column_index)

    def select_card_on_board(self, coordinates: tuple[int, int] | None) -> Card | None:
        if coordinates is None:
            return None
        else:
            return self.board[coordinates]

    def remove_card_from_board(self, coordinates: tuple[int, int]) -> None:
        self.board[coordinates] = "  "

    def place_card_on_board(self, card: Card, coordinates: tuple[int, int]) -> None:
        self.board[coordinates] = card

    def reveal_card_on_board(self, coordinates: tuple[int, int] | None) -> None:
        if coordinates is not None:
            card = self.board[coordinates]
            if isinstance(card, Card):
                card.display_status = True


def generate_board(rows: int, columns: int) -> Board:
    element_rows = [_ for _ in range(rows + 1)]
    element_columns = [_ for _ in range(columns)]

    board = {k: "  " for k in tuple(itertools.product(element_rows, element_columns))}
    return Board(board, rows, columns)


def draw_board(tableau: Board, foundations: Board) -> None:
    print("\n  00 01 02 03 04 05 06  ")
    print("+ -------------------- +")
    for i in range(foundations.rows):
        print("|", end=" ")
        for row, _, value in foundations:
            if row == i and isinstance(value, Card):
                print(value.display_value, end=" ")
            elif row == i and isinstance(value, str):
                print(value, end=" ")
        print("|\r")
    print("+ -------------------- +")
    for i in range(tableau.rows + 1):
        print(f"|", end=" ")
        for row, _, value in tableau:
            if row == i and isinstance(value, Card):
                print(value.display_value, end=" ")
            elif row == i and isinstance(value, str):
                print(value, end=" ")
        print("|\r")
    print("+ -------------------- +")
