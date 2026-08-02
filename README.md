# Three-Strikes You'reee Out

Identify a mystery 2025 MLB player from their season stats and up to three
AI-generated clues. Clues come from a Gemini model pulling facts from outside
the dataset, and a validator model screens each one so it never leaks the
player's name.

## An extension of the Section 1 guessing game

This project builds on the simple number-guessing game from **Section 1**. That
version had you guess a hidden number with higher/lower feedback. Here the same
core loop — a hidden answer, repeated guesses, a limited number of attempts, and
a score — is extended into a full MLB player guesser: the secret is a real
player instead of a number, guesses are names picked from an autocomplete, and
the feedback comes from a stat card plus AI-generated, name-safe clues.

## Architecture Overview
The main class is the Game class, the class handles and saves the current state of the game and corresponds the user action to an appropriate action in the back end. 

The Game class uses the Player class to understand player data; the player class encapitulates the pertinent information about a player with methods to load players from data and retrieve players. 

The Game class can call the Clue class to generate clues about a player to be guessed. The Clue class has two AI models, a GeminiModel that retireves the appropriate clue for a player and a validatorModel that ensure the clue does not contain identitfying information about a player. The ValidatorModel Functions in a feedback loop with the GeminiModel and will reprompt if identitfying information is found. 



## Set Up Instruction

```bash
streamlit run app.py
```

Requires a `.env` file with `API_KEY` (Gemini) and optionally `GEMINI_MODEL`.

## Sample Output
- User is guessing the player Jahmani Jones, user asks for the player's nickname. GeminiModel retrieves the nickname 'Jam' and the validator model confirms that the nickname is not identitfying the player directly. 

- User is guessing the player Heliot Ramos and asks for his best moment. The Gemini Model finds that Heliot Ramos hit the first 'Spalsh Hit' into the McCovey Cove by a right handed hitter, the validator model asks the Gemini Model to remove reference to the player name so Gemnini Model replaces player name with 'This Outfielder'

## Layout

- `app.py` — Streamlit UI (view only).
- `game_models.py` — game logic: player selection, clue generation, validation,
  scoring.
- `Data/MLB_2025` — 2025 player dataset, used to pick the secret and show stats.
- `Design.md` — full design, class structure, and game/clue flow diagrams.

## Design Decisions

Key decisions made while building this, and what each one trades away.

### Easy find evaulaution

The clues for a player is only retrieve when the user's asks for it, and not loaded with the player card

- **Why:** To save API call cost and ensure initial load spped is quick.    
- **Tradeoff:** When the user eventually clicks on get clue, the process is slow since it's not preloaded. 

### Two-model pipeline: generator + validator

A `GeminiModel` produces the clue and a separate `ValidatorModel` screens it for
name leaks, re-prompting Gemini with an explicit correction when the name slips
through (see the corrective loop in `Design.md`).

- **Why:** The single hardest failure mode is a clue that names the player and
  spoils the round. Separating "write the clue" from "did it leak the name?"
  keeps each responsibility small and makes the leak check independently
  testable.
- **Tradeoff:** Up to `max_retries` extra Gemini calls per clue on a leak, adding
  latency and cost. It also can't catch *semantic* leaks (e.g. "the Angels' most
  famous two-way star") — only literal name matches.


### Discrete Clues

There is only three clues available 'Players Best Moment', 'Player's Nickname', and 'Player's College/Highschool'

- **Why:** This helps remove the possibility of prompt injection makes it easier to test and refine our AI prompt with a small set of inputs
- **Tradeoff:** It would make the game a lot more dynamic if users have more freedom to input free-text clues

### Testing Summary:
- **What worked:** I thought that generally the retriever validator loop worked well in preventing information leak
- **What didn't work:** I worked on it for a while but I was never able to get the latin names to show - up correctly. There may be something wrong with the encoding standard I was using
- **What I Learned** I learned that using validator and retriever loop can help ensure that the output is correct and prevent unintended behavior

### Reflection
This project taught that AI works best in a well-defined environement and when its work and output can be checked.

#### Sample output
#### Wrong Guess then Getting Clue 
```
2026-08-02 12:24:57,521 [INFO] game_models: Loaded 408 players from C:\Users\yang1\Documents\AI101\DJ-You-Recommender\Data\MLB_2025
2026-08-02 12:24:57,521 [INFO] game_models: Starting new round (team=any, awards=False)
2026-08-02 12:24:57,521 [INFO] game_models: Secret player chosen from 408 candidates (team=any, awards=False)
2026-08-02 12:25:06,669 [INFO] game_models: Wrong guess on attempt 1; 2 left
2026-08-02 12:25:56,583 [INFO] game_models: Generating clue 1 for Edmundo Sosa
2026-08-02 12:25:57,582 [INFO] game_models: Gemini request (model=gemini-3.6-flash, 213 chars)
2026-08-02 12:26:00,829 [INFO] game_models: Gemini response (126 chars)
2026-08-02 12:26:00,829 [INFO] game_models: Validator: clue is clean
2026-08-02 12:26:00,829 [INFO] game_models: Validator: clue is clean
2026-08-02 12:26:00,829 [INFO] game_models: Clue 1 ready (0 retries)
```
#### Validator Finding bad nickname

2026-08-02 12:26:39,328 [INFO] game_models: Secret player chosen from 45 candidates (team=any, awards=True)
2026-08-02 12:26:42,310 [INFO] game_models: Generating clue 0 for James Wood
2026-08-02 12:26:42,588 [INFO] game_models: Gemini request (model=gemini-3.6-flash, 212 chars)
2026-08-02 12:26:53,466 [INFO] game_models: Gemini response (51 chars)
2026-08-02 12:26:53,466 [INFO] game_models: Validator: leak detected (name token 'wood' present)
2026-08-02 12:26:53,466 [WARNING] game_models: Clue 0 leaked the name; re-prompting (retry 1/3)
2026-08-02 12:26:53,466 [INFO] game_models: Validator: building corrective re-prompt
2026-08-02 12:26:53,466 [INFO] game_models: Gemini request (model=gemini-3.6-flash, 294 chars)
2026-08-02 12:27:05,534 [INFO] game_models: Gemini response (157 chars)
2026-08-02 12:27:05,534 [INFO] game_models: Validator: clue is clean
2026-08-02 12:27:05,534 [INFO] game_models: Validator: clue is clean
2026-08-02 12:27:05,534 [INFO] game_models: Clue 0 ready (1 retries)

