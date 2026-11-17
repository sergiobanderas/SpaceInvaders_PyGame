import os

from config import *

# scores.txt lives next to this file, no matter where the game is launched from
SCORES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), SCORES_FILE)


def load_scores():
    """Read every saved score from the file and return them as (name, score) sorted from highest to lowest"""
    scores = []
    if not os.path.exists(SCORES_PATH):
        return scores  # No games saved yet

    with open(SCORES_PATH, encoding="utf-8") as file:
        for line in file:
            # Each line has the format: name;score
            parts = line.strip().rsplit(";", 1)
            if len(parts) == 2 and parts[1].isdigit():
                scores.append((parts[0], int(parts[1])))

    scores.sort(key=lambda entry: entry[1], reverse=True)
    return scores


def top_scores(count=TOP_SCORES_COUNT):
    """Return the best scores, highest first"""
    return load_scores()[:count]


def save_score(name, score):
    """Append a new score to the file"""
    with open(SCORES_PATH, "a", encoding="utf-8") as file:
        file.write(f"{name};{score}\n")
