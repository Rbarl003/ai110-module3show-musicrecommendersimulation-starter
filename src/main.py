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


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Taste profile: "The Focused Studier" — calm, acoustic study music
    user_prefs = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.40,
        "likes_acoustic": True,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print()
    print("=" * 44)
    print("  TOP RECOMMENDATIONS")
    print(f"  for a {user_prefs['favorite_genre']} / "
          f"{user_prefs['favorite_mood']} listener")
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


if __name__ == "__main__":
    main()
