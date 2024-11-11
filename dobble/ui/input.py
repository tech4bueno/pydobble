import sys
import tty
import termios
from typing import List, Callable

from rich.table import Table
from rich.style import Style
from rich.text import Text
from rich import box

from ..config import DIFFICULTY_LEVELS
from .components import console
from .display import display_title


def get_arrow_key_selection(
    options: List[str], display_func: Callable[[int], None]
) -> int:
    """
    Handle arrow key selection from a list of options.

    Args:
        options: List of options to choose from
        display_func: Function to display the current state

    Returns:
        Selected index
    """

    def get_key():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ch == "\x1b":
                ch = sys.stdin.read(2)
                return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    current_selection = 0

    while True:
        console.clear()
        display_func(current_selection)

        key = get_key()

        if key == "[A":  # Up arrow
            current_selection = (current_selection - 1) % len(options)
        elif key == "[B":  # Down arrow
            current_selection = (current_selection + 1) % len(options)
        elif key == "\r":  # Enter key
            return current_selection


def display_difficulty_options(current_selection: int) -> None:
    """Display difficulty options in a table format with the current selection highlighted."""
    display_title()

    console.print(
        "\n[bold yellow]Select Difficulty (Use ↑↓ arrows, Enter to select):[/bold yellow]\n"
    )

    table = Table(box=box.ROUNDED, show_header=True)
    table.add_column("Difficulty Level", style="cyan")
    table.add_column("Symbols per Card", justify="center", style="green")

    for i, (level, size) in enumerate(DIFFICULTY_LEVELS.items()):
        style = Style(bgcolor="blue", color="white") if i == current_selection else None
        level_text = Text(level, style=style)
        size_text = Text(str(size), style=style)
        table.add_row(level_text, size_text)

    # Add Custom option
    style = (
        Style(bgcolor="blue", color="white")
        if current_selection == len(DIFFICULTY_LEVELS)
        else None
    )
    custom_text = Text("Custom", style=style)
    custom_size = Text("Choose your own", style=style)
    table.add_row(custom_text, custom_size)

    console.print(table)
