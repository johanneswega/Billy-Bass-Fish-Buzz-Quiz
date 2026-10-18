# basic script to generate audio file used in the game
# can be used to change basic audios, like what the Fish is saying 
# if a specific player wins, etc.

# listen to the audio in the audio folder if you want to change 
# something specific --> keep the naming convention the same

# for instance the audio file "wP1.wav" is played to welcome player 1
# --> look inside the code of "FischQuiz.py" to see when which audio is played
# and what it means

# if you change the audio for the rules, you need to also change the text in the 
# list rules_text within the get_ready function within FischQuiz.py

# similar thing if you want to change the audio for announcing the winners

from fisch import *

f = Fisch()

text = """There will be thirty questions in total, covering a variety of categories."""

f.gen_audio(text, 'audio/rules2.wav')
f.speak('audio/rules2.wav')
