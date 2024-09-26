from terminal_solitaire.deck import (
    Card,
    Deck,
    Suits,
    _set_card_colour,
    build_deck,
    shuffle_deck,
)

deck = build_deck()
shuffled = shuffle_deck(deck)


def test_deck_class_instance() -> None:
    assert isinstance(deck, Deck)


def test_card_class_instance() -> None:
    assert isinstance(deck.cards[0], Card)


def test_card_display_false_value() -> None:
    card = Card("\u2660", "A", "Black")
    assert card.display_value == 2 * "\u2587"


def test_card_display_true_value() -> None:
    card = Card("\u2660", "A", "Black", True)
    assert card.display_value == "A\u2660"


def test_deck_is_correct_size() -> None:
    deck = build_deck()
    assert len(deck.cards) == 52


def test_shuffled_deck_is_different() -> None:
    assert deck is not shuffled


def test_number_of_dealt_cards() -> None:
    deal = shuffled.deal(7)
    assert len(deal) == 7


def test_set_card_colour_red() -> None:
    assert _set_card_colour(Suits.DIAMONDS) == "Red"


def test_set_card_colour_black() -> None:
    assert _set_card_colour(Suits.SPADES) == "Black"
