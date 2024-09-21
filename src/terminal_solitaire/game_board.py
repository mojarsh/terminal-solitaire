from terminal_solitaire.deck import Card

CARD_BACK = "\u2587"


class Board:
    def __init__(self, columns: int, rows: int):
        self.columns = columns
        self.rows = rows
        self.tableau = self.generate_tableau_board()
        self.foundations = self.generate_foundations_board()

    def generate_tableau_board(self) -> dict:
        tableau = {}
        for row in range(self.rows):
            for col in range(self.columns):
                tableau[(col, row)] = "  "

        return tableau

    def generate_foundations_board(self) -> dict:
        foundations = {}
        for row in range(1):
            for col in range(self.columns):
                foundations[(col, row)] = "  "

        return foundations

    def draw_board(self) -> None:
        print("\n    00 01 02 03 04 05 06  ")
        print("  + -------------------- +")
        for i in range(1):
            print("  |", end=" ")
            for k, v in self.foundations.items():
                if k[1] == i:
                    print(v, end=" ")
            print("|\r")
        print("  + -------------------- +")
        for i in range(self.rows):
            print(f"{i:02}|", end=" ")
            for k, v in self.tableau.items():
                if k[1] == i:
                    print(v, end=" ")
            print("|\r")
        print("  + -------------------- +")


def assign_tableau_display_icon(
    original_tableau: list[list[Card]], board: Board
) -> None:
    for row in original_tableau:
        row_index = original_tableau.index(row)
        for idx, card in enumerate(row):
            if idx == 0:
                display = card.value + card.suit
            else:
                display = 2 * CARD_BACK

            board.tableau[(idx + row_index, row_index)] = display
