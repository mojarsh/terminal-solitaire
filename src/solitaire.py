from terminal_solitaire.deck import Deck, deal
from terminal_solitaire.game_board import Board

VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
# Unicode values for each suit, spades, clubs, hearts and diamonds respectively
SUITS = ["\u2660", "\u2663", "\u2661", "\u2662"]
CARD_BACK = "\u2587"


def main() -> None:

    deck = Deck(VALUES, SUITS).shuffle()
    board = Board(7, 13)

    deal_tableau = []
    for x in range(board.columns):
        row_cards = deal(deck=deck, number_of_cards=board.columns - x)
        deal_tableau.append(row_cards)
        for idx, val in enumerate(row_cards):
            if idx == 0:
                board.tableau[(idx + x, x)] = val
            else:
                board.tableau[(idx + x, x)] = 2 * CARD_BACK

    board.draw_board()


if __name__ == "__main__":
    main()
