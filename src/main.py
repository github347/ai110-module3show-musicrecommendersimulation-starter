"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


# ── Standard profiles ────────────────────────────────────────────────────────

ORIGINAL_PROFILE = {
    "name": "Original Profile",
    "genre": "pop",
    "mood": "happy", 
    "energy": 0.8,
    "likes_acoustic": False,
    }

HIGH_ENERGY_POP = {
    "name": "High-Energy Pop",
    "genre": "pop",
    "mood": "happy",
    "energy": 0.9,
    "likes_acoustic": False,
}

CHILL_LOFI = {
    "name": "Chill Lofi",
    "genre": "lofi",
    "mood": "chill",
    "energy": 0.35,
    "likes_acoustic": True,
}

DEEP_INTENSE_ROCK = {
    "name": "Deep Intense Rock",
    "genre": "rock",
    "mood": "intense",
    "energy": 0.95,
    "likes_acoustic": False,
}

# ── Adversarial / edge-case profiles ─────────────────────────────────────────

# Contradiction: high energy but sad mood — opposite ends of the emotional spectrum.
# Expected stress: the scorer rewards energy closeness AND mood match separately,
# so songs that are high-energy but NOT sad will rank well despite the sad preference.
CONFLICTING_ENERGY_SAD = {
    "name": "Adversarial — High Energy + Sad Mood",
    "genre": "blues",
    "mood": "sad",
    "energy": 0.9,
    "likes_acoustic": False,
}

# Ghost genre: no song in the dataset has genre "k-pop".
# Expected stress: genre_score will always be 0; ranking collapses to mood + energy only.
GHOST_GENRE = {
    "name": "Adversarial — Nonexistent Genre (k-pop)",
    "genre": "k-pop",
    "mood": "happy",
    "energy": 0.8,
    "likes_acoustic": False,
}

# Extremes: perfectly still (energy 0.0) AND loves acoustic.
# Expected stress: acoustic songs score well on two axes simultaneously;
# check whether a very-low-energy, acoustic-heavy result dominates unfairly.
EXTREME_ACOUSTIC = {
    "name": "Adversarial — Zero Energy + Max Acoustic",
    "genre": "folk",
    "mood": "melancholic",
    "energy": 0.0,
    "likes_acoustic": True,
}

ALL_PROFILES = [
    HIGH_ENERGY_POP,
    CHILL_LOFI,
    DEEP_INTENSE_ROCK,
    CONFLICTING_ENERGY_SAD,
    GHOST_GENRE,
    EXTREME_ACOUSTIC,
]


def run_profile(user_prefs: dict, songs: list) -> None:
    label = user_prefs.get("name", "Unnamed Profile")
    # score_song / recommend_songs don't use the "name" key, so pass a clean copy
    prefs = {k: v for k, v in user_prefs.items() if k != "name"}

    print(f"\n{'=' * 60}")
    print(f"Profile: {label}")
    print(f"  genre={prefs['genre']}  mood={prefs['mood']}"
          f"  energy={prefs['energy']}  likes_acoustic={prefs.get('likes_acoustic', False)}")
    print(f"{'=' * 60}")

    recommendations = recommend_songs(prefs, songs, k=5)
    for rank, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        print(f"  {rank}. {song['title']} ({song['artist']}) — Score: {score:.2f}")
        print(f"     Because: {explanation}")


def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile in ALL_PROFILES:
        run_profile(profile, songs)

    print()


if __name__ == "__main__":
    main()
