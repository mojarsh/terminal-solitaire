from terminal_solitaire.deck import Deck

VALUES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
# Unicode values for each suit, spades, clubs, hearts and diamonds respectively
SUITS = ["\u2660", "\u2663", "\u2661", "\u2662"]

deck = Deck(VALUES, SUITS).shuffle()

for card in deck:
    print(card)
