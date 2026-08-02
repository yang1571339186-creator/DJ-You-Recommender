"""Streamlit UI for the MLB Player Guessing Game.

Thin view layer over game_models.Game. All game logic (picking the secret
player, generating/validating clues, scoring) lives in the model classes; this
file only handles session state and rendering.
"""

import streamlit as st

from game_models import Clue, Game


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------


def new_game(team: str | None = None, awards: bool = False) -> None:
    """Create a fresh Game and start a round. No clues are retrieved up front.

    st.session_state.clues holds one slot per clue; each stays None until the
    user reveals it, at which point the clue text is fetched and cached there.
    """
    game = Game()
    game.start_new_round(team=team, awards=awards)
    st.session_state.game = game
    st.session_state.clues = [None] * game.MAX_CLUES
    st.session_state.guesses = []  # list of guessed Player objects
    st.session_state.messages = []


def reveal_clue(index: int) -> None:
    """Fetch the clue at `index` on demand and cache it in session state."""
    if st.session_state.clues[index] is None:
        st.session_state.clues[index] = st.session_state.game.get_clue(index)


def get_game() -> Game:
    if "game" not in st.session_state:
        new_game()
    return st.session_state.game


# ---------------------------------------------------------------------------
# Page
# ---------------------------------------------------------------------------

st.set_page_config(page_title="MLB Player Guesser", page_icon="⚾")

st.title("⚾ MLB Player Guessing Game")
st.caption("Guess the mystery 2025 MLB player from AI-generated clues.")

game = get_game()

st.sidebar.header("New Round Filters")
# Autocomplete over the actual team codes in the data. "" = any team.
filter_team = st.sidebar.selectbox(
    "Team (optional)",
    options=["", *game.all_teams()],
    index=0,
    help="Pick a team to restrict the mystery player, or leave as Any.",
    placeholder="Any team",
)
filter_awards = st.sidebar.checkbox("All-Stars only", value=False)

if st.sidebar.button("Start New Round 🔁"):
    new_game(team=filter_team or None, awards=filter_awards)
    st.rerun()

# ---------------------------------------------------------------------------
# Player stat card — everything about the secret player EXCEPT name and team.
# These are the reasoning aids; name/team stay hidden (team is a "New Round"
# filter, revealing it would defeat the guess).
# ---------------------------------------------------------------------------


def render_stat_card(player) -> None:
    """Show the secret player's stats, including team, omitting only the name."""
    st.subheader("Mystery Player Stats")

    def fmt(value, decimals=None):
        if value is None:
            return "—"
        if decimals is not None:
            return f"{value:.{decimals}f}"
        return str(value)

    top = st.columns(4)
    top[0].metric("Position", fmt(player.position) or "—")
    top[1].metric("Age", fmt(player.age))
    top[2].metric("WAR", fmt(player.war, 1))
    top[3].metric("Games", fmt(player.games))

    bottom = st.columns(4)
    bottom[0].metric("HR", fmt(player.home_runs))
    bottom[1].metric("AVG", fmt(player.batting_avg, 3))
    bottom[2].metric("OBP", fmt(player.on_base_pct, 3))
    bottom[3].metric("SLG", fmt(player.slugging, 3))

    stat = st.columns(3)
    stat[0].metric("OPS", fmt(player.ops, 3))
    stat[1].metric("Team", fmt(player.team) or "—")

    stat = st.columns(1)
    awards = player.awards if player.awards and player.awards != "None" else "—"
    stat[0].metric("Awards", awards)
    


render_stat_card(game.secret_player)
st.divider()

st.subheader("Clues")
for i, clue_text in enumerate(st.session_state.clues):
    label = Clue.CLUE_LABELS[i]
    if clue_text is not None:
        st.info(f"**{label}:** {clue_text}")
    else:
        if st.button(f"Reveal: {label} 🔍", key=f"reveal_{i}"):
            try:
                with st.spinner("Generating clue…"):
                    reveal_clue(i)
            except Exception:
                # Gemini call failed (network, API key, rate limit, etc.).
                # Leave the clue unrevealed so the button can be tried again.
                st.error("Couldn't generate that clue. Please try again.")
            else:
                st.rerun()

revealed = sum(1 for c in st.session_state.clues if c is not None)
st.caption(f"Clues revealed: {revealed} / {game.MAX_CLUES}")

with st.expander("Developer Debug Info"):
    st.write("Secret player:", game.secret_player.name if game.secret_player else None)
    st.write("Clue index:", game.clue_index)
    st.write("Attempts:", game.attempts)
    st.write("Score:", game.score)
    st.write("Status:", game.status)

# ---------------------------------------------------------------------------
# Round already over
# ---------------------------------------------------------------------------

if game.status != "playing":
    if game.status == "won":
        st.success(
            f"🎉 You won! It was **{game.secret_player.name}**. "
            f"Final score: {game.score}"
        )
    else:
        st.error(
            f"Out of guesses! It was **{game.secret_player.name}**. "
            f"Score: {game.score}"
        )
    st.stop()

# ---------------------------------------------------------------------------
# Guess input
# ---------------------------------------------------------------------------

st.subheader("Make a guess")
st.caption(f"Guesses remaining: {game.MAX_CLUES - game.attempts}")

# Previous guesses — name, team, position of each player already guessed.
if st.session_state.guesses:
    st.markdown("**Previous guesses**")
    st.table(
        [
            {
                "Name": p.name,
                "Team": p.team,
                "Position": p.position,
            }
            for p in st.session_state.guesses
        ]
    )

# Autocomplete: type to filter the fixed list of 2025 player names. A blank
# leading option keeps the box empty until the user picks, so no accidental
# submit of a pre-filled name.
guess = st.selectbox(
    "Player name:",
    options=["", *game.all_names],
    index=0,
    key=f"guess_{game.attempts}",
    placeholder="Start typing a player's name…",
)
submit = st.button("Submit Guess 🚀")

if submit:
    if not guess:
        st.warning("Pick a player from the list.")
    else:
        # Record the guessed player's details (does not touch secret_player).
        guessed_player = game.retrieve_guess(guess)
        if guessed_player is not None:
            st.session_state.guesses.append(guessed_player)
        correct = game.check_guess(guess)
        if correct:
            st.balloons()
        else:
            remaining = game.MAX_CLUES - game.attempts
            if remaining > 0:
                st.warning(f"Wrong guess. {remaining} guess(es) left.")
        st.rerun()

st.divider()
st.caption("Clues generated by Gemini and screened so they never leak the name.")
