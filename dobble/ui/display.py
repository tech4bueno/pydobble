from rich.columns import Columns
from rich.panel import Panel

from ..game.game import DobbleGame
from .components import create_card_table, console


def display_title():
    title = """[cyan]
╔╦╗╔═╗╔╗ ╔╗ ╦  ╔═╗
 ║║║ ║╠╩╗╠╩╗║  ║╣
═╩╝╚═╝╚═╝╚═╝╩═╝╚═╝
[/cyan]"""
    console.print(title, justify="center")


def display_game_state(game: DobbleGame) -> None:
    """Display the current game state, including the live card and all players' top cards."""
    console.clear()

    if game.live_card:
        console.print(
            Panel(
                create_card_table(game.live_card, show_coordinates=True),
                title="[cyan]Live Card[/cyan]",
                border_style="cyan",
                expand=False,
            )
        )

    player_panels = []
    for player in game.players:
        top_card = player.get_card()
        if top_card:
            card_table = create_card_table(top_card, show_coordinates=False)
            player_panels.append(
                Panel(
                    card_table,
                    title=f"[bold]{player.name}[/bold] ({len(player.cards)} cards)",
                    border_style="green",
                )
            )

    console.print(Columns(player_panels, equal=True, expand=True))
