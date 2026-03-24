# tests/test_game.py
import pytest
from tests.conftest import StubInputHandler
from terminal_solitaire.deck import Card, Suits, Values
from terminal_solitaire.game import (
    Game,
    ActionInputError,
    ColumnInputError,
    EmptyHandError,
    _validate_user_input,
)
from terminal_solitaire.rules import RuleBreakError
from terminal_solitaire.deck import EmptyDeckError


# ── _draw_action ──────────────────────────────────────────────────────────────


def test_draw_action_populates_hand(game: Game) -> None:
    game._draw_action()
    assert not game.hand.is_empty


def test_draw_action_deals_three_cards(game: Game) -> None:
    game._draw_action()
    assert len(game.hand.cards) == 3


def test_draw_action_reduces_deck(game: Game) -> None:
    initial_count = len(game.deck.cards)
    game._draw_action()
    assert len(game.deck.cards) == initial_count - 3


def test_draw_action_cycles_hand_back_to_deck(game: Game) -> None:
    game._draw_action()
    deck_count_after_first_draw = len(game.deck.cards)
    game._draw_action()
    # hand cards should have been reinserted into deck
    assert len(game.deck.cards) == deck_count_after_first_draw


def test_draw_action_empty_deck_and_hand_raises(game: Game) -> None:
    game.deck.cards = []
    with pytest.raises(EmptyDeckError):
        game._draw_action()


def test_draw_action_reveals_top_card_only(game: Game) -> None:
    game._draw_action()
    assert game.hand.cards[0].display_status is True
    assert all(c.display_status is False for c in game.hand.cards[1:])


# ── _hand_action ──────────────────────────────────────────────────────────────


def test_hand_action_empty_hand_raises(game: Game) -> None:
    with pytest.raises(EmptyHandError):
        game._hand_action()


def test_hand_action_to_foundations_valid(game: Game) -> None:
    # seed=42 produces a known deck — place an ace manually to guarantee a valid move
    ace = Card(Suits.HEARTS, Values.ACE, "Red", display_status=True)
    game.hand.draw([ace])
    game.input_handler = StubInputHandler(["f"])
    game._hand_action()
    assert len(game.foundation_board.heart_foundations) == 1


def test_hand_action_to_foundations_invalid_raises(game: Game) -> None:
    # a TWO with an empty foundation should fail
    two = Card(Suits.HEARTS, Values.TWO, "Red", display_status=True)
    game.hand.draw([two])
    game.input_handler = StubInputHandler(["f"])
    with pytest.raises(RuleBreakError):
        game._hand_action()


def test_hand_action_to_tableau_valid(game: Game) -> None:
    eight = Card(Suits.SPADES, Values.EIGHT, "Black", display_status=True)
    seven = Card(Suits.HEARTS, Values.SEVEN, "Red", display_status=True)
    for row in range(game.tableau_board.rows + 1):
        game.tableau_board.remove_card_from_board((row, 0))
    game.tableau_board.place_card_on_board(eight, (0, 0))
    game.hand.draw([seven])
    game.input_handler = StubInputHandler(["t", "0"])
    initial_count = sum(1 for _, _, v in game.tableau_board if isinstance(v, Card))
    game._hand_action()
    new_count = sum(1 for _, _, v in game.tableau_board if isinstance(v, Card))
    assert new_count == initial_count + 1


def test_hand_action_to_tableau_invalid_raises(game: Game) -> None:
    # an ace on a non-empty column that doesn't accept it should fail
    ace = Card(Suits.HEARTS, Values.ACE, "Red", display_status=True)
    game.hand.draw([ace])
    game.input_handler = StubInputHandler(["t", "0"])
    with pytest.raises(RuleBreakError):
        game._hand_action()


def test_hand_action_removes_card_from_hand(game: Game) -> None:
    ace = Card(Suits.HEARTS, Values.ACE, "Red", display_status=True)
    game.hand.draw([ace])
    game.input_handler = StubInputHandler(["f"])
    game._hand_action()
    assert game.hand.is_empty


# ── _foundation_action ────────────────────────────────────────────────────────
def test_foundation_action_valid_move(game: Game) -> None:
    # place an ace at the top of column 0 to guarantee a valid foundation move
    ace = Card(Suits.HEARTS, Values.ACE, "Red", display_status=True)
    coords = game.tableau_board.find_coordinates_of_next_space(0)
    game.tableau_board.place_card_on_board(ace, coords)
    game.input_handler = StubInputHandler(["0"])
    game._foundation_action()
    assert len(game.foundation_board.heart_foundations) == 1


def test_foundation_action_invalid_move_raises(game: Game) -> None:
    # place a TWO on an empty foundation — should fail the rule check
    two = Card(Suits.HEARTS, Values.TWO, "Red", display_status=True)
    coords = game.tableau_board.find_coordinates_of_next_space(0)
    game.tableau_board.place_card_on_board(two, coords)
    game.input_handler = StubInputHandler(["0"])
    with pytest.raises(RuleBreakError):
        game._foundation_action()


def test_foundation_action_reveals_next_card(game: Game) -> None:
    # after moving the top card the card beneath should be revealed
    ace = Card(Suits.HEARTS, Values.ACE, "Red", display_status=True)
    hidden = Card(Suits.SPADES, Values.TWO, "Black", display_status=False)
    coords_hidden = game.tableau_board.find_coordinates_of_next_space(0)
    game.tableau_board.place_card_on_board(hidden, coords_hidden)
    coords_ace = game.tableau_board.find_coordinates_of_next_space(0)
    game.tableau_board.place_card_on_board(ace, coords_ace)
    game.input_handler = StubInputHandler(["0"])
    game._foundation_action()
    assert hidden.display_status is True


