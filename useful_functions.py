import json
import pybuzzers
import time
import os

### intialize buzzers ###
# Get a list of all connected buzzers, and pick out the first one
buzzer = pybuzzers.get_all_buzzers()[0]

# Turn on the light of all controllers
buzzer.set_lights([False, False, False, False])

# Define an event handler we want to run every time a button is pressed
def respond_to_press(buzzer_set: pybuzzers.BuzzerSet, buzzer: int, button: int):
    button_colour = pybuzzers.COLOUR[button]
    # open file handler and write output to txt file
    fh = open("answers.txt", "a")
    fh.write(f"{button_colour} button pressed on buzzer {buzzer}! \n")
    fh.close()

# Register this event handler with the BuzzerSet instance
buzzer.on_button_down(respond_to_press)

# Load questions from JSON
def load_questions(filename="questions.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)
    
# function to split string and to get answer
def split_string(p):
    if len(p)==0:
        return ''
    else:
        return colors_to_choice[p[0][:p[0].find(' ')]]
    
# function to read answers.txt and get results
def get_results():
    # make lists for player and store their button presses in them
    p1, p2, p3, p4 = [], [], [], []
    # open answers.txt and get the answers
    fh = open("answers.txt", "r")
    for line in fh:
        if 'buzzer 0' in line:
            p1.append(line)
        if 'buzzer 1' in line:
            p2.append(line)
        if 'buzzer 2' in line:
            p3.append(line)
        if 'buzzer 3' in line:
            p4.append(line)
    fh.close()

    # return first registered answer of players
    return split_string(p1), split_string(p2), split_string(p3), split_string(p4)

# function to update score 
def update_score(a1, a2, a3, a4, q):
    if a1 == labs[q['answer']]:
        player_score[0] += 1
    if a2 == labs[q['answer']]:
        player_score[1] += 1
    if a3 == labs[q['answer']]:
        player_score[2] += 1
    if a4 == labs[q['answer']]:
        player_score[3] += 1       
    # write score content to file 
    content = f'''Player , Points \n
    #1, {player_score[0]}\n
    #2, {player_score[1]}\n
    #3, {player_score[2]}\n
    #4, {player_score[3]}\n''' 
    with open('score.txt', 'w') as f:
        f.write(content)

def celebrate(a1, a2, a3, a4, q, f):
    correct = labs[q['answer']]
    answers = [a1, a2, a3, a4]

    # check if correct 
    check = [1 if i==correct else 0 for i in answers]

    if check[0]==1 and check[1]==1 and check[2]==1 and check[3]==1:
        f.speak('audio/call.wav')
    if check[0]==0 and check[1]==0 and check[2]==0 and check[3]==0: 
        f.speak('audio/stupid.wav')
    if check[0]==1 and check[1]==1 and check[2]==0 and check[3]==0: 
        f.speak('audio/c12.wav')
    if check[0]==1 and check[1]==0 and check[2]==0 and check[3]==1: 
        f.speak('audio/c14.wav')
    if check[0]==0 and check[1]==1 and check[2]==1 and check[3]==0: 
        f.speak('audio/c23.wav')
    if check[0]==0 and check[1]==1 and check[2]==0 and check[3]==1: 
        f.speak('audio/c24.wav')
    if check[0]==0 and check[1]==0 and check[2]==1 and check[3]==1: 
        f.speak('audio/c34.wav')
    if check[0]==0 and check[1]==1 and check[2]==1 and check[3]==1: 
        f.speak('audio/w1.wav')
    if check[0]==1 and check[1]==0 and check[2]==1 and check[3]==1: 
        f.speak('audio/w2.wav')
    if check[0]==1 and check[1]==1 and check[2]==0 and check[3]==1: 
        f.speak('audio/w3.wav')
    if check[0]==1 and check[1]==1 and check[2]==1 and check[3]==0: 
        f.speak('audio/w4.wav')
    if check[0]==1 and check[1]==0 and check[2]==0 and check[3]==0: 
        f.speak('audio/o1.wav')
    if check[0]==0 and check[1]==1 and check[2]==0 and check[3]==0: 
        f.speak('audio/o2.wav')
    if check[0]==0 and check[1]==0 and check[2]==1 and check[3]==0: 
        f.speak('audio/o3.wav')
    if check[0]==0 and check[1]==0 and check[2]==0 and check[3]==1: 
        f.speak('audio/o4.wav')


# function to clear answer file
def clear_answer_file():
    file_to_delete = open("answers.txt",'w')
    file_to_delete.close()

# function to print player score
def print_score():
    print('\n')
    for player, score in enumerate(player_score):
        print(f"Player {player + 1}: {score} points \n")
    
# function to ask question
def ask_question(q):
    # make sure answers.txt is empty
    file_to_delete = open("answers.txt",'w')
    file_to_delete.close()

    print_score()
    time.sleep(3)
    os.system('clear')

    # print question
    print(f"\nCategory: {q['category']} \n")
    print(f"Question: {q['question']} \n")
    for i, option in enumerate(q['options']):
        print(f"{labs[i]}) {option}")

    # start listening to buzzer presses
    # for 10 seconds
    start_time = time.time()
    time_limit = 10
    #print(f"\nYou have {time_limit} seconds to answer! Press your buzzer!")
    buzzer.start_listening()
    while time.time() - start_time < time_limit:
        # Turn on the light of all controllers
        buzzer.set_lights([True, True, True, True]) 
    # Turn off lights on all controllers
    buzzer.set_lights([False, False, False, False]) 
    buzzer.stop_listening()

    # get answers 
    a1, a2, a3, a4 = get_results()

    # display correct answer
    os.system('clear')
    print(f"\nCategory: {q['category']} \n")
    print(f"Question: {q['question']} \n")
    for i, option in enumerate(q['options']):
        if i == q['answer']:
            s = f"CORRECT: {labs[i]}) {option}"
        else:
            s = f"FALSE: {labs[i]}) {option}"
        # display the answers of the players
        if a1 == labs[i]:
            s += ' (P1) '
        if a2 == labs[i]:
            s += ' (P2) '
        if a3 == labs[i]:
            s += ' (P3) '
        if a4 == labs[i]:
            s += ' (P4) '            
        print(s)
    time.sleep(3)
    os.system('clear')

    update_score(a1, a2, a3, a4, q)
    os.system('clear')
    print_score()
    time.sleep(3)
    os.system('clear')

player_score = [0, 0, 0, 0]
questions = load_questions()
# color button to A-D dictonary
colors_to_choice = {'Blue': 'A', 'Orange': 'B', 'Green': 'C', 'Yellow': 'D', 'Red': 'Invalid'}
labs = ['A', 'B', 'C', 'D', 'Invalid']
print(len(questions))