import sys
from typing import Optional, List

from rich.prompt import Prompt

from .game.game import DobbleGame
from .ui.game_ui import GameUI
from .ui.display import display_title, display_game_state
from .ui.components import console


class GameController:
    """
    Controls the game flow and coordinates between the game logic and UI.
    """

    def __init__(self):
        self.ui = GameUI()
        self.game: Optional[DobbleGame] = None

    def setup_new_game(self) -> None:
        """Initialise a new game with user-selected options."""
        symbols_per_card = self.ui.select_difficulty()
        self.game = DobbleGame(symbols_per_card=symbols_per_card)

        player_names = self.ui.get_player_names()
        self.game.setup_game(player_names)

    def run_game_turn(self) -> None:
        """Handle a single game turn."""
        display_game_state(self.game)

        coordinate = Prompt.ask("\nEnter coordinate of the matching symbol (e.g. B2), or 'q' to quit")
        if coordinate.lower() == "q":
            sys.exit(0)

        matching_players = self.game.find_matching_players(coordinate)
        if not matching_players:
            console.print("[red]Nobody has that symbol.[/red]")
            return

        winner_idx = self.ui.select_winner(matching_players, self.game.players)
        self.game.play_winning_card(winner_idx)

        player_name = self.game.players[winner_idx].name
        self.ui.display_turn_result(player_name)

    def run_game(self) -> None:
        """Run the main game loop."""
        console.clear()
        display_title()

        self.setup_new_game()

        while not self.game.is_over:
            self.run_game_turn()

            if not self.game.is_over:
                console.input("\nPress Enter to continue...")

        self.ui.display_game_results(self.game)


def main():
    """Entry point for the game."""
    controller = GameController()
    controller.run_game()


if __name__ == "__main__":
    main()
