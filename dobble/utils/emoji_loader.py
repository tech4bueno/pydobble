from pathlib import Path
import random
import sys
from typing import Dict, List


def parse_code_points(line: str) -> List[int]:
    if ".." in line:
        start, end = line.split("..")
        return list(range(int(start, 16), int(end, 16) + 1))
    return [int(line, 16)]


def generate_emoji_map() -> Dict[int, str]:
    emojis = []
    emoji_file = Path(__file__).parent.parent / "data" / "emojis.txt"

    with open(emoji_file, "r") as f:
        for line in f:
            line = line.strip()
            for code_point in parse_code_points(line):
                try:
                    emoji = chr(code_point)
                    if sys.stdout.encoding.upper() in ["UTF-8", "UTF8"]:
                        emoji.encode("utf-8")
                        emojis.append(emoji)
                except (UnicodeEncodeError, UnicodeError):
                    continue

    random.shuffle(emojis)
    return {i: emoji for i, emoji in enumerate(emojis)}


EMOJI_MAP = generate_emoji_map()
