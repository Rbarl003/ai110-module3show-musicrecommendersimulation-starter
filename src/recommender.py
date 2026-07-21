from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file into a list of dictionaries.

    Numeric columns are converted from strings to numbers so they can be
    used in math later:
      - id, tempo_bpm        -> int
      - energy, valence,
        danceability,
        acousticness         -> float
    Text columns (title, artist, genre, mood) are left as strings.

    Required by src/main.py
    """
    import csv

    int_fields = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability", "acousticness"}

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song: Dict = {}
            for key, value in row.items():
                if key in int_fields:
                    song[key] = int(value)
                elif key in float_fields:
                    song[key] = float(value)
                else:
                    song[key] = value
            songs.append(song)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences using the Algorithm Recipe:

      - Genre match      -> +2.0
      - Mood match       -> +1.0
      - Energy similarity-> +1.0 max, graded by closeness
      - Acoustic bonus   -> +0.5 (only if the user likes acoustic AND the
                            song is acoustic enough)

    Returns (score, reasons), where reasons is a list of human-readable
    strings explaining which components fired.

    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons: List[str] = []

    # Genre match (+2.0): the reliable anchor, worth double a mood match.
    if song["genre"] == user_prefs["favorite_genre"]:
        score += 2.0
        reasons.append(f"genre match ({song['genre']}) +2.0")

    # Mood match (+1.0): refines the feel within a genre.
    if song["mood"] == user_prefs["favorite_mood"]:
        score += 1.0
        reasons.append(f"mood match ({song['mood']}) +1.0")

    # Energy similarity (up to +1.0): graded so a near-miss still earns credit.
    energy_diff = abs(user_prefs["target_energy"] - song["energy"])
    energy_points = 1.0 * (1 - energy_diff)
    score += energy_points
    reasons.append(f"energy close (Δ{energy_diff:.2f}) +{energy_points:.2f}")

    # Acoustic bonus (+0.5): tiebreaker, only when the user actually cares.
    if user_prefs["likes_acoustic"] and song["acousticness"] >= 0.6:
        score += 0.5
        reasons.append(f"acoustic ({song['acousticness']:.2f}) +0.5")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Scores every song, ranks them highest-first, and returns the top k.

    Each returned item is (song_dict, score, explanation).

    Required by src/main.py
    """
    # Score every song. A list comprehension is the Pythonic way to build
    # one list from another: for each song, unpack (score, reasons) and pair
    # it with the song and a joined explanation string.
    scored = [
        (song, score, "; ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]

    # Rank highest-first. sorted() returns a NEW sorted list (it does not
    # touch `scored`); key=itemgetter-style lambda pulls the score out of each
    # tuple; reverse=True puts the biggest score first.
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)

    # Slice the top k.
    return ranked[:k]
