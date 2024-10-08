from typing import Callable

from terminal_solitaire.deck import Card, Values

type Rule = Callable[[Card, Card | None], bool]


def alternating_colour_rule(
    card_to_move: Card, card_at_destination: Card | None
) -> bool:
    if card_at_destination is None:
        return True
    elif card_to_move.colour != card_at_destination.colour:
        return True
    else:
        return False


def lower_value_rule(card_to_move: Card, card_at_destination: Card | None) -> bool:
    if card_at_destination is None:
        return True
    else:
        value_index = {value.value: idx for idx, value in enumerate(Values)}
        previous_card_index = value_index[card_at_destination.value]
        current_card_index = value_index[card_to_move.value]

        if previous_card_index - current_card_index == 1:
            return True

        else:
            return False


def king_to_empty_space_rule(
    card_to_move: Card, card_at_destination: Card | None
) -> bool:
    if card_to_move.value is Values.KING and card_at_destination is None:
        return True
    elif card_at_destination is not None:
        return True
    else:
        return False


def check_if_card_is_ace(card: Card) -> bool:
    if card.value is Values.ACE:
        return True
    else:
        return False
