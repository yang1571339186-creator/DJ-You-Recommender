def get_range_for_difficulty(difficulty: str):
    difficulty = difficulty.strip().lower()
    if difficulty == "easy":
        return 1, 20
    if difficulty == "normal":
        return 1, 100
    if difficulty == "hard":
        return 1, 50
    return 1, 100
def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None

def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if (type(guess) != int):
        guess = int(guess)
    if (type(secret) != int):
        secret = int(secret)
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess < secret:
            return "Too Low", "📈 Go HIGHER!"
        else:
            return "Too High", "📉 Go LOWER!"
    except TypeError:
        g = int(guess)
        secret = int(secret)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g < secret:
            return "Too Low", "📈 Go HIGHER!"
        return "Too High", "📉 Go LOWER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number )
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score