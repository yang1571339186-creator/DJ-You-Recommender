import csv
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
    target_valence: float
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
    numeric_fields = {
        "energy",
        "tempo_bpm",
        "valence",
        "danceability",
        "acousticness",
    }

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song: Dict = {}
            for key, value in row.items():
                if key == "id":
                    song[key] = int(value)
                elif key in numeric_fields:
                    song[key] = float(value)
                else:
                    song[key] = value
            songs.append(song)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    # Weighted-sum model from the README recipe. Each sub-score is 0..1 and is
    # multiplied by its weight; the weights sum to 1.0 so the final score is 0..1.
    reasons: List[str] = []
    score = 0.0

    # genre_match (weight 0.30): 1.0 if the song's genre equals the favorite.
    fav_genre = user_prefs.get("favorite_genre", user_prefs.get("genre"))
    if fav_genre is not None and song["genre"] == fav_genre:
        score += 0.30
        reasons.append(f"matches your favorite genre ({song['genre']})")

    # mood_match (weight 0.20): 1.0 if the moods match.
    fav_mood = user_prefs.get("favorite_mood", user_prefs.get("mood"))
    if fav_mood is not None and song["mood"] == fav_mood:
        score += 0.20
        reasons.append(f"matches your {song['mood']} mood")

    # energy closeness (weight 0.25): 1 - |song.energy - target_energy|.
    target_energy = user_prefs.get("target_energy", user_prefs.get("energy"))
    if target_energy is not None:
        energy_closeness = 1.0 - abs(song["energy"] - target_energy)
        score += 0.25 * energy_closeness
        if energy_closeness >= 0.8:
            reasons.append("energy level is close to what you want")

    # valence closeness (weight 0.15): 1 - |song.valence - target_valence|.
    target_valence = user_prefs.get("target_valence", user_prefs.get("valence"))
    if target_valence is not None:
        valence_closeness = 1.0 - abs(song["valence"] - target_valence)
        score += 0.15 * valence_closeness
        if valence_closeness >= 0.8:
            reasons.append("positivity matches your taste")

    # acoustic_match (weight 0.10): rewards high acousticness when the user
    # likes acoustic music.
    if user_prefs.get("likes_acoustic"):
        score += 0.10 * song["acousticness"]
        if song["acousticness"] >= 0.5:
            reasons.append("acoustic sound you enjoy")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # Scoring: rate every song independently.
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        if reasons:
            explanation = "; ".join(reasons)
        else:
            explanation = "no strong matches, but it's in the catalog"
        scored.append((song, score, explanation))

    # Ranking: sort by score (descending), breaking ties by energy closeness
    # to the user's target so the closer-energy song wins an equal score.
    target_energy = user_prefs.get("target_energy", user_prefs.get("energy"))

    def energy_closeness(item: Tuple[Dict, float, str]) -> float:
        song = item[0]
        if target_energy is None:
            return 0.0
        return 1.0 - abs(song["energy"] - target_energy)

    scored.sort(key=lambda item: (item[1], energy_closeness(item)), reverse=True)

    return scored[:k]
