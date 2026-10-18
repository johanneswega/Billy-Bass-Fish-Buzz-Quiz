# Billy Bass Quiz Game

A four-player quiz game hosted by a singing **Big Mouth Billy Bass** fish, with **PlayStation 2 Buzz! controllers** used as the player input devices.

[![Basic Demo](https://img.youtube.com/vi/9lwKqI7PBsQ/hqdefault.jpg)](https://youtu.be/9lwKqI7PBsQ)
*Click on the image to watch the demo on YouTube*

The project combines hardware and software to create a quirky, interactive game-show experience:

* 🐟 **Arduino** controls the Billy Bass fish and brings the game host to life.
* 🎮 **PS2 Buzz! controllers** are used by the four players to answer questions.
* 🖥️ **Python + PyQt** handles the game logic, controller input, and graphical user interface.
* 🔌 Custom hardware and software integration connects everything into a single playable system.

The result is a physical quiz game where Billy Bass acts as the host while four players compete using classic Buzz! controllers.
## Installation

The project runs on **Python 3.11** and is intended to run inside a dedicated Conda environment.

All required packages and dependencies can be installed using the included `fisch.yml` file:

```bash
conda env create -f fisch.yml
conda activate Fisch
```
Some of the most important packages used by the project are:

* `TTS` — text-to-speech generation
* `sounddevice` — audio playback
* `pyserial` — serial communication with the Arduino
* `pybuzzers` — communication with the PlayStation 2 Buzz! controllers

The Billy Bass functionality is implemented in the `Fisch` class in `fisch.py`.

This file contains the code responsible for:

* Generating speech using text-to-speech
* Communicating with the Arduino over USB/serial
* Sending commands to control the Billy Bass body and mouth motors
* Playing generated speech through the computer's audio output

Have a look at `fisch.py` to understand how the fish is controlled and how speech and movement are coordinated.

The Arduino is connected via USB and is detected using the following code within `fisch.py`:

```python
usbport = [i for i in os.listdir('/dev') if 'cu.usbserial' in i][0]

self.arduino = serial.Serial(f'/dev/{usbport}', 9600, timeout=0.1)
```

This is currently configured for **macOS**. If you are using another operating system, you may need to modify the USB port detection to match the device path used by your system.

The Arduino code can be found in the `Arduino Code` folder if you want to see how the motor commands are received and handled.

The main game interface is implemented in `FischQuiz.py`. This contains the actual quiz game logic and graphical interface. See the sections below for more information about setting up and running a game.

## Hardware

You will need:

* A Big Mouth Billy Bass
* An Arduino Mini or similar microcontroller
* A set of four PlayStation 2 Buzz! controllers with USB adapter

To make the fish move, I largely followed this excellent tutorial by Donald Bell:

https://maker.pro/arduino/projects/how-to-animate-billy-bass-with-bluetooth-audio-source

I also used the Arduino code from this tutorial, which can be found in the `Arduino Code` folder.

In the tutorial, he modifies the Billy Bass to add internal speakers and a Bluetooth audio interface. These modifications are not required for this project, unless you want to use the Billy Bass itself as the speaker, which does make the experience more realistic when the fish is speaking.

For the basic functionality of this project, you essentially only need the **H-bridge motor driver** to control the Billy Bass's mouth and body motors.

## Setting Up a Game

The easiest way to set up a new game is to clone the repository and create a separate copy for your quiz:

```bash
git clone https://github.com/johanneswega/Billy-Bass-Fish-Buzz-Quiz.git
mv Billy-Bass-Fish-Buzz-Quiz New_Quiz
cd New_Quiz
rm -rf .git
```

This gives you a standalone copy of the project, including the basic audio files used for announcing the rules and other game instructions.

### 1. Add Your Questions

Fill in `questions.json` with the questions for your quiz. For a standard party, I normally use 30 questions.

Each question should follow this format:

```json
[
  {
    "category": "Halloween",
    "question": "In which country is Užgavėnės celebrated, a Halloween-like tradition where people dress up and go door-to-door asking for money?",
    "options": ["Lithuania", "Poland", "Romania", "Belarus"],
    "answer": 0
  }
]
```

Each question contains the following fields:

* `category`: The category of the question.
* `question`: The question text.
* `options`: A list of four possible answers.
* `answer`: The index of the correct answer, starting at `0` for the first option, `1` for the second, and so on.

### 2. Generate the Question Audio

Once you have filled in `questions.json`, run the question compilation script:

```bash
python compile_questions.py
```

This generates audio files for each question and its answer options. For example, you should find files such as `audio/q1/A.wav` in the generated audio directories.

### 3. Check the Bluetooth Connection

There is currently a known issue when using the Billy Bass's built-in Bluetooth speaker. Before starting the game, make sure your laptop is **not connected to the `LQSC_BT` Bluetooth speaker** on the fish. The easiest workaround is to turn off Bluetooth on your laptop altogether.

### 4. Customize the Additional Audio (Optional)

If you want to change the greetings, rules, or other phrases spoken by Billy Bass, have a look at `gen_audio.py` and follow the instructions in that file. This step is optional. For a basic quiz game, the existing audio files are sufficient.

### 5. Start the Game

After generating all the question audio files, start the game with:

```bash
python FischQuiz.py
```

The game should now launch, and you're ready to play!