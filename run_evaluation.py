"""
System Evaluation runner for the Music Recommender Simulation.

Runs a set of "normal" user preference profiles and a set of adversarial /
edge-case profiles through the actual recommend_songs() implementation in
src/recommender.py, and prints the real output (or the real crash) for each.

Usage:
    python run_evaluation.py
"""

from src.recommender import load_songs, recommend_songs

NORMAL_PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.85},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9},
}

ADVERSARIAL_PROFILES = {
    "conflicting_signals": {"genre": "metal", "mood": "chill", "energy": 0.1},
    "no_match_genre": {"genre": "opera", "mood": "happy", "energy": 0.5},
    "missing_fields": {"mood": "sad"},
    "boundary_energy": {"genre": "pop", "mood": "happy", "energy": 1.5},
    "empty_prefs": {},
    "type_mismatch_energy": {"genre": "lofi", "mood": "chill", "energy": "high"},
    "exact_tie": {"genre": "classical", "mood": "romantic", "energy": 0.355},
}


def print_results(label, user_prefs, songs, k=5):
    print(f"\n{label}")
    print(f"  profile: {user_prefs}")
    print("-" * 60)
    try:
        recommendations = recommend_songs(user_prefs, songs, k=k)
        if not recommendations:
            print("  (no recommendations returned)")
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            reasons = explanation if explanation else "no scoring factors matched"
            print(f"  {rank}. {song['title']} by {song['artist']} - Score: {score:.2f}")
            print(f"       - {reasons}")
    except Exception as exc:
        print(f"  CRASHED: {type(exc).__name__}: {exc}")
    print("=" * 60)


def main():
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    print("\n" + "#" * 60)
    print("# NORMAL PROFILES")
    print("#" * 60)
    for label, prefs in NORMAL_PROFILES.items():
        print_results(label, prefs, songs)

    print("\n" + "#" * 60)
    print("# ADVERSARIAL / EDGE-CASE PROFILES")
    print("#" * 60)
    for label, prefs in ADVERSARIAL_PROFILES.items():
        print_results(label, prefs, songs)


if __name__ == "__main__":
    main()
