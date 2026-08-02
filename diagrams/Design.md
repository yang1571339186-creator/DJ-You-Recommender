# MLB Player Guessing Game — Design

A guessing game where the player identifies a mystery 2025 MLB player from
AI-generated clues. The dataset (`Data/MLB_2025`) is used **only to pick** the
secret player — every clue comes from a Gemini model pulling facts from outside
our dataset. A validator model guards each clue so it never leaks the player's
name.

## Clues

Exactly **3 fixed clues** are revealed in order, one per wrong guess:

1. **Nickname** — "Does the player have a nickname?"
2. **School** — "What college or high school did the player attend?"
3. **Best moment** — "What is the player's best career moment?"

Three wrong guesses (all clues exhausted) ends the round as a loss.

## Class Structure

```mermaid
classDiagram
    class Game {
        -player_data: dict
        -secret_player: Player
        -clue: Clue
        -clue_index: int
        -attempts: int
        -score: int
        -status: str
        +start_new_round()
        +retrieve_player() Player
        +next_clue() str
        +check_guess(name) bool
        +end_round()
    }

    class Player {
        +name: str
        +team: str
        +position: str
    }

    class Clue {
        -player: Player
        -gemini: GeminiModel
        -validator: ValidatorModel
        +CLUE_QUESTIONS: list
        +get_validated_clue(index) str
    }

    class GeminiModel {
        +model_name: str
        +ask(prompt) str
    }

    class ValidatorModel {
        +max_retries: int
        +contains_name(clue_text, player_name) bool
        +build_correction_prompt(question, player_name, bad_answer) str
    }

    Game "1" --> "1" Player : picks from data
    Game "1" --> "1" Clue : has
    Clue "1" --> "1" Player : describes
    Clue "1" --> "1" GeminiModel : uses
    Clue "1" --> "1" ValidatorModel : uses
    ValidatorModel ..> GeminiModel : drives re-prompt
```

## Game Loop

The data only selects the player; all three clues are AI-generated.

```mermaid
flowchart TD
    Start([Start Round]) --> Retrieve[Game.retrieve_player<br/>random Player from data]
    Retrieve --> Clue1[Clue 1: Nickname]

    Clue1 --> G1{Guess?}
    G1 -->|Correct| Win
    G1 -->|Wrong| Clue2[Clue 2: School]

    Clue2 --> G2{Guess?}
    G2 -->|Correct| Win
    G2 -->|Wrong| Clue3[Clue 3: Best moment]

    Clue3 --> G3{Guess?}
    G3 -->|Correct| Win
    G3 -->|Wrong| Lose[Lose - reveal player]

    Win[Win - score by clues used] --> End([End Round])
    Lose --> End
```

## Clue Pipeline

Each clue is a fixed question sent to Gemini, then screened by the validator.

```mermaid
flowchart TD
    Data[(Data/MLB_2025)] -.pick only.-> Pick[Game.retrieve_player]
    Pick --> Secret[secret Player name]

    Request([Game needs clue N]) --> Select{clue_index}
    Select -->|0| Q1["Q: Does the player<br/>have a nickname?"]
    Select -->|1| Q2["Q: What college / high school<br/>did the player attend?"]
    Select -->|2| Q3["Q: What is the player's<br/>best career moment?"]

    Q1 --> Gemini
    Q2 --> Gemini
    Q3 --> Gemini
    Secret --> Gemini[GeminiModel.ask<br/>player_name + question]

    Gemini --> Raw[Raw clue text]
    Raw --> Validator{ValidatorModel.contains_name<br/>Is the player's name<br/>in the answer?}

    Validator -->|Clean| Return[Return safe clue]
    Validator -->|Leaked| Regen[Corrective re-prompt]
    Regen --> Gemini
    Return --> Display([Display clue N])
```

## Validator Corrective Loop

On a leak, the validator re-prompts Gemini with an **explicit** instruction
naming what leaked and forbidding it. A retry counter caps the loop, with
name-redaction as the final fallback so a round always resolves.

```mermaid
flowchart TD
    Start([get_validated_clue]) --> Ask[Gemini.ask player + question]
    Ask --> Check{Validator: name present?}

    Check -->|No| Ok[Return clue]
    Check -->|Yes| Count{Retries left?}

    Count -->|Yes| Correct[Re-prompt Gemini, explicit:<br/>'Your previous answer mentioned<br/>the name. Do NOT include<br/>PLAYER_NAME or any part of it.<br/>Answer the question again.']
    Correct --> Ask

    Count -->|No, exhausted| Fallback[Redact name to blank<br/>as last resort]
    Fallback --> Ok
```
