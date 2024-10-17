from terminal_solitaire.board import generate_foundations, generate_tableau
from terminal_solitaire.deck import build_deck
from terminal_solitaire.game import Game
from terminal_solitaire.rules import (
    alternating_colour_rule,
    higher_value_foundation_rule,
    king_to_empty_space_rule,
    lower_value_rule,
)


def main() -> None:
    tableau = generate_tableau(13, 7)
    foundations = generate_foundations(1, 7)
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
