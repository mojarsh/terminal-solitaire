from terminal_solitaire.deck import Card, Suits, Values
from terminal_solitaire.rules import (
    alternating_colour_rule,
    lower_value_rule,
    higher_value_foundation_rule,
    king_to_empty_space_rule,
    same_suit_foundation_rule,
)

jack_of_hearts = Card(Suits.HEARTS, Values.JACK, "Red")
eight_of_clubs = Card(Suits.CLUBS, Values.EIGHT, "Black")
seven_of_diamonds = Card(Suits.DIAMONDS, Values.SEVEN, "Red")
queen_of_spades = Card(Suits.SPADES, Values.QUEEN, "Black")


def test_alternating_colour_rule_happy_path() -> None:
    assert alternating_colour_rule(seven_of_diamonds, eight_of_clubs) is True


def test_alternating_colour_rule_unhappy_path() -> None:
    assert alternating_colour_rule(seven_of_diamonds, jack_of_hearts) is False


def test_lower_value_rule_happy_path() -> None:
    assert lower_value_rule(seven_of_diamonds, eight_of_clubs) is True


def test_lower_value_rule_unhappy_path() -> None:
    assert lower_value_rule(eight_of_clubs, queen_of_spades) is False


def test_higher_value_foundation_rule_happy_path() -> None:
    assert (
        higher_value_foundation_rule(
            Card(Suits.HEARTS, Values.TWO, "Red"), jack_of_hearts
        )
        is False
    )


def test_higher_value_foundation_rule_ace() -> None:
    ace = Card(Suits.HEARTS, Values.ACE, "Red")
    assert higher_value_foundation_rule(ace, None) is True


def test_higher_value_foundation_rule_sequence() -> None:
    two = Card(Suits.HEARTS, Values.TWO, "Red")
    ace = Card(Suits.HEARTS, Values.ACE, "Red")
    assert higher_value_foundation_rule(two, ace) is True


def test_king_to_empty_space_rule_king_empty() -> None:
    king = Card(Suits.SPADES, Values.KING, "Black")
    assert king_to_empty_space_rule(king, None) is True


def test_king_to_empty_space_rule_non_king_empty() -> None:
    assert king_to_empty_space_rule(eight_of_clubs, None) is False


def test_king_to_empty_space_rule_non_empty() -> None:
    assert king_to_empty_space_rule(eight_of_clubs, jack_of_hearts) is True


def test_same_suit_foundation_rule_happy_path() -> None:
    assert same_suit_foundation_rule(seven_of_diamonds, jack_of_hearts) is False


def test_same_suit_foundation_rule_empty_foundation() -> None:
    assert same_suit_foundation_rule(seven_of_diamonds, None) is True


def test_same_suit_foundation_rule_matching_suit() -> None:
    two_of_hearts = Card(Suits.HEARTS, Values.TWO, "Red")
    assert same_suit_foundation_rule(two_of_hearts, jack_of_hearts) is True
