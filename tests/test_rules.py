from terminal_solitaire.deck import Card, Suits, Values
from terminal_solitaire.rules import alternating_colour_rule, lower_value_rule

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
