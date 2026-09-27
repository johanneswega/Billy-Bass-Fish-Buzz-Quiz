from TTS.api import TTS
import sounddevice as sd
import sounddevice as sd
import soundfile as sf
import serial
import time
import sounddevice as sd
import serial
import time
import numpy as np
import os

class Fisch():
    # intialize serial communication and language model
    def __init__(self, model='Standard', speaker=None, speed=0.9, threshold=0.3):
        # Arduino setup
        # find USB port 
        usbport = [i for i in os.listdir('/dev') if 'cu.usbserial' in i][0]
        self.arduino = serial.Serial(f'/dev/{usbport}', 9600, timeout=0.1)
        time.sleep(2)
        print("\n Connected to Fisch! \n")

        # nice speaker is p230
        self.speaker = speaker

        # choose model
        if model=='Standard':
            model = "tts_models/en/vctk/vits"
            self.speaker = 'p230'
        if model=='German':
            model = 'tts_models/de/thorsten/vits'
        if model=='French':
            model = 'tts_models/fr/css10/vits'
        self.tts = TTS(model_name=model, progress_bar=True, gpu=False)
        print("\n Initialized Language Model! \n")

        # define threshold
        self.threshold = threshold

        # set speed 
        self.speed = speed

    # method to send commands to fisch via serial
    def send_command(self, command):
        self.arduino.write((command + '\n').encode())
        self.arduino.flush()

    # method to generate audio file
    def gen_audio(self, text, file):
        # generate audio file
        if self.speaker!=None:
            self.tts.tts_to_file(text=text, file_path=file, speaker=self.speaker, speed=self.speed)
        else:
            self.tts.tts_to_file(text=text, file_path=file, speed=self.speed)

    # method to speak a piece of text
    def speak(self, file, move=True, moveback=True):
        # Load audio
        data, samplerate = sf.read(file)
        # determine threshold for opening mouth
        threshold = self.threshold*np.max(data)

        # Play audio
        if move==True:
            self.send_command("MOVE FORWARD")
        sd.play(data, samplerate)
        step = int(samplerate * 0.05)  # 50 ms steps
        for i in range(0, len(data), step):
            segment = data[i:i+step]
            if np.max(np.abs(segment)) > threshold:
                self.send_command("OPEN MOUTH")
            else:
                self.send_command("CLOSE MOUTH")
            time.sleep(0.05)  # matches step duration

        sd.wait()
        self.send_command("CLOSE MOUTH")
        if moveback==True:
            self.send_command("MOVE BACK")

