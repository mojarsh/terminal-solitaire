from typing import Callable

from terminal_solitaire.deck import Card, Values

type Rule = Callable[[Card, Card | None], bool]

def can_move_to_foundations(card: Card, last_on_foundations: Card | None, rules: list[Rule]) -> bool:
    return all(rule(card, last_on_foundations) for rule in rules)

def same_suit_foundation_rule(
        card_to_move: Card, card_at_destination: Card | None
) -> bool:
    if card_at_destination is None:
        return True
    return card_to_move.suit == card_at_destination.suit

def alternating_colour_rule(
    card_to_move: Card, card_at_destination: Card | None
) -> bool:
    if card_at_destination is None:
        return True
    elif card_to_move.colour != card_at_destination.colour:
        return True
    else:
        return False


def higher_value_foundation_rule(
    card_to_move: Card, card_at_destination: Card | None
) -> bool:
    is_ace = _check_if_card_is_ace(card_to_move)
    value_index = {value.value: idx for idx, value in enumerate(Values)}

    if card_at_destination is not None:
        previous_card_index = value_index[card_at_destination.value]
        current_card_index = value_index[card_to_move.value]

        if current_card_index - previous_card_index == 1:
            return True
    elif card_at_destination is None and is_ace:
        return True

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
    if card_to_move.value == Values.KING and card_at_destination is None:
        return True
    elif card_at_destination is not None:
        return True
    else:
        return False


def _check_if_card_is_ace(card: Card | None) -> bool:
    if card is None:
        return False
    elif card.value == Values.ACE:
        return True
    else:
        return False


class RuleBreakError(Exception):
    def __init__(self):
        self.message = "Invalid move, try another one!"
        super().__init__(self.message)

