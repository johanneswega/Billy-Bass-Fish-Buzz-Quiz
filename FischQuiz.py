import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer, QEventLoop
from useful_functions import *
from fisch import *
import resources_rc

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

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, q):
        # load the .ui file
        super().__init__()
        uic.loadUi("gui.ui", self) 

        # get question
        self.q = q
        self.qind = 0

        # enables line wrapping
        self.question.setWordWrap(True)
        self.info.setWordWrap(True)

        # set all question labels to clear
        self.clear_question_labels()
        self.nextButton.hide()

        # connect click to handler
        self.startButton.clicked.connect(self.on_startButton_click)

        # connect click to handler
        self.nextButton.clicked.connect(self.on_nextButton_click)

    # button press to start game
    def on_startButton_click(self):
        self.startButton.hide()
        #pyttsx3.speak("Let's start the game then folks! But before we start let's make sure everyone is there.")
        f.speak('audio/hello.wav')
        self.current_player = 1  # start with player 1
        QTimer.singleShot(1500, lambda: self.check_whos_there(self.current_player))

    # function to assign controllers to players
    def check_whos_there(self, player_num):
        if player_num==1:
            f.speak('audio/P1.wav', moveback=False)
        if player_num==2:
            f.speak('audio/P2.wav', move=False, moveback=False)
        if player_num==3:
            f.speak('audio/P3.wav', move=False, moveback=False)     
        if player_num==4:
            f.speak('audio/P4.wav', move=False, moveback=False)  

        self.info.setText(f'Player {player_num}, are you there? Please press your buzzer!')

        # set lights depending on which player we expect
        lights = [False, False, False, False]
        lights[player_num - 1] = True
        buzzer.set_lights(lights)
        buzzer.start_listening()

        # start timer to poll file
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.check_buzz(player_num))
        self.timer.start(100)  # check every 100ms

    def check_buzz(self, player_num):
        with open('answers.txt', 'r') as fh:
            for line in fh:
                if f"Red button pressed on buzzer {player_num - 1}!" in line:
                    buzzer.set_lights([False, False, False, False])
                    if player_num==1:
                        f.speak('audio/wP1.wav', move=False, moveback=False)
                    if player_num==2:
                        f.speak('audio/wP2.wav', move=False, moveback=False)
                    if player_num==3:
                        f.speak('audio/wP3.wav', move=False, moveback=False)
                    if player_num==4:
                        f.speak('audio/wP4.wav', move=False, moveback=True)
                    self.info.setText(f'Welcome Player {player_num}!')
                    self.timer.stop()
                    buzzer.stop_listening()
                    clear_answer_file()

                    if player_num < 4:
                        # go to next player after 1 seconds
                        self.current_player += 1
                        QTimer.singleShot(1500, lambda: self.check_whos_there(self.current_player))
                    else:
                        # all 4 confirmed → show category
                        self.rule_index = 0
                        QTimer.singleShot(1000, lambda: self.get_ready(self.rule_index))
                    return
                
    def get_ready(self, i):
        rules_text = ["Great, everyone's here! Before we begin, let me quickly explain the rules of the game. Listen carefully — I'll only go over them once.",
                      "There will be thirty questions in total, covering a variety of categories. Every fifth question will match the theme of tonight's party — spooky Halloween!",
                      "Each correct answer earns you one point. I'll read each question aloud along with the four possible answers. When I'm done, your controllers will light up, meaning it's time to answer. You'll have fifteen seconds to respond, and only your first answer counts, so make sure to hit the right color on your buzzer.",
                      "Doesn't seem to difficult does it?"]
        if i<3:
            self.info.setText(rules_text[i])
            QTimer.singleShot(200, lambda: f.speak(f'audio/rules{i+1}.wav'))
            self.rule_index += 1
            QTimer.singleShot(1200, lambda: self.get_ready(self.rule_index))
        else:
            self.info.setText(rules_text[i])
            QTimer.singleShot(200, lambda: f.speak(f'audio/rules{i+1}.wav'))
            QTimer.singleShot(1200, self.start)

    def start(self):
        self.info.setText('')
        f.speak(f'audio/start.wav')
        QTimer.singleShot(1000, self.show_category)

    def on_nextButton_click(self):
        self.nextButton.hide()
        self.clear_question_labels()
        self.qind += 1
        # wait 2 s and then change category label
        if self.qind != len(questions):
            self.q = questions[self.qind]
            QTimer.singleShot(2000, self.show_category)
        else:
            QTimer.singleShot(2000, self.show_winner)

    def clear_question_labels(self):
        self.info.setText('')
        self.category.setText('') 
        self.question.setText('') 
        self.A.setText('') 
        self.B.setText('')
        self.C.setText('')
        self.D.setText('')

        self.AP1.setText('') 
        self.AP2.setText('') 
        self.AP3.setText('') 
        self.AP4.setText('') 

        self.BP1.setText('') 
        self.BP2.setText('') 
        self.BP3.setText('') 
        self.BP4.setText('') 

        self.CP1.setText('') 
        self.CP2.setText('') 
        self.CP3.setText('') 
        self.CP4.setText('') 

        self.DP1.setText('') 
        self.DP2.setText('') 
        self.DP3.setText('') 
        self.DP4.setText('') 

        self.qimage.hide()
        self.Aimage.hide()
        self.Bimage.hide()
        self.Cimage.hide()
        self.Dimage.hide()

        # set font sizes back to normal
        font = self.A.font()
        font.setBold(False)    
        self.A.setFont(font)
        self.B.setFont(font)
        self.C.setFont(font)
        self.D.setFont(font)    

    def show_category(self):
        self.info.setText('')
        # make sure answers.txt is empty
        clear_answer_file()

        self.category.setText(f"Category: {self.q['category']}")
        f.speak(f"audio/q{self.qind + 1}/ready.wav")
        QTimer.singleShot(2000, self.show_question)

    def show_question(self):
        self.question.setText(f"{self.q['question']}")
        self.qimage.show()
        QTimer.singleShot(200, lambda: f.speak(f"audio/q{self.qind + 1}/question.wav", moveback=False)) 
        QTimer.singleShot(1000, self.show_A)

    def show_A(self):
        self.A.setText(f"A: {self.q['options'][0]}")
        self.Aimage.show()
        f.speak(f"audio/q{self.qind + 1}/A.wav", move=False,  moveback=False)
        QTimer.singleShot(300, self.show_B)

    def show_B(self):
        self.B.setText(f"B: {self.q['options'][1]}")
        self.Bimage.show()
        f.speak(f"audio/q{self.qind + 1}/B.wav", move=False,  moveback=False)
        QTimer.singleShot(300, self.show_C)

    def show_C(self):
        self.C.setText(f"C: {self.q['options'][2]}")
        self.Cimage.show()
        f.speak(f"audio/q{self.qind + 1}/C.wav", move=False,  moveback=False)
        QTimer.singleShot(300, self.show_D)

    def show_D(self):
        self.D.setText(f"D: {self.q['options'][3]}")
        self.Dimage.show()
        f.speak(f"audio/q{self.qind + 1}/D.wav", move=False,  moveback=True)
        buzzer.start_listening()
        buzzer.set_lights([True, True, True, True]) 
        # play countdown music
        data, samplerate = sf.read('audio/countdown_fast.wav')
        sd.play(data, samplerate)
        QTimer.singleShot(17000, self.show_next)

    def show_next(self):
        buzzer.set_lights([False, False, False, False]) 
        buzzer.stop_listening()
        # set the fontsize of the correct answer to bold
        font = self.A.font()
        font.setBold(True) 
        if self.q['answer']==0:
            self.A.setFont(font)
        if self.q['answer']==1:
            self.B.setFont(font)
        if self.q['answer']==2:
            self.C.setFont(font)
        if self.q['answer']==3:
            self.D.setFont(font)
        self.update_points()
        self.nextButton.show()

    def update_points(self):
        # get answers 
        a1, a2, a3, a4 = get_results()
        update_score(a1, a2, a3, a4, self.q)
        celebrate(a1, a2, a3, a4, self.q, f)

        # set progress bars and labels to current score
        self.player1_score.setValue(player_score[0])
        self.player1_points.setText(f"{player_score[0]} points")

        self.player2_score.setValue(player_score[1])
        self.player2_points.setText(f"{player_score[1]} points")

        self.player3_score.setValue(player_score[2])
        self.player3_points.setText(f"{player_score[2]} points")

        self.player4_score.setValue(player_score[3])
        self.player4_points.setText(f"{player_score[3]} points")

        # show player 1's answer
        if a1 == 'A':
            self.AP1.setText('P1')
        if a1 == 'B':
            self.BP1.setText('P1')
        if a1 == 'C':
            self.CP1.setText('P1')
        if a1 == 'D':
            self.DP1.setText('P1')

        # show player 2's answer
        if a2 == 'A':
            self.AP2.setText('P2')
        if a2 == 'B':
            self.BP2.setText('P2')
        if a2 == 'C':
            self.CP2.setText('P2')
        if a2 == 'D':
            self.DP2.setText('P2')

        # show player 3's answer
        if a3 == 'A':
            self.AP3.setText('P3')
        if a3 == 'B':
            self.BP3.setText('P3')
        if a3 == 'C':
            self.CP3.setText('P3')
        if a3 == 'D':
            self.DP3.setText('P3')

        # show player 4's answer
        if a4 == 'A':
            self.AP4.setText('P4')
        if a4 == 'B':
            self.BP4.setText('P4')
        if a4 == 'C':
            self.CP4.setText('P4')
        if a4 == 'D':
            self.DP4.setText('P4')

    def show_winner(self):
        self.info.setText("Oi your cheeky bastards, seems like the game is already over! I know you smart-asses have already figured out who won already if you ain't stupid or blind on both of your eyes. Anyways I will still epically anounce who won! Just hold on a sec, I ain't to good at head calculatin' ...")
        QTimer.singleShot(200, lambda: f.speak("audio/final.wav"))
        QTimer.singleShot(2000, self.figure_out_winner)

    def figure_out_winner(self):
        max_score = max(player_score)
        a = [1, 2, 3, 4]
        winners = [player for player in a if player_score[player-1] == max_score]

        if len(winners)==1:
            if winners[0]==1:
                text = "HOLY MACKEREL! Player 1 just wiped the floor with the rest of ya! That’s right—Player 1 is the champion of chaos, the undisputed ruler of the vodka sea! By decree of my glorious masters Johannes and Oriane, they shall receive unlimited vodka shots and eternal bragging rights till dawn!"
            elif winners[0]==2:
                text = "Oi oi oi, looks like Player 2’s got the moves and the brain cells the rest of you lost hours ago! The almighty masters Johannes and Oriane decree: pour them endless vodka shots until they start speaking fluent fish! Congratulations, you slippery legend!"
            elif winners[0]==3:
                text = "Would ya look at that—Player 3 just destroyed the competition like a shark at a sushi buffet! All hail the vodka overlord, as blessed by the holy names Johannes and Oriane! Someone bring this legend a trophy—or at least a shot glass!"
            else:
                text = 'Sweet Neptune’s beard! Player 4 just won the whole bloody thing! Absolute domination, like Poseidon on a bender! My masters Johannes and Oriane are raising their ghostly goblets in your honor—may your liver survive the night!'
            self.info.setText(text)
            QTimer.singleShot(200, lambda: f.speak(f"audio/P{winners[0]}win.wav"))

        elif len(winners)==2:
            first = winners[0]
            second = winners[1]
            text = f"Oh ho ho! A bloody tie between players {first} and {second}! You two legends fought so hard even my circuits can't tell who's better! Masters Johannes and Oriane declare: both of ya get infinite vodka shots, and you must drink until one of ya falls—then we'll really know who's the winner!"
            self.info.setText(text)
            QTimer.singleShot(200, lambda: f.speak(f'audio/P{first}_P{second}_win.wav'))       

        elif len(winners)==3:
            first = winners[0]
            second = winners[1]
            third = winners[2]
            check = ['Win' if j in winners else 'Loose' for j in a]
            looser = check.index('Loose') + 1
            text = f"Looks like someone belongs into a mental institution, right player {looser}? Bloody hell, we indeed got a three-way tie between players {first}, {second} and {third}! You chaotic gremlins broke the system! Johannes and Oriane are cackling from the shadows! Each of ya gets endless Vodka shots as your prize money. Drink responsibly — or irresponsibly, I’m not your fish-dad!"
            self.info.setText(text)
            QTimer.singleShot(200, lambda: f.speak(f'audio/P{looser}_loose.wav'))     

        else:
            text = "WHAT IN THE FISHSTICKS?! A FOUR-WAY TIE?! This is madness! You’ve reached party legend status! Johannes and Oriane are officially too impressed (or too drunk) to decide. Everyone gets unlimited vodka shots, the respect of the sea, and a hangover so bad even I’ll feel it tomorrow!"
            self.info.setText(text)
            QTimer.singleShot(200, lambda: f.speak('audio/allwin.wav')) 

# start app
f = Fisch()
app = QtWidgets.QApplication(sys.argv)
window = MyWindow(q=questions[0])
window.showFullScreen()
sys.exit(app.exec_())