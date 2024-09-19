from terminal_solitaire.deck import Deck

VALUES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
SUITS = ["Spades", "Clubs", "Hearts", "Diamonds"]
deck = Deck(VALUES, SUITS)


def test_deck_class_instance() -> None:
    assert isinstance(deck, Deck)


def test_deck_is_correct_size() -> None:
    assert len(deck.build()) == 52
