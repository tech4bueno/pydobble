from dataclasses import dataclass
from typing import List, Set, Tuple, Optional
import math
from ..utils.emoji_loader import EMOJI_MAP


@dataclass
class DobbleCard:
    """
    Represents a game card.

    Each card contains a set of symbols with exactly one symbol that matches
    any other given card. Symbols are represented by integers.

    Attributes:
        symbols (Set[int]): Set of integer symbols on the card.
    """

    symbols: Set[int]

    def __str__(self) -> str:
        emoji_symbols = [EMOJI_MAP[s % len(EMOJI_MAP)] for s in sorted(self.symbols)]
        return f"Card({', '.join(emoji_symbols)})"

    def get_symbol_grid(self) -> List[List[Tuple[Optional[int], str]]]:
        """
        Convert the card's symbols into a grid layout for display.

        Returns:
            List[List[Tuple[int, str]]]: A 2D grid where each cell contains
            a tuple of (symbol_number, emoji_character). Empty cells contain (None, " ").
        """
        symbols = sorted(self.symbols)
        size = math.ceil(math.sqrt(len(symbols)))
        grid = []
        idx = 0

        for i in range(size):
            row = []
            for j in range(size):
                if idx < len(symbols):
                    symbol = symbols[idx]
                    emoji = EMOJI_MAP[symbol % len(EMOJI_MAP)]
                    row.append((symbol, emoji))
                else:
                    row.append((None, " "))
                idx += 1
            grid.append(row)

        return grid

    def get_matching_symbol(self, other: "DobbleCard") -> Optional[Tuple[int, str]]:
        """
        Find the matching symbol between this card and another card.

        Args:
            other (DobbleCard): The other card to compare with.

        Returns:
            Tuple[int, str]: A tuple of (symbol_number, emoji_character) if a match is found,
            None otherwise.
        """
        matching_symbols = self.symbols & other.symbols
        if not matching_symbols:
            return None
        matching_num = next(iter(matching_symbols))
        return matching_num, EMOJI_MAP[matching_num % len(EMOJI_MAP)]

    def has_symbol_at_coordinate(self, coordinate: str) -> Optional[int]:
        """
        Check if the card has a symbol at the given coordinate.

        Args:
            coordinate (str): The coordinate to check (e.g., 'A1', 'B2').

        Returns:
            Optional[int]: The symbol at that coordinate, if any.
        """
        try:
            col = ord(coordinate[0].upper()) - ord("A")
            row = int(coordinate[1:]) - 1
            grid = self.get_symbol_grid()
            return grid[row][col][0] if 0 <= row < len(grid) and 0 <= col < len(grid[0]) else None
        except (IndexError, ValueError):
            return None
