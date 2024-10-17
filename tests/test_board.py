from terminal_solitaire.board import Board, Tableau, generate_tableau
from terminal_solitaire.deck import Card, build_deck

tableau = generate_tableau(13, 7)


def test_generated_board_is_correct_size() -> None:
    assert tableau.rows == 13 and tableau.columns == 7


def test_board_instance() -> None:
    assert isinstance(tableau, Tableau)


def test_stack_of_revealed_cards() -> None:
    deck = build_deck()
    tableau.deal_initial_tableau(deck)
    revealed_cards = tableau.get_stack_of_revealed_cards(1)
    assert len(revealed_cards.keys()) == 1


def test_number_of_cards_dealt_onto_board() -> None:
    deck = build_deck()
    tableau.deal_initial_tableau(deck)
    dealt_cards = [value for _, _, value in tableau if value != "  "]
    assert len(dealt_cards) == 28


def test_status_of_cards_dealt_onto_board() -> None:
    deck = build_deck()
    tableau.deal_initial_tableau(deck)
    dealt_cards = [value for _, _, value in tableau if value != "  "]
    hidden_cards = [card for card in dealt_cards if card.display_status == False]
    shown_cards = [card for card in dealt_cards if card.display_status == True]
    assert len(hidden_cards) == 21 and len(shown_cards) == 7


def test_find_coordinates_of_last_card_happy_path() -> None:
    deck = build_deck()
    tableau.deal_initial_tableau(deck)
    assert tableau.find_coordinates_of_last_card(6) == (6, 6)


def test_find_coordinates_of_last_card_unhappy_path() -> None:
    empty_tableau = generate_tableau(13, 7)
    assert empty_tableau.find_coordinates_of_last_card(6) == None


def test_find_coordinates_of_next_space() -> None:
    assert tableau.find_coordinates_of_next_space(6) == (7, 6)


def test_select_card_on_board() -> None:
    assert isinstance(tableau.select_card_on_board((0, 0)), Card)


def test_remove_card_from_board() -> None:
    tableau.remove_card_from_board((0, 0))

    assert tableau.board[(0, 0)] == "  "


def test_place_card_on_board() -> None:
    card = Card("test", "test", "test")
    tableau.place_card_on_board(card, (0, 0))
    assert tableau.board[(0, 0)] == card


def test_reveal_card_on_board() -> None:
    tableau.reveal_card_on_board((0, 6))

    assert tableau.board[(0, 6)].display_status == True
