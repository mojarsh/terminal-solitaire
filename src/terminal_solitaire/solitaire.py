from terminal_solitaire.board import generate_foundations, generate_tableau
from terminal_solitaire.deck import build_deck
from terminal_solitaire.game import Game
from terminal_solitaire.config import GameConfig
def main() -> None:
    tableau = generate_tableau(20, 7)
    foundations = generate_foundations(1, 7)
    deck = build_deck()
    game = Game(tableau, foundations, deck, GameConfig())
    game.initialise_game()
    game.run_game_loop()


if __name__ == "__main__":
    main()
