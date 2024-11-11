from dataclasses import dataclass
from typing import List, Optional

from .card import DobbleCard


@dataclass
class Player:
    """
    Represents a player in the Dobble game.

    Attributes:
        name (str): The player's name.
        cards (List[DobbleCard]): The player's deck of cards.
    """

    name: str
    cards: List[DobbleCard]

    def __str__(self) -> str:
        return f"{self.name} ({len(self.cards)} cards)"

    def get_card(self) -> Optional[DobbleCard]:
        """Get the top card without removing it."""
        return self.cards[0] if self.cards else None

    def take_top_card(self) -> Optional[DobbleCard]:
        """Remove and return the top card."""
        return self.cards.pop(0) if self.cards else None

    def has_matching_symbol(self, symbol: int) -> bool:
        """Check if the player's top card has the given symbol."""
        top_card = self.get_card()
        return symbol in top_card.symbols

    @property
    def is_out_of_cards(self) -> bool:
        """Check if the player has no cards left."""
        return len(self.cards) == 0
