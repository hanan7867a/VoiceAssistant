import speech_recognition as sr
import webbrowser
import pyttsx3
import pyautogui
import time

engine = pyttsx3.init()

def speak(text):
    print("🤖:", text)
    engine.say(text)
    engine.runAndWait()

def listen(prompt="Listening..."):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak(prompt)
        print("🎤 Listening...")
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio)
        print(f"🗣️ You said: {query}")
        return query.lower()
    except:
        speak("Sorry, I didn’t get that.")
        return None

def google_search_mode():
    query = listen("What do you want to search on Google?")
    if not query:
        return
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    speak(f"Searching Google for {query}")
    time.sleep(5)  # Give browser time to load
    control_browser()

def control_browser():
    speak("You can now say scroll, click, next page, or go back.")
    while True:
        command = listen("Waiting for your browser command...")
        if not command:
            continue

        # Scroll Commands
        if "scroll down" in command:
            pyautogui.scroll(-1000)
            speak("Scrolling down.")
        elif "scroll up" in command:
            pyautogui.scroll(1000)
            speak("Scrolling up.")

        # Click Commands (approximate Y positions)
        elif "click first" in command:
            pyautogui.moveTo(500, 300)
            pyautogui.click()
            speak("Opening first link.")
            time.sleep(5)
        elif "click second" in command:
            pyautogui.moveTo(500, 400)
            pyautogui.click()
            speak("Opening second link.")
            time.sleep(5)
        elif "click third" in command:
            pyautogui.moveTo(500, 500)
            pyautogui.click()
            speak("Opening third link.")
            time.sleep(5)

        # Navigation Commands
        elif "go back" in command or "back" in command:
            pyautogui.hotkey('alt', 'left')
            speak("Going back.")
            time.sleep(3)
        elif "next page" in command or "next" in command:
            pyautogui.press('tab', presses=10)
            pyautogui.press('enter')
            speak("Opening next page.")
            time.sleep(3)
        elif "exit" in command or "stop" in command:
            speak("Okay, stopping.")
            break
        else:
            speak("Sorry, I didn't understand that command.")
