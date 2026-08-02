# Model Card — Three-Strikes You'reee Out


## Human Test

Manual spot-checks a person can run by playing a round and reading the clue
against expectations. The point is to confirm clues are relevant, name-free, and
readable — things the automated substring check can't judge.

##Ronald Acuna Jr. (International Star Player)
| Input | OutPut | Result |
| What is his nickname| El Abusador | Pass|
| What Highschool |Didn't go to high school| Pass |
| Best Career Moment | Starting the 40-90 Club |Pass|

##Hunter Goodman (American All Start)
| Input | OutPut | Result |
| What is his nickname| None Nickname | Pass (His nickname is Goody but it reveals lastname, so none is outputed)|
| What Highschool |University of Memphis| Pass |
| Best Career Moment | Grandslam vs Arizaon Cardinals|Pass|


##Ben Williamson(Unknown Player)
| Input | OutPut | Result |
| What is his nickname| Non Nickname | Pass |
| What Highschool |College of William and Mary| Pass |
| Best Career Moment | Gettign drafted|Pass|(I would argue his first MLB hit)

##Limitation 
The AI can be a bit unpredictable for players that are not as well-known. Altough we supply enough information to keep the model focused to search for baseball players, sometimes obsecure facts about player's nickname and best moments may not be available

##AI Misuse
One of the main things I want to prevent is the AI clue generator from giving away player's information thus ruining the game. So I added a validator to ensure that the player's name is not given away in the clue and that we have discrete clues with prompts that are optimized to prevent prompt injection

##Surprise
No major surprises since the game is fairly controlled

##Working with AI
The AI gave really good ideas in terms of building the guardrails for the prompt to ensure reliable output. However, one major issue with AI code came during code refactoring. I had originally imagained a sequentially clue reveal(one clue after the other) but changed it to discrete types of clues. However, AI never picked up that the clue reveal code should be refactored to the new setting and thuse the clue reveal process was incorrect for a while. 
