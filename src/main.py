"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    print(f"loaded {len(songs)} songs." )



    # Starter example profile
    user_prefs = list()
    user_prefs.append({"genre": "pop", "mood": "sad", "energy": 0.8, "valence": 0.8})

    user_prefs.append({"genre": "rock", "mood": "sad", "energy": 0.9, "valence": 0.2})

    
    user_prefs.append({"genre": "classical", "mood": "happy", "energy": 0.5, "valence": 0.2})
    for user in user_prefs:
        recommendations = recommend_songs(user, songs, k=5)
        print("\nTop recommendations:\n")
        for rec in recommendations:
            # You decide the structure of each returned item.
            # A common pattern is: (song, score, explanation)
            song, score, explanation = rec
            print(f"{song['title']} - Score: {score:.2f}")
            print(f"Because: {explanation}")
            print()


if __name__ == "__main__":
    main()
