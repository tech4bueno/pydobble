import pytest

from dobble.game.card import DobbleCard


@pytest.fixture
def emoji_map(monkeypatch):
    """Fixture to provide a consistent emoji map for testing"""
    test_emoji_map = {0: "😀", 1: "😂", 2: "😊", 3: "😎", 4: "🤔", 5: "😴"}
    monkeypatch.setattr("dobble.game.card.EMOJI_MAP", test_emoji_map)
    return test_emoji_map


@pytest.fixture
def sample_cards():
    """Fixture providing various card configurations for testing"""
    return {
        "standard": DobbleCard({0, 1, 2}),
        "matching": DobbleCard({1, 3, 4}),
        "non_matching": DobbleCard({5, 6, 7}),
        "empty": DobbleCard(set()),
        "large": DobbleCard({0, 1, 2, 3, 4, 5, 6, 7, 8}),
    }


def test_init():
    """Test DobbleCard initialization"""
    symbols = {1, 2, 3}
    card = DobbleCard(symbols)
    assert card.symbols == symbols
    assert isinstance(card.symbols, set)


@pytest.mark.parametrize(
    "symbols,expected_str",
    [
        ({0, 1, 2}, "Card(😀, 😂, 😊)"),
        (set(), "Card()"),
        ({6, 7, 8}, "Card(😀, 😂, 😊)"),  # Testing wraparound
    ],
)
def test_str_representation(emoji_map, symbols, expected_str):
    """Test string representation of cards with different configurations"""
    card = DobbleCard(symbols)
    assert str(card) == expected_str


def test_get_symbol_grid(sample_cards):
    """Test grid generation functionality"""
    # Test 3-symbol card (should create 2x2 grid)
    grid = sample_cards["standard"].get_symbol_grid()
    assert len(grid) == 2  # 2 rows
    assert len(grid[0]) == 2  # 2 columns

    # Test empty card
    empty_grid = sample_cards["empty"].get_symbol_grid()
    assert empty_grid == []

    # Test large card (should create 3x3 grid)
    large_grid = sample_cards["large"].get_symbol_grid()
    assert len(large_grid) == 3
    assert len(large_grid[0]) == 3
    assert all(len(row) == 3 for row in large_grid)


@pytest.mark.parametrize(
    "card_symbols,other_symbols,expected",
    [
        ({0, 1, 2}, {1, 3, 4}, (1, "😂")),  # One matching symbol
        ({0, 1, 2}, {3, 4, 5}, None),  # No matching symbols
        ({0, 1, 2}, set(), None),  # Empty other card
        ({0, 1, 2}, {0, 1, 2}, (0, "😀")),  # Self-matching
    ],
)
def test_get_matching_symbol(emoji_map, card_symbols, other_symbols, expected):
    """Test matching symbol detection between cards"""
    card1 = DobbleCard(card_symbols)
    card2 = DobbleCard(other_symbols)
    assert card1.get_matching_symbol(card2) == expected


def test_emoji_wrapping(emoji_map):
    """Test emoji mapping wraparound for large numbers"""
    map_size = len(emoji_map)
    test_cases = [
        (map_size + 1, emoji_map[1]),  # Should wrap to index 1
        (map_size * 2 + 3, emoji_map[3]),  # Should wrap to index 3
        (map_size - 1, emoji_map[map_size - 1]),  # Last emoji
    ]

    for number, expected_emoji in test_cases:
        card = DobbleCard({number})
        assert expected_emoji in str(card)


@pytest.mark.parametrize(
    "symbols,expected_size",
    [
        ({0}, 1),  # 1 symbol -> 1x1 grid
        ({0, 1}, 2),  # 2 symbols -> 2x2 grid
        ({0, 1, 2, 3}, 2),  # 4 symbols -> 2x2 grid
        ({0, 1, 2, 3, 4}, 3),  # 5 symbols -> 3x3 grid
        ({0, 1, 2, 3, 4, 5, 6, 7, 8}, 3),  # 9 symbols -> 3x3 grid
    ],
)
def test_grid_scaling(symbols, expected_size):
    """Test grid size scaling based on number of symbols"""
    card = DobbleCard(symbols)
    grid = card.get_symbol_grid()
    assert len(grid) == expected_size
    assert all(len(row) == expected_size for row in grid)


def test_grid_content_integrity(sample_cards, emoji_map):
    """Test that grid content matches the original symbols"""
    card = sample_cards["standard"]
    grid = card.get_symbol_grid()

    # Collect all symbols from grid
    grid_symbols = set()
    for row in grid:
        for symbol, emoji in row:
            if symbol is not None:
                grid_symbols.add(symbol)
                # Verify emoji mapping
                assert emoji == emoji_map[symbol % len(emoji_map)]

    # Verify all original symbols are in grid
    assert grid_symbols == card.symbols
