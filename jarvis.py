import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import pyaudio
import wave
import pywhatkit as wk
import pyautogui
import time

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
  engine.say(audio)
  engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
     speak("Good Morning!")
    elif hour >= 12 and hour < 18:
     speak("Good Afternoon!")
    else:
     speak("Good Evening!")
    speak("I am Jarvis. How may I help you")

def takeCommand():
   try:
      CHUNK = 1024
      FORMAT = pyaudio.paInt16
      CHANNELS = 2
      RATE = 44100
      RECORD_SECONDS = 5
      WAVE_OUTPUT_FILENAME = "output.wav"
  
      p = pyaudio.PyAudio()
      stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,frames_per_buffer=CHUNK)
      
      print("Listening...")
     
      frames = []
      for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
         data = stream.read(CHUNK)
         frames.append(data)

      print("Recognizing...")

      stream.stop_stream()
      stream.close()
      p.terminate()

      wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
      wf.setnchannels(CHANNELS)
      wf.setsampwidth(p.get_sample_size(FORMAT))
      wf.setframerate(RATE)
      wf.writeframes(b''.join(frames))
      wf.close()

      r = sr.Recognizer()
      with sr.AudioFile("output.wav") as source:
         audio = r.record(source)
      try:
         text = r.recognize_google(audio)
         return text
      except sr.UnknownValueError:
       return "Sorry, I didn't understand that"
   except Exception as e:
       print(f"Error: {e}")
       return "None"

if __name__ == "__main__":
  wishMe()
  while True:
    query = takeCommand().lower()

    if 'hello jarvis' in query:
       print('yes sir')
       speak('yes sir')
    
    if 'open google' in query:

       webbrowser.open("https://www.google.com")
       speak("What would you like to search on google?")
       search_term = takeCommand()
       url = f"https://www.google.com/search?q=%7B{search_term}%7D"
       webbrowser.open(url)
       speak(f"Searching on google for {search_term}")

    elif 'open youtube' in query:
       webbrowser.open("https://www.youtube.com")
       speak("What would you like to search on YouTube?")
       search_term = takeCommand()
       url = f"https://www.youtube.com/results?search_query=%7B{search_term}%7D"
       webbrowser.open(url)
       speak(f"Searching YouTube for {search_term}")
       wk.playonyt(f"{search_term}")

    elif 'take screenshot' in query:
       speak("tell me a name for the file")
       name=takeCommand()
       time.sleep(3)
       img=pyautogui.screenshot()
       img.save(f'{name}.png')
       speak("screenshot saved")

    elif 'the time' in query:
       strTime = datetime.datetime.now().strftime("%H:%M:%S")
       speak(f"the time is {strTime}") 
    elif 'close window' in query: 
       pyautogui.hotkey('ctrl','shift','w')
       speak("Closed the window")
    elif 'shut down' in query:
       os.system("shutdown /s /t 5")
    elif 'restart the system' in query:
       os.system("shutdown /r /t 5")
    elif "volume up" in query:
       pyautogui.press("volumeup")
       pyautogui.press("volumeup")
    elif "volume down" in query:

       pyautogui.press("volumedown")
       pyautogui.press("volumedown")
    elif (('stop' in query) or ('close' in query) or ('bye' in query)):
       speak("thank you")
       break