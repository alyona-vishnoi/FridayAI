import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
# import random
# import numpy as np
import pyautogui

chatStr = ""
def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Alyona: {query}\n Friday: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    # print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    # with open(f"Openai/prompt- {random.randint(1, 2343434356)}", "w") as f:
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)

def say(text):
    os.system(f'say "{text}"')

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone(device_index = 0) as source:
        # r.pause_threshold =  0.6
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Friday"
            print(e)

if __name__ == '__main__':
    print('Welcome to Friday A.I')
    say("Friday A.I")
    while True:
        print("Listening...")
        query = takeCommand()
        # todo: Add more sites
        sites = [["portfolio", "https://www.alyonavishnoi.com"], ["youtube", "https://www.youtube.com"], ["github", "https://github.com/"], ["google", "https://www.google.com"], ]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} ...")
                webbrowser.open(site[1])
        # todo: Add a feature to open spotify and play songs
        if "open music" in query:
            os.system(f"open /System/Applications/Spotify.app")
            # Wait for Spotify to open
            pyautogui.sleep(5)
            # Press the spacebar to play/pause the music
            pyautogui.press('space')
        # todo: Add a feature to ask for the time
        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"The time is {min} minutes after {hour}")
        # todo: Add a feature to open facetime
        elif "open facetime".lower() in query.lower():
            os.system(f"open /System/Applications/FaceTime.app")
        # todo: Add a feature to open password manager
        elif "open pass".lower() in query.lower():
            os.system(f"open /Applications/Passky.app")
        # todo: Add a feature to use chatgpt
        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)
        # quit
        elif "Friday Quit".lower() in query.lower():
            exit()
        # todo: Add a feature to reset chat
        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else:
            print("Chatting...")
            chat(query)
