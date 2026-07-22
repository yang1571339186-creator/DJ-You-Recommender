# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
DJ You

---

## 2. Intended Use  

DJ You is a small, content-based music recommender built for classroom exploration, not real-world deployment. Given a short description of a user's taste, it ranks a fixed catalog of 20 songs and returns the top 5, each paired with a plain-English reason for why it was chosen.

It assumes the user can describe their taste as a simple profile: a favorite genre, a favorite mood, a target energy level (how intense they want the music), a target valence (how positive/upbeat), and whether they like acoustic music. It further assumes those preferences are stable and that a good recommendation is one whose features are numerically close to the profile. It is meant to teach how data becomes a ranked prediction — it is not tuned for real listeners or a real music library.

---

## 3. How the Model Works  

Imagine each song has a little report card: what genre it is, what mood it gives off, how energetic it is, how upbeat (positive) it feels, and how acoustic it sounds. The user fills out a matching wish list: their favorite genre, favorite mood, how much energy they want, how upbeat they want it, and whether they like acoustic music.

To score a song, the model checks the wish list one item at a time and awards points for each match:

- Same genre? Add the most points (this matters most).
- Same mood? Add a solid chunk.
- Is the song's energy close to what the user asked for? The closer it is, the more points — a perfect match gives full credit, and being far off gives almost none.
- Is the song's positivity close to the target? Same idea, fewer points at stake.
- If the user likes acoustic music, quieter/acoustic songs get a small bonus.

All those points add up to a single score between 0 and 1, so every song can be compared fairly. The model then lines up all the songs from highest to lowest score and hands back the top few, along with a short note listing which items "fired" (for example, "matches your favorite genre; energy level is close to what you want").

**Changes from the starter logic:** the starter just returned the first few songs unchanged and a placeholder explanation. I replaced that with the real weighted-scoring recipe, made the profile fields flexible (it accepts either `favorite_genre`/`target_energy` names or short `genre`/`energy` names), added the human-readable reasons, and made ranking break ties by whichever song's energy is closest to the user's target so equal scores still order sensibly.

---

## 4. Data  

The dataset is a single CSV file, `data/songs.csv`, containing **20 songs**. Each row has an id, title, artist, genre, mood, and five numeric features: energy, tempo (BPM), valence, danceability, and acousticness. I used the starter catalog as-is — no songs were added or removed.

**Genres represented (11):** pop (4 songs), lofi (4), ambient (3), synthwave (2), and then rock, metal, soul, jazz, indie pop, folk, and classical with just one song each.

**Moods represented (8):** chill (5), happy (4), intense (4), relaxed (3), focused (2), moody (2) — with the remaining moods rare or absent for some genres.

**What's missing:** the dataset is heavily skewed toward pop, lofi, and ambient, so most other genres have only a single example. There's no information about lyrics, language, era/release year, artist popularity, or cultural context. Whole dimensions of taste — like "I want something in Spanish," "something from the 90s," or "something by artists like this one" — simply can't be expressed, because the data doesn't contain them.

---

## 5. Strengths  

- **Well-represented tastes:** A user who likes upbeat, high-energy pop (for example genre `pop`, mood `happy`, energy ~0.8, valence ~0.8) gets a clean, confident top 5 — "Sunrise City" and "Skyline Anthem" rise to the top with strong scores because pop is the best-represented genre in the catalog.
- **Energy and positivity matching:** The distance-based sub-scores work as intended — songs whose energy and valence are numerically close to the target consistently rank above ones that are far off, even when genre doesn't match, which keeps the list from being genre-only.
- **Explanations match the scores:** The "Because:" reasons line up with why a song ranked where it did, so the output is easy to sanity-check. When I read a recommendation, the stated reasons matched my own intuition about why that song fit the profile.
- **Graceful degradation:** Because the model uses a weighted sum rather than requiring every feature to match, a single mismatch lowers a song's score instead of eliminating it — so the system still returns a reasonable ranked list even for imperfect matches.

---

## 6. Limitations and Bias 

- **Features it ignores:** The score uses only genre, mood, energy, valence, and acousticness. It deliberately leaves out `tempo_bpm` (it's on a 60–152 scale and would swamp the 0–1 features unless rescaled) and `danceability`. It has no notion of lyrics, language, artist similarity, era, or novelty/diversity.
- **Underrepresented genres and moods:** Genres like classical, jazz, folk, soul, rock, and metal appear only once each, so users who love them get low, unreliable scores. A classical/happy user is served especially poorly because the one classical song is tagged `chill`, not `happy`, so even the "right" genre misses on mood.
- **Overfitting to one preference:** Genre carries the largest single weight (0.30). When it's over-weighted (I tested 0.60), the top results collapse onto one genre and produce a repetitive, filter-bubble-style list that ignores otherwise-great songs from other genres.
- **Unintended favoritism:** Because the catalog is skewed toward pop, lofi, and ambient, users whose taste happens to align with those genres get richer, more confident recommendations, while everyone else gets weaker matches. The unfairness isn't in the math — it's baked into the data distribution the math sits on top of.
- **Cold spots:** For taste combinations that barely exist in the catalog (e.g. sad, high-energy rock), the system still returns 5 songs, but they're low-scoring near-misses. It never says "I don't have a good answer" — it always fills the list, which can overstate its confidence.

---

## 7. Evaluation  

I checked the recommender both by running it on several user profiles and with the starter tests in `tests/test_recommender.py` (run via `pytest`).

**Profiles I tested** (from `src/main.py`):

- `pop / sad / energy 0.8 / valence 0.8` — a well-represented profile; produced a strong, sensible top 5 led by pop songs.
- `rock / sad / energy 0.9 / valence 0.2` — a cold spot; the catalog has almost no sad rock, so scores were low and the list was made of near-misses.
- `classical / happy / energy 0.5 / valence 0.2` — mostly low scores, because the single classical song is tagged `chill` and doesn't match the happy mood.

**What I looked for:** that higher scores actually corresponded to better feature matches; that the "Because:" reasons matched why each song ranked where it did; that ties were broken sensibly (by energy closeness); and that the total score always stayed within 0–1.

**What surprised me:** how quickly the system runs out of good answers for underrepresented tastes while still confidently returning a full list of 5 — the ranking always looks authoritative even when the underlying scores are weak. It made clear that the quality of the recommendations depends far more on the data distribution than on the scoring math.

---

## 8. Future Work  

- **More Features** I would've liked to have features about the songs to work with.Such as the year the songs were published as well as in what locations (i.e city) the songs are populat in. 
- **Use the ignored features:** Curve `tempo_bpm` to to a 0-1 scale where 0.5 is the average. This way we can quantitfy how the bpm should affect the result. We would need a diverse number of songs to make this work. 
- **Handling complex tastes:** Using sueprvised learning from the users. The users can 'like' or  'disklike' songs in the recommendation and the weighs can change dynamically based on that. 
- **Better explanations:** Show how close each numeric feature was (e.g. "energy 0.82 vs your 0.80") rather than a fixed phrase, so the reasons are more specific and trustworthy.

---

## 9. Personal Reflection  

Building this model made the song recommendation feel a lot more formulaic. Ultimately, the system that big companies use is a version of this model but with more features and data so it helped me understand these systems. 

The most interesting discovery was how much power lives in two invisible places: the weights I picked and the data I fed in. Deciding that genre is worth 0.30 and acousticness only 0.10 quietly decides whose taste gets served well, and a catalog skewed toward pop and lofi means those listeners get better results before any code even runs. That changed how I think about the recommendation apps I use every day — behind every "just for you" list are similar weight and data choices I never see, shaping what I'm offered and what I never get shown.
