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
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """
    Scores a single song against user preferences using the weighted recipe:
      score = 0.35 * mood_score + 0.25 * genre_score + 0.25 * energy_score + 0.15 * acoustic_score

    Returns a (score, explanation) tuple where explanation lists which attributes matched.
    """
    mood_score = 1.0 if song["mood"] == user_prefs["mood"] else 0.0
    genre_score = 1.0 if song["genre"] == user_prefs["genre"] else 0.0
    energy_score = 1.0 - abs(song["energy"] - user_prefs["energy"])
    likes_acoustic = user_prefs.get("likes_acoustic", False)
    acoustic_score = song["acousticness"] if likes_acoustic else 1.0 - song["acousticness"]

    score = (0.35 * mood_score
           + 0.25 * genre_score
           + 0.25 * energy_score
           + 0.15 * acoustic_score)

    reasons = []
    if mood_score == 1.0:
        reasons.append(f"mood matches ({song['mood']})")
    if genre_score == 1.0:
        reasons.append(f"genre matches ({song['genre']})")

    reasons.append(f"energy closeness {energy_score:.2f}")
    reasons.append(f"acoustic fit {acoustic_score:.2f}")
    explanation = "; ".join(reasons)

    return score, explanation

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
