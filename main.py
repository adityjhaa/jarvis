import speech_recognition as sr
import pyttsx3

import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')

import openai
openai.api_key = OPENAI_KEY

def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

recognizer = sr.Recognizer()

def RecordText():
    try:

        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)

            print("I am listening, Sir!")

            recorded_audio = recognizer.listen(source)
        
        try:
            text = recognizer.recognize_google(recorded_audio, language="en-US")
            return text


        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio.")
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
    except Exception as ex:
        print("Error during recognition:", ex)

def send_to_GPT(messages, model="gpt-3.5-turbo"):

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].message.content
    messages.append(response.choice[0].message)
    return message


messages = [{"role":"user", "content":"Please act like Jarvis from Iron man."}]
while(1):
    text = RecordText()
    messages.append({"role":"user", "content":text})
    response = send_to_GPT(messages)

    SpeakText(response)

    print(response)

