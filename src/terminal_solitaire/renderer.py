from terminal_solitaire.board import Tableau, Foundations
from terminal_solitaire.deck import Card

def draw_board(tableau: Tableau, foundations: Foundations) -> None:
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
        print("|", end=" ")
        for row, _, value in tableau:
            if row == i and isinstance(value, Card):
                print(value.display_value, end=" ")
            elif row == i and isinstance(value, str):
                print(value, end=" ")
        print("|\r")
    print("+ -------------------- +")
