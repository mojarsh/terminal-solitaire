import pytest
from terminal_solitaire.board import Board, Tableau, generate_tableau
from terminal_solitaire.deck import Card, build_deck



@pytest.fixture
def tableau() -> Tableau:
    return generate_tableau(13, 7)

@pytest.fixture
def dealt_tableau() -> Tableau:
    t = generate_tableau(13, 7)
    t.deal_initial_tableau(build_deck())

    return t

def test_generated_board_is_correct_size(tableau: Tableau) -> None:
    assert tableau.rows == 13 and tableau.columns == 7


def test_board_instance(tableau: Tableau) -> None:
    assert isinstance(tableau, Tableau)


def test_stack_of_revealed_cards(dealt_tableau: Tableau) -> None:
    revealed_cards = dealt_tableau.get_stack_of_revealed_cards(1)
    assert len(revealed_cards.keys()) == 1


def test_number_of_cards_dealt_onto_board(dealt_tableau: Tableau) -> None:
    dealt_cards = [value for _, _, value in dealt_tableau if value != "  "]
    assert len(dealt_cards) == 28


def test_status_of_cards_dealt_onto_board(dealt_tableau: Tableau) -> None:
    dealt_cards = [value for _, _, value in dealt_tableau if isinstance(value, Card)]
    hidden_cards = [card for card in dealt_cards if not card.display_status]
    shown_cards = [card for card in dealt_cards if card.display_status]
    assert len(hidden_cards) == 21 and len(shown_cards) == 7


def test_find_coordinates_of_last_card_happy_path(dealt_tableau: Tableau) -> None:
    assert dealt_tableau.find_coordinates_of_last_card(6) == (6, 6)


def test_find_coordinates_of_last_card_unhappy_path(tableau: Tableau) -> None:
    assert tableau.find_coordinates_of_last_card(6) is None


def test_find_coordinates_of_next_space(dealt_tableau: Tableau) -> None:
    assert dealt_tableau.find_coordinates_of_next_space(6) == (7, 6)


def test_select_card_on_board(dealt_tableau: Tableau) -> None:
    assert isinstance(dealt_tableau.select_card_on_board((0, 0)), Card)


def test_remove_card_from_board(dealt_tableau: Tableau) -> None:
    dealt_tableau.remove_card_from_board((0, 0))

    assert dealt_tableau.board[(0, 0)] == "  "


def test_place_card_on_board(tableau: Tableau) -> None:
    card = Card("test", "test", "test")
    tableau.place_card_on_board(card, (0, 0))
    assert tableau.board[(0, 0)] == card


def test_reveal_card_on_board(dealt_tableau) -> None:
    dealt_tableau.reveal_card_on_board((0, 6))
    if isinstance(dealt_tableau.select_card_on_board((0, 6)), Card):
        assert dealt_tableau.board[(0, 6)].display_status is True