# ── _tableau_action ───────────────────────────────────────────────────────────


def test_tableau_action_invalid_move_raises(game: Game) -> None:
    # moving from a column onto itself should fail the rule check
    game.input_handler = StubInputHandler(["0", "1", "0"])
    with pytest.raises(RuleBreakError):
        game._tableau_action()


def test_tableau_action_valid_move_updates_board(game: Game) -> None:
    seven = Card(Suits.HEARTS, Values.SEVEN, "Red", display_status=True)
    eight = Card(Suits.SPADES, Values.EIGHT, "Black", display_status=True)
    for row in range(game.tableau_board.rows + 1):
        game.tableau_board.remove_card_from_board((row, 0))
        game.tableau_board.remove_card_from_board((row, 1))
    game.tableau_board.place_card_on_board(seven, (0, 0))
    game.tableau_board.place_card_on_board(eight, (0, 1))
    game.input_handler = StubInputHandler(
        ["0", "", "1"]
    )  # col, card count (full stack), dest
    game._tableau_action()
    assert game.tableau_board.find_coordinates_of_last_card(1) == (1, 1)


def test_tableau_action_reveals_card_after_move(game: Game) -> None:
    hidden = Card(Suits.CLUBS, Values.NINE, "Black", display_status=False)
    seven = Card(Suits.HEARTS, Values.SEVEN, "Red", display_status=True)
    eight = Card(Suits.SPADES, Values.EIGHT, "Black", display_status=True)
    for row in range(game.tableau_board.rows + 1):
        game.tableau_board.remove_card_from_board((row, 0))
        game.tableau_board.remove_card_from_board((row, 1))
    game.tableau_board.place_card_on_board(hidden, (0, 0))
    game.tableau_board.place_card_on_board(seven, (1, 0))
    game.tableau_board.place_card_on_board(eight, (0, 1))
    game.input_handler = StubInputHandler(["0", "1", "1"])
    game._tableau_action()
    assert hidden.display_status is True


def test_tableau_action_empty_column_raises(game: Game) -> None:
    for row in range(game.tableau_board.rows + 1):
        game.tableau_board.remove_card_from_board((row, 0))
    game.input_handler = StubInputHandler(["0", "1", "1"])
    # empty column has no revealed stack — get_stack_of_revealed_cards returns {}
    # first_card in the action will be None after the stack check
    with pytest.raises((RuleBreakError, ColumnInputError)):
        game._tableau_action()


# ── _check_if_game_won ────────────────────────────────────────────────────────


def test_game_not_won_initially(game: Game) -> None:
    assert game.game_won is False


def test_check_if_game_won_false_with_empty_foundations(game: Game) -> None:
    game._check_if_game_won()
    assert game.game_won is False


def test_check_if_game_won_true_when_all_on_foundations(game: Game) -> None:
    for suit in Suits:
        colour = "Red" if suit in (Suits.HEARTS, Suits.DIAMONDS) else "Black"
        for value in Values:
            card = Card(suit, value, colour, display_status=True)
            game.foundation_board.move_card_to_foundations(card)
    game._check_if_game_won()
    assert game.game_won is True


# ── _apply_rules ──────────────────────────────────────────────────────────────


def test_apply_rules_valid_foundation_ace(game: Game) -> None:
    ace = Card(Suits.HEARTS, Values.ACE, "Red", display_status=True)
    game._apply_rules(ace, None, "f")  # should not raise


def test_apply_rules_invalid_foundation_two(game: Game) -> None:
    two = Card(Suits.HEARTS, Values.TWO, "Red", display_status=True)
    with pytest.raises(RuleBreakError):
        game._apply_rules(two, None, "f")


def test_apply_rules_valid_tableau_move(game: Game) -> None:
    seven = Card(Suits.HEARTS, Values.SEVEN, "Red")
    eight = Card(Suits.SPADES, Values.EIGHT, "Black")
    game._apply_rules(seven, eight, "t")  # should not raise


def test_apply_rules_invalid_tableau_same_colour(game: Game) -> None:
    seven = Card(Suits.HEARTS, Values.SEVEN, "Red")
    eight = Card(Suits.HEARTS, Values.EIGHT, "Red")
    with pytest.raises(RuleBreakError):
        game._apply_rules(seven, eight, "t")


def test_apply_rules_unknown_action_raises(game: Game) -> None:
    ace = Card(Suits.HEARTS, Values.ACE, "Red")
    with pytest.raises(ValueError):
        game._apply_rules(ace, None, "x")


# ── _validate_user_input ──────────────────────────────────────────────────────


def test_validate_valid_actions(game: Game) -> None:
    for action in ["t", "f", "d", "h", "q", "r"]:
        _validate_user_input(action)  # none should raise


def test_validate_invalid_action_raises() -> None:
    with pytest.raises(ActionInputError):
        _validate_user_input("x")


def test_validate_valid_columns() -> None:
    for col in range(7):
        _validate_user_input(col)  # none should raise


def test_validate_invalid_column_raises() -> None:
    with pytest.raises(ColumnInputError):
        _validate_user_input(9)


def test_validate_negative_column_raises() -> None:
    with pytest.raises(ColumnInputError):
        _validate_user_input(-1)
