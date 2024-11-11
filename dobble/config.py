from typing import Dict

VALID_CARD_SIZES = [2, 3, 4, 6, 8, 12, 14, 18, 20, 24, 30, 32, 38, 42, 44, 48, 54, 60]
DIFFICULTY_LEVELS: Dict[str, int] = {
    "Trivial": 3,
    "Easy": 4,
    "Normal": 8,
    "Hard": 12,
    "Extreme": 18,
}
