import pytest
from unittest.mock import Mock, patch
from rich.prompt import Prompt, IntPrompt

from dobble.config import DIFFICULTY_LEVELS
from dobble.ui.game_ui import GameUI
from dobble.main import GameController


@pytest.fixture
def mock_console():
    with patch("dobble.ui.components.console") as mock:
        yield mock


@pytest.fixture
def mock_display_title():
    with patch("dobble.ui.display.display_title") as mock:
        yield mock


@pytest.fixture
def mock_display_game_state():
    with patch("dobble.ui.display.display_game_state") as mock:
        yield mock


@pytest.fixture
def mock_get_arrow_key_selection():
    with patch("dobble.ui.input.get_arrow_key_selection") as mock:
        yield mock


@pytest.fixture
def mock_game():
    mock = Mock()
    mock.players = []  # Ensure players attribute exists
    mock.find_matching_players.return_value = []
    mock.is_over = False
    return mock


@pytest.fixture
def game_ui():
    with patch("dobble.ui.game_ui.get_arrow_key_selection") as mock_selection:
        ui = GameUI()
        ui._get_arrow_key_selection = mock_selection  # Add mock as instance attribute
        yield ui


@pytest.fixture
def game_controller(mock_game):
    with patch("dobble.game.game.DobbleGame", return_value=mock_game):
        controller = GameController()
        controller.game = mock_game  # Pre-set the game instance
        yield controller


class TestGameUI:
    def test_select_difficulty_predefined(
        self, game_ui, mock_console, mock_display_title
    ):
        game_ui._get_arrow_key_selection.return_value = 0  # First difficulty level

        result = game_ui.select_difficulty()

        assert result == list(DIFFICULTY_LEVELS.values())[0]
        game_ui._get_arrow_key_selection.assert_called_once()

    def test_get_player_names(self, game_ui):
        with patch.object(Prompt, "ask", return_value=" Player1 , Player2 "):
            result = game_ui.get_player_names()
            assert result == ["Player1", "Player2"]

    def test_select_winner_single_player(self, game_ui):
        players = [Mock(name="Player1"), Mock(name="Player2")]
        result = game_ui.select_winner([1], players)
        assert result == 1

