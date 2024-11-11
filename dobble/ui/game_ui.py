from typing import List, Optional
from rich.prompt import Prompt, IntPrompt

from ..config import VALID_CARD_SIZES, DIFFICULTY_LEVELS
from ..game.game import DobbleGame
from ..game.player import Player
from .display import display_title, display_game_state
from .input import get_arrow_key_selection, display_difficulty_options
from .components import console


class GameUI:
    """Handles user interface and game flow."""

    @staticmethod
    def select_difficulty() -> int:
        """Get the desired number of symbols per card from the user."""
        options = list(DIFFICULTY_LEVELS.keys()) + ["Custom"]
        selection = get_arrow_key_selection(options, display_difficulty_options)

        if selection < len(DIFFICULTY_LEVELS):
            return list(DIFFICULTY_LEVELS.values())[selection]

        return GameUI._get_custom_difficulty()

    @staticmethod
    def _get_custom_difficulty() -> int:
        """Handle custom difficulty selection."""
        console.clear()
        display_title()
        valid_sizes = ", ".join(map(str, VALID_CARD_SIZES))
        console.print(f"\nValid card sizes: {valid_sizes}")

        while True:
            size = IntPrompt.ask("Enter number of symbols per card")
            if size in VALID_CARD_SIZES:
                return size
            console.print("[red]Invalid size. Please choose from the list above.[/red]")

    @staticmethod
    def get_player_names() -> List[str]:
        """Get player names from user input."""
        names = Prompt.ask("Enter player names (comma-separated)").split(",")
        return [name.strip() for name in names if name.strip()]

    @staticmethod
    def select_winner(matching_players: List[int], players: List[Player]) -> int:
        """Handle winner selection when multiple players have matching symbols."""
        if len(matching_players) == 1:
            return matching_players[0]

        console.print("\n[yellow]More than one player has that symbol![/yellow]")
        console.print("Who spotted the match first?")

        for i, player_idx in enumerate(matching_players, 1):
            console.print(f"{i}. {players[player_idx].name}")

        while True:
            choice = IntPrompt.ask(
                "Enter player number",
                choices=[str(i) for i in range(1, len(matching_players) + 1)],
            )
            if 1 <= choice <= len(matching_players):
                return matching_players[choice - 1]

    @staticmethod
    def display_turn_result(player_name: Optional[str]):
        """Display the result of a player's turn."""
        console.print(f"[green]Well done {player_name}![/green]")

    @staticmethod
    def display_game_results(game: DobbleGame):
        """Display the final game results."""
        console.print("\n[bold yellow]Game Over![/bold yellow]")
        winner = game.get_winner()
        results = game.get_game_results()

        for name, cards_left in results:
            if name == winner:
                console.print(f"[green]{name} was the winner![/green]")
            else:
                console.print(f"{name} had {cards_left} cards left")

