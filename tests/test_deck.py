import pytest
from terminal_solitaire.deck import (
    Card,
    Deck,
    Suits,
    _set_card_colour,
    build_deck,
    shuffle_deck,
)


@pytest.fixture
def deck() -> Deck:
    return build_deck()


@pytest.fixture
def shuffled(deck: Deck) -> Deck:
    return shuffle_deck(deck)


def test_deck_class_instance(deck: Deck) -> None:
    assert isinstance(deck, Deck)


def test_card_class_instance(deck: Deck) -> None:
    assert isinstance(deck.cards[0], Card)


def test_card_display_false_value() -> None:
    card = Card("\u2660", "A", "Black")
    assert card.display_value == 2 * "\u2587"


def test_card_display_true_value() -> None:
    card = Card("\u2660", "A", "Black", True)
    assert card.display_value == "A\u2660"


def test_deck_is_correct_size(deck: Deck) -> None:
    assert len(deck.cards) == 52


def test_shuffled_deck_is_different(deck: Deck, shuffled: Deck) -> None:
    assert [c.value + c.suit for c in deck.cards] != [
        c.value + c.suit for c in shuffled.cards
    ]


def test_number_of_dealt_cards(shuffled: Deck) -> None:
    deal = shuffled.deal(7)
    assert len(deal) == 7


def test_set_card_colour_red() -> None:
    assert _set_card_colour(Suits.DIAMONDS) == "Red"


def test_set_card_colour_black() -> None:
    assert _set_card_colour(Suits.SPADES) == "Black"
