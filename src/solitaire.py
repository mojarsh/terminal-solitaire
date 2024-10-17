from terminal_solitaire.board import generate_board
from terminal_solitaire.deck import build_deck
from terminal_solitaire.game import Game
from terminal_solitaire.rules import (
    alternating_colour_rule,
    higher_value_foundation_rule,
    king_to_empty_space_rule,
    lower_value_rule,
)


def main() -> None:
    tableau = generate_board(13, 7, True)
    foundations = generate_board(1, 7, False)
    deck = build_deck()
    rules = {
        "foundation": [higher_value_foundation_rule],
        "tableau": [
            alternating_colour_rule,
            lower_value_rule,
            king_to_empty_space_rule,
        ],
    }
    game = Game(tableau, foundations, deck, rules)
    game.initialise_game()
    game.run_game_loop()


if __name__ == "__main__":
    main()
