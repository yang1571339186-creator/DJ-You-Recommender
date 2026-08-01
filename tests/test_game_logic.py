import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty


def test_get_range_for_difficulty():
    assert get_range_for_difficulty("easy") == (1, 20)
    assert get_range_for_difficulty("normal") == (1, 100)
    assert get_range_for_difficulty("hard") == (1, 50)
    assert get_range_for_difficulty("invalid") == (1, 100)
    assert get_range_for_difficulty("EASY") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("HARD") == (1, 50)
    assert get_range_for_difficulty("  easy  ") == (1, 20)
    assert get_range_for_difficulty("\tnormal\n") == (1, 100)


def test_parse_guess():
    ok, guess, error = parse_guess("42")
    assert ok is True
    assert guess == 42
    assert error is None

    ok, guess, error = parse_guess("0")
    assert ok is True
    assert guess == 0
    assert error is None

    ok, guess, error = parse_guess("-5")
    assert ok is True
    assert guess == -5
    assert error is None

    ok, guess, error = parse_guess("3.7")
    assert ok is True
    assert guess == 3
    assert error is None

    ok, guess, error = parse_guess("10.9")
    assert ok is True
    assert guess == 10
    assert error is None

    ok, guess, error = parse_guess("")
    assert ok is False
    assert guess is None
    assert error == "Enter a guess."

    ok, guess, error = parse_guess(None)
    assert ok is False
    assert guess is None
    assert error == "Enter a guess."

    ok, guess, error = parse_guess("abc")
    assert ok is False
    assert guess is None
    assert error == "That is not a number."

    ok, guess, error = parse_guess("12.34.56")
    assert ok is False
    assert guess is None
    assert error == "That is not a number."

    ok, guess, error = parse_guess("  50  ")
    assert ok is True
    assert guess == 50
    assert error is None


def test_check_guess():
    outcome, message = check_guess(42, 42)
    assert outcome == "Win"
    assert message == "🎉 Correct!"

    outcome, message = check_guess(10, 50)
    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!"

    outcome, message = check_guess(100, 50)
    assert outcome == "Too High"
    assert message == "📉 Go LOWER!"

    outcome, message = check_guess(0, 0)
    assert outcome == "Win"
    assert message == "🎉 Correct!"

    outcome, message = check_guess(-5, -5)
    assert outcome == "Win"
    assert message == "🎉 Correct!"

    outcome, message = check_guess(-10, 0)
    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!"

    outcome, message = check_guess(5, -10)
    assert outcome == "Too High"
    assert message == "📉 Go LOWER!"

    outcome, message = check_guess("42", "42")
    assert outcome == "Win"
    assert message == "🎉 Correct!"

    outcome, message = check_guess("10", "50")
    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!"

    outcome, message = check_guess("100", "50")
    assert outcome == "Too High"
    assert message == "📉 Go LOWER!"


def test_update_score():
    score = update_score(0, "Win", 0)
    assert score == 100

    score = update_score(0, "Win", 1)
    assert score == 90

    score = update_score(0, "Win", 9)
    assert score == 10

    score = update_score(0, "Win", 10)
    assert score == 10


    score = update_score(100, "Too High", 0)
    assert score == 95

    score = update_score(100, "Too Low", 0)
    assert score == 95

    score = update_score(200, "Too High", 5)
    assert score == 195

    score = update_score(200, "Too Low", 10)
    assert score == 195

    score = update_score(0, "Unknown", 0)
    assert score == 0

    score = update_score(50, "Unknown", 5)
    assert score == 50


