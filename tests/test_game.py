import pytest
import itertools
from typing import List

from dobble.game.game import DobbleGame
from dobble.game.card import DobbleCard
from dobble.game.player import Player
from dobble.config import VALID_CARD_SIZES


@pytest.fixture
def game():
    """Create a basic game instance with 3 symbols per card."""
    return DobbleGame(symbols_per_card=3)

@pytest.fixture
def setup_game():
    """Create a game instance with 3 symbols per card and 2 players."""
    game = DobbleGame(symbols_per_card=3)
    game.setup_game(["Player1", "Player2"])
    return game

@pytest.mark.parametrize("symbols_per_card", VALID_CARD_SIZES)
def test_valid_card_generation(symbols_per_card):
    """Test that generated decks follow the rules of Dobble."""
    game = DobbleGame(symbols_per_card)

    # Test 1: Deck has the correct number of cards
    expected_cards = (symbols_per_card**2) - symbols_per_card + 1
    assert len(game.cards) == expected_cards

    # Test 2: Each card has the correct number of symbols
    for card in game.cards:
        assert len(card.symbols) == symbols_per_card

    # Test 3: Exactly one symbol matches for any two cards
    for card1, card2 in itertools.combinations(game.cards, 2):
        common_symbols = card1.symbols & card2.symbols
        assert len(common_symbols) == 1


class TestDobbleGameInitialization:
    def test_init_valid_symbols(self):
        """Test initialization with valid number of symbols."""
        game = DobbleGame(symbols_per_card=3)
        assert game.symbols_per_card == 3
        assert isinstance(game.cards, list)
        assert all(isinstance(card, DobbleCard) for card in game.cards)
        assert game.live_card is None
        assert game.players == []

    def test_init_invalid_symbols(self):
        """Test initialization with invalid number of symbols."""
        with pytest.raises(ValueError) as exc_info:
            DobbleGame(symbols_per_card=7)
        assert "Invalid number of symbols per card" in str(exc_info.value)

    def test_card_generation_properties(self, game):
        """Test that generated cards follow Dobble properties."""
        cards = game.cards

        # Test each pair of cards shares exactly one symbol
        for i, card1 in enumerate(cards):
            for card2 in cards[i + 1:]:
                common_symbols = card1.symbols & card2.symbols
                assert len(common_symbols) == 1, f"Cards should share exactly one symbol: {card1}, {card2}"

        # Test each card has correct number of symbols
        for card in cards:
            assert len(card.symbols) == game.symbols_per_card

class TestGameSetup:
    def test_setup_game_valid(self, game):
        """Test game setup with valid player names."""
        player_names = ["Alice", "Bob"]
        game.setup_game(player_names)

        assert game.live_card is not None
        assert len(game.players) == 2
        assert all(isinstance(p, Player) for p in game.players)
        assert [p.name for p in game.players] == player_names

        # Check cards are distributed equally
        cards_per_player = len(game.players[0].cards)
        assert all(len(p.cards) == cards_per_player for p in game.players)

    def test_setup_game_empty_players(self, game):
        """Test game setup with empty player list."""
        with pytest.raises(ValueError) as exc_info:
            game.setup_game([])
        assert "Must provide at least one player name" in str(exc_info.value)

    def test_setup_game_shuffled(self, game):
        """Test that cards are shuffled during setup."""
        original_cards = game.cards.copy()
        game.setup_game(["Player1"])

        # Test that either the live card or player cards are in different order
        # Note: There's a tiny chance this could fail randomly
        assert (game.live_card != original_cards[0] or
                game.players[0].cards != original_cards[1:])

class TestGameplay:
    def test_get_symbol_at_coordinate(self, setup_game):
        """Test getting symbol at coordinate."""
        # We can't test specific coordinates as they're randomly assigned
        # but we can test the method returns an integer or None
        coordinate = "A1"
        symbol = setup_game.get_symbol_at_coordinate(coordinate)
        assert isinstance(symbol, (int, type(None)))

    def test_get_symbol_no_live_card(self, game):
        """Test getting symbol when no live card exists."""
        assert game.get_symbol_at_coordinate("A1") is None

    def test_find_matching_players(self, setup_game):
        """Test finding players with matching symbols."""
        # Get a valid symbol from live card
        live_card_symbol = next(iter(setup_game.live_card.symbols))

        # Create a player card that definitely matches
        matching_player_idx = 0
        matching_card = DobbleCard({live_card_symbol, 100, 101})
        setup_game.players[matching_player_idx].cards = [matching_card]

        # Test matching
        matches = setup_game.find_matching_players("A1")  # Coordinate doesn't matter as we mocked the card
        assert matching_player_idx in matches

    def test_play_winning_card(self, setup_game):
        """Test playing a winning card."""
        old_live_card = setup_game.live_card
        winner_idx = 0
        winner_top_card = setup_game.players[winner_idx].cards[0]

        setup_game.play_winning_card(winner_idx)

        assert setup_game.live_card == winner_top_card
        assert setup_game.live_card != old_live_card
        assert len(setup_game.players[winner_idx].cards) == 2

class TestGameEnd:
    def test_is_over_true(self, setup_game):
        """Test game over detection when a player runs out of cards."""
        setup_game.players[0].cards = []
        assert setup_game.is_over

    def test_is_over_false(self, setup_game):
        """Test game over detection when no player has run out of cards."""
        assert not setup_game.is_over

    def test_get_game_results(self, setup_game):
        """Test getting game results."""
        results = setup_game.get_game_results()
        assert len(results) == 2
        assert all(isinstance(r, tuple) and len(r) == 2 for r in results)
        assert all(isinstance(r[0], str) and isinstance(r[1], int) for r in results)

    def test_get_winner_exists(self, setup_game):
        """Test getting winner when one exists."""
        setup_game.players[0].cards = []
        assert setup_game.get_winner() == "Player1"

    def test_get_winner_none(self, setup_game):
        """Test getting winner when none exists."""
        assert setup_game.get_winner() is None
