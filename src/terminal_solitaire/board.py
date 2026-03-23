import itertools
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Generator

from terminal_solitaire.deck import Card, Deck, Suits


@dataclass
class Board(ABC):
    board: dict[tuple[int, int], str | Card]
    rows: int
    columns: int

    @abstractmethod
    def __iter__(self) -> Generator[tuple[int, int, str | Card]]:
        pass


@dataclass
class Foundations(Board):
    spade_foundations: list[Card] = field(default_factory=list)
    heart_foundations: list[Card] = field(default_factory=list)
    club_foundations: list[Card] = field(default_factory=list)
    diamond_foundations: list[Card] = field(default_factory=list)

    def __iter__(self) -> Generator[tuple[int, int, str | Card], None, None]:
        for key, value in self.board.items():
            row = key[0]
            column = key[1]
            yield row, column, value

    def check_last_card_on_foundations(self, card: Card) -> Card | None:
        try:
            if card.suit == Suits.SPADES:
                return self.spade_foundations[-1]
            elif card.suit == Suits.HEARTS:
                return self.heart_foundations[-1]
            elif card.suit == Suits.CLUBS:
                return self.club_foundations[-1]
            elif card.suit == Suits.DIAMONDS:
                return self.diamond_foundations[-1]
        except (IndexError, AttributeError):
            return None

    def move_card_to_foundations(self, card: Card) -> None:
        card.display_status = True
        if card.suit == Suits.SPADES:
            self.spade_foundations.append(card)
            self.board[(0, 3)] = self.spade_foundations[-1]
        elif card.suit == Suits.HEARTS:
            self.heart_foundations.append(card)
            self.board[(0, 4)] = self.heart_foundations[-1]
        elif card.suit == Suits.CLUBS:
            self.club_foundations.append(card)
            self.board[(0, 5)] = self.club_foundations[-1]
        elif card.suit == Suits.DIAMONDS:
            self.diamond_foundations.append(card)
            self.board[(0, 6)] = self.diamond_foundations[-1]


@dataclass
class Tableau(Board):
    def __iter__(self) -> Generator[tuple[int, int, str | Card], None, None]:
        for key, value in self.board.items():
            row = key[0]
            column = key[1]
            yield row, column, value

    def deal_initial_tableau(self, deck: Deck) -> None:
        dealt_cards = [
            deck.deal(number_of_cards=self.columns - i) for i in range(self.columns)
        ]
        for row_index, row in enumerate(dealt_cards):
            for idx, card in enumerate(row):
                if idx == 0:
                    card.display_status = True

                self.board[(row_index, idx + row_index)] = card

    def get_first_card_coordinates(self, column_index: int, row_offset: int | None = None) -> tuple[int, int] | None:

        row_indices = [
            row
            for row, column, value in self
            if column == column_index
            and isinstance(value, Card)
            and value.display_status
        ]
        if row_indices != []:
            if row_offset is None:
                first_row_index = min(row_indices)
                return (first_row_index, column_index)

            # row_offset is the number of cards to be moved
            # adjusted_offset accounts for 0 indexing of row_indices
            adjusted_offset = row_offset - 1
            first_row_index = max(row_indices) - adjusted_offset
            return (first_row_index, column_index)

        return None

    def get_stack_of_revealed_cards(self, column_index: int, row_index: int | None = None) -> dict[tuple[int, int], Card | str]:
        first_card = self.get_first_card_coordinates(column_index, row_index)
        last_card = self.find_coordinates_of_last_card(column_index)
        if first_card is None or last_card is None:
            return {}
        coordinate_list = [
            (i, column_index) for i in range(first_card[0], last_card[0] + 1)
        ]
        return {
            c: card
            for c in coordinate_list
            if (card := self.select_card_on_board(c)) is not None
        }

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

    def select_card_on_board(self, coordinates: tuple[int, int] | None) -> Card | str | None:
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


def generate_tableau(rows: int, columns: int) -> Tableau:
    element_rows = [_ for _ in range(rows + 1)]
    element_columns = [_ for _ in range(columns)]

    board: dict[tuple[int, int], str | Card] = {
        k: "  " for k in tuple(itertools.product(element_rows, element_columns))
    }
    return Tableau(board, rows, columns)


def generate_foundations(rows: int, columns: int) -> Foundations:
    element_rows = [_ for _ in range(rows + 1)]
    element_columns = [_ for _ in range(columns)]

    board: dict[tuple[int, int], str | Card] = {
        k: "  " for k in tuple(itertools.product(element_rows, element_columns))
    }
    return Foundations(board, rows, columns)


def clear_board(tableau: Tableau, foundations: Foundations) -> None:
    """ "Move all cards from tableau to foundations when game is won."""
    return None
