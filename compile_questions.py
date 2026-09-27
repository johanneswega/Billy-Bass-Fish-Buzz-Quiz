from fisch import *
import json
import os

# Load questions from JSON
def load_questions(filename="questions.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

q = load_questions()
f = Fisch()

for i in range(len(q)):
    print(f"{i+1}/{len(q)}")
    if not os.path.exists(f'audio/q{i+1}'):
        os.makedirs(f'audio/q{i+1}')

    ready = f"Get ready for question {i+1} out of {len(q)}. The Question is from Category: {q[i]['category']}"
    question = f"The question is: {q[i]['question']}"
    A = f"Is it A: {q[i]['options'][0]}"
    B = f"or B: {q[i]['options'][1]}"
    C = f"or C: {q[i]['options'][2]}"
    D = f"or is it D: {q[i]['options'][3]}"

    f.gen_audio(ready, f'audio/q{i+1}/ready.wav')
    f.speak(f'audio/q{i+1}/ready.wav')

    f.gen_audio(question, f'audio/q{i+1}/question.wav')
    f.speak(f'audio/q{i+1}/question.wav')

    f.gen_audio(A, f'audio/q{i+1}/A.wav')
    f.speak(f'audio/q{i+1}/A.wav')

    f.gen_audio(B, f'audio/q{i+1}/B.wav')
    f.speak(f'audio/q{i+1}/B.wav')

    f.gen_audio(C, f'audio/q{i+1}/C.wav')
    f.speak(f'audio/q{i+1}/C.wav')

    f.gen_audio(D, f'audio/q{i+1}/D.wav')
    f.speak(f'audio/q{i+1}/D.wav')