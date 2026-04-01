import argparse
import sys
from terminal_solitaire.board import generate_foundations, generate_tableau
from terminal_solitaire.deck import build_deck
from terminal_solitaire.game import Game
from terminal_solitaire.config import GameConfig
from terminal_solitaire.renderer import Renderer
from terminal_solitaire.input_handler import InputHandler
from terminal_solitaire.stats import show_stats_summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Terminal Solitaire")
    parser.add_argument(
        "--seed", type=int, default=None, help="Seed for reproducible deals"
    )
    parser.add_argument(
        "--stats", action="store_true", help="Game statistics for the user"
    )
    args = parser.parse_args()

    config = GameConfig(seed=args.seed)

    if args.stats:
        show_stats_summary(config.stats_path)
        sys.exit(0)

    tableau = generate_tableau(20, 7)
    foundations = generate_foundations(1, 7)
    deck = build_deck()
    renderer = Renderer()
    game = Game(tableau, foundations, deck, config, renderer)
    input_handler = InputHandler(
        renderer,
        on_prompt=lambda _: game.refresh(),
    )
    game.input_handler = input_handler
    game.initialise_game()
    game.run_game_loop()


if __name__ == "__main__":
    main()
