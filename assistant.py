import speech_recognition as sr
from time import ctime
import time
import playsound
import os
import random
from gtts import gTTS
import webbrowser

class user:
    name = ''
    def setName(self, name):
        self.name = name

def if_contains(terms):
    for term in terms:
        if term in voice_data:
            return True

r = sr.Recognizer() # initialise a recogniser
# listen for audio and convert it to text:
def record_audio(ask=False):
    with sr.Microphone() as source: # source is microphone
        if ask:
            lucy_speak(ask)
        audio = r.listen(source)  # listen for the audio via source
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)  # convert audio to text
        except sr.UnknownValueError: # error: recognizer does not understand
            lucy_speak('I did not get that')
        except sr.RequestError:
            lucy_speak('Sorry, the service is down') # error: recognizer is not connected
        print(f"You: {voice_data.lower()}") # print what user said
        return voice_data.lower()  

# get string and make a audio file to be played
def lucy_speak(audio_string):
    tts = gTTS(text=audio_string, lang='en') # text to speech(voice)
    r = random.randint(1,20000000)
    audio_file = 'audio' + str(r) + '.mp3'
    tts.save(audio_file) # save as mp3
    playsound.playsound(audio_file) # play the audio file
    print(f"Lucy: {audio_string}") # print what assistant said
    os.remove(audio_file) # remove audio file


def respond(voice_data):
    # 1: greetings
    if if_contains(['hey','hi','hello']):
        greetings = [f"Hey, how can I help you?", f"Hey, what's up?", f"I'm listening.", f"How can I help you?"]
        greet = greetings[random.randint(0,len(greetings)-1)]
        lucy_speak(greet)

    # 2: name
    if if_contains(["what is your name","what's your name","tell me your name"]):
        if user_obj.name:
            lucy_speak("My name is Lucy.")
        else:
            lucy_speak("My name is Lucy. What's your name?")
    # 3: user name
    if if_contains(["my name is","i am"]):
        user_name = voice_data.split("is")[-1].strip()
        lucy_speak(f"Okay, i will remember that {user_name}.")
        user_obj.setName(user_name) # remember name in user object

    # 4: greeting
    if if_contains(["how are you","how are you doing"]):
        lucy_speak(f"I'm very well, thanks for asking {user_obj.name}.")

    # 5: time
    if if_contains(["what's the time","tell me the time","what time is it","i need the time"]):
        lucy_speak(ctime())
    
    # 6: search
    if if_contains(["find"]):
        search = record_audio('What do you want to search for?')
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)
        lucy_speak('Here is what I found for ' + search)

    # 7: location
    if if_contains(["location"]):
        location = record_audio('What is the location?')
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        lucy_speak('Here is the location of ' + location)
    
    # 8: open notepad
    if if_contains(["notepad"]):
        os.system('notepad')
        lucy_speak('Done for you!')

    # 9: youtube
    if if_contains(["youtube"]):
            webbrowser.open("www.youtube.com")
            lucy_speak("Here is youtube for you!")

    # 10: github
    if if_contains(["github",]):
            webbrowser.open("https://www.github.com")
            lucy_speak("Here is github for you!")
    
    # 11: exiting
    if if_contains(["thank you","exit"]):
        lucy_speak('Goodbye')
        exit()
    

time.sleep(1)
lucy_speak('Hello!')
user_obj = user()
while 1:
    voice_data = record_audio() # get the voice input
    respond(voice_data) #respond