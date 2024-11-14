from typing import List, Tuple, Optional
import random

from .card import DobbleCard
from .player import Player
from ..config import VALID_CARD_SIZES


class DobbleGame:
    """
    Manages the core game logic for Dobble.

    The game involves players finding matching symbols between their cards and a central card.

    Attributes:
        symbols_per_card (int): Number of symbols on each card.
        cards (List[DobbleCard]): All cards in the game.
        live_card (DobbleCard): The current central card.
        players (List[Player]): List of players in the game.
    """

    def __init__(self, symbols_per_card: int):
        """Initialise a new Dobble game."""

        self.symbols_per_card = symbols_per_card
        self.cards = self._generate_cards()
        self.live_card: Optional[DobbleCard] = None
        self.players: List[Player] = []

    def _generate_cards(self) -> List[DobbleCard]:
        """
        Generate a complete set of Dobble cards ensuring each pair of cards shares exactly one symbol.

        Returns:
            List[DobbleCard]: The generated set of cards.
        """
        n = self.symbols_per_card - 1
        cards = (
            [[i + n**2 for i in range(n + 1)]]
            + [[(o + i * n) for i in range(n)] + [n + n**2] for o in range(n)]
            + [
                [(o * n + i * (p * n + 1)) % (n**2) for i in range(n)] + [p + n**2]
                for p in range(n)
                for o in range(n)
            ]
        )
        return [DobbleCard(set(card)) for card in cards]

    def setup_game(self, player_names: List[str]) -> None:
        """Set up the game by creating players and dealing cards to them."""

        if not player_names:
            raise ValueError("Must provide at least one player name")

        shuffled = self.cards.copy()
        random.shuffle(shuffled)

        self.live_card = shuffled.pop()
        cards_per_player = len(shuffled) // len(player_names)

        self.players = [
            Player(name=name, cards=shuffled[i * cards_per_player:(i + 1) * cards_per_player])
            for i, name in enumerate(player_names)
        ]

    @property
    def is_over(self) -> bool:
        """Check if any player has run out of cards."""
        return any(player.is_out_of_cards for player in self.players)

    def get_symbol_at_coordinate(self, coordinate: str) -> Optional[int]:
        """Get the symbol at the given coordinate on the live card."""
        if not self.live_card:
            return None
        return self.live_card.has_symbol_at_coordinate(coordinate)

    def find_matching_players(self, coordinate: str) -> List[int]:
        """
        Find all players whose top cards match the symbol at the given coordinate.

        Args:
            coordinate (str): The coordinate to check (e.g., 'A1', 'B2').

        Returns:
            List[int]: Indices of all players with matching cards.
        """
        symbol = self.get_symbol_at_coordinate(coordinate)
        if symbol is None:
            return []

        return [i for i, player in enumerate(self.players) if player.has_matching_symbol(symbol)]

    def play_winning_card(self, winner_idx: int) -> None:
        """Move winning card to the centre."""
        player = self.players[winner_idx]
        self.live_card = player.take_top_card()

    def get_game_results(self) -> List[Tuple[str, int]]:
        """Get the final game results for all players."""
        return [(player.name, len(player.cards)) for player in self.players]

    def get_winner(self) -> Optional[str]:
        """Get the name of the winning player, if any."""
        for player in self.players:
            if player.is_out_of_cards:
                return player.name
        return None
