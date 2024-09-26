from terminal_solitaire.board import generate_board
from terminal_solitaire.deck import build_deck
from terminal_solitaire.game import Game
from terminal_solitaire.rules import alternating_colour_rule, lower_value_rule


def main() -> None:
    tableau = generate_board(13, 7)
    foundations = generate_board(1, 7)
    deck = build_deck()
    rules = [alternating_colour_rule, lower_value_rule]
    game = Game(tableau, foundations, deck, rules)
    game.initialise_game()
    game.run_game_loop()


if __name__ == "__main__":
    main()
