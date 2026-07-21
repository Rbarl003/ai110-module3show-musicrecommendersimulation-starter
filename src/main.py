"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    # When run as a module: python -m src.main
    from src.recommender import load_songs, recommend_songs
except ModuleNotFoundError:
    # When run directly from inside src/: python main.py
    from recommender import load_songs, recommend_songs


# Distinct taste profiles to test the recommender against.
# Each is a user_prefs dict: favorite_genre, favorite_mood, target_energy,
# likes_acoustic.
PROFILES = {
    "Chill Lofi Studier": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.40,
        "likes_acoustic": True,
    },
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.85,
        "likes_acoustic": False,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "likes_acoustic": False,
    },
}


def print_recommendations(name: str, user_prefs: dict, songs: list) -> None:
    """Print the top-k ranked recommendations for one taste profile."""
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print()
    print("=" * 44)
    print(f"  TOP RECOMMENDATIONS — {name}")
    print(f"  {user_prefs['favorite_genre']} / {user_prefs['favorite_mood']}, "
          f"energy {user_prefs['target_energy']:.2f}, "
          f"acoustic={user_prefs['likes_acoustic']}")
    print("=" * 44)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']} — {song['artist']}")
        print(f"   Score: {score:.2f}")
        print("   Reasons:")
        # `explanation` joins each reason with "; " — split it back out so
        # every reason gets its own bulleted line.
        for reason in explanation.split("; "):
            print(f"     • {reason}")

    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Run the recommender against every taste profile.
    for name, user_prefs in PROFILES.items():
        print_recommendations(name, user_prefs, songs)


if __name__ == "__main__":
    main()
