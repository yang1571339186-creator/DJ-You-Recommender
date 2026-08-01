# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
| --- | --- | --- | --- |
| Secret = 73, Guess = 22 | Game to say "go higher" | Says "go lower" | The logic under the Check Guess function is back wards |
| Enter new game, play multiple times | Score decreases with wrong guesses | Score resets to zero every other attempt | Under the update_score function resets score to 0 after every even attempt |
| New game | New game with low and high range according to difficulty | Defaults to 0 to 100 every time | When the new game button is clicked, app.py generates a new game with a low and high range between 0 and 100 instead of using the low and high parameters |
| Start new game | Banner shows correct low and high numbers based on difficulty | Banner outputs 0 to 100 every time | The html code for the banner always uses a range between 0 and 100 instead using the low and high variables | 
|Switch difficulty|Game will select a number between low and high appropriate for the difficulty|Game will always use a low and high of 0 and 100|get_range_for_difficulty function doesn't string match as expected and instead always returns the default 0 and 100 range

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  - I used Claude Code as the AI tool for this project
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - I asked Claude for ideas to fix the new game button not producing the right difficult. Cluade was able to point me to the right code section and the right fix.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  - I asked Claude for the reason why the too high/too low hint is incorrect and Claude was unable to find the bug and instead suggested int type enforcement on the "secret" parameter, which will always be an int and not the root cause. I did as claude suggest and reran the app and the problem persisted

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - For visual bugs that are apparent to the user, i.e the banner not displaying correctly. I would verify through testing at the UI level to ensure display is correct. On the otherhand, backend bugs such as the get_range_for_difficulty function not returning correct ranges, is tested using pytest functions direct testing the get_range_for_difficulty through different inputs
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  - Testing test_check_guess with strings as guess and secret showed that the code has error where it casts strings to int too late. Meaning that the previous code will return the comparison between strings rather than as int values if guess and secrets were both strings
- Did AI help you design or understand any tests? How?
  - I used claude to create the test cases and verified the test cases to see if they make sense. I find that adding more detailed docstrings help AI create test cases with better accuracy

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  - Essentially, the reun method stops the execution of the current stack and reruns the script. However, the state of the session is maintained so that the state variables like difficulty and max range is maintained. 
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  - Use git commmit more frequently so that I'm don't worry about using changes. Furthermore, I would want to use 'plan' mode more frequently to ensure AI understands the assignment before making changes. 
- What is one thing you would do differently next time you work with AI on a coding task?
  - I would use AI to give me a high-level summary of the code base. Especially with a larger code base, it would be helpful to work with a high-level summary before digging into the code
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  - AI generates code with better context; in this case, I feel like being on top of documentation will helpp my AI agent work better and more efficiently
