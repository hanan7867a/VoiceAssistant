import threading
import time
import pyttsx3
import speech_recognition as sr
from web_search import google_search_mode, control_browser
from whatsapp_bot import send_whatsapp_message
from scheduler import add_meeting, check_meetings, meetings

# Initialize the Text-to-Speech Engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech"""
    print(f"🤖: {text}")
    engine.say(text)
    engine.runAndWait()

def listen(prompt="Listening..."):
    """Recognize speech from the microphone"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(prompt)
        speak(prompt)
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio)
        print(f"🗣️ You said: {query}")
        return query.lower()
    except:
        speak("Sorry, I didn't catch that.")
        return None

# Threading function to run the scheduler in the background
def schedule_thread():
    while True:
        check_meetings()
        time.sleep(60)  # Check meetings every minute

# Function to handle the main assistant loop
def main_assistant_loop():
    speak("Hello, I am your voice assistant. How can I help you today?")
    while True:
        command = listen("What would you like to do? Say 'search', 'whatsapp', or 'schedule'.")
        if not command:
            continue

        # Web search functionality
        if "search" in command:
            google_search_mode()

        # WhatsApp bot functionality
        elif "whatsapp" in command:
            send_whatsapp_message()

        # Scheduling functionality
        elif "schedule" in command or "meeting" in command:
            add_meeting()

        # Check schedule functionality
        elif "check schedule" in command:
            if not meetings:
                speak("No upcoming meetings.")
            else:
                speak("Here are your upcoming meetings:")
                for meeting_time, person in sorted(meetings.items()):
                    formatted_time = meeting_time.strftime('%d %B at %I:%M %p')
                    speak(f"Meeting with {person} on {formatted_time}")

        elif "exit" in command or "stop" in command:
            speak("Goodbye!")
            break

# Start the background scheduler thread
scheduler_thread = threading.Thread(target=schedule_thread, daemon=True)
scheduler_thread.start()

# Start the main assistant loop
if __name__ == "__main__":
    main_assistant_loop()
