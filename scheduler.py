import schedule
import time  
import datetime  
import json
import pyttsx3
import speech_recognition as sr
import threading

MEETING_FILE = "meetings.json"

# Load saved meetings
try:
    with open(MEETING_FILE, "r") as file:
        raw_meetings = json.load(file)
        meetings = {
            datetime.datetime.strptime(k, "%Y-%m-%d %H:%M"): v 
            for k, v in raw_meetings.items()
        }
except (FileNotFoundError, json.JSONDecodeError):
    meetings = {}

# Remove past meetings
meetings = {k: v for k, v in meetings.items() if k >= datetime.datetime.now()}

# Function to save meetings
def save_meetings():
    try:
        with open(MEETING_FILE, "w") as file:
            json.dump({k.strftime("%Y-%m-%d %H:%M"): v for k, v in meetings.items()}, file)
    except Exception as e:
        print(f"Error saving meetings: {e}")

# Text-to-Speech
def speak(text):
    local_engine = pyttsx3.init()
    local_engine.setProperty('rate', 150)
    local_engine.say(text)
    local_engine.runAndWait()
    local_engine.stop()

# Speech Recognition
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening, please speak.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        return recognizer.recognize_google(audio).lower()
    except:
        return None

# Convert 12hr to 24hr
def convert_to_24_hour(time_str):
    try:
        time_str = time_str.lower().replace(".", "").replace("a m", "AM").replace("p m", "PM").replace("a.m", "AM").replace("p.m", "PM")
        time_str = " ".join(time_str.split())
        if " " in time_str:
            parts = time_str.split(" ")
            if len(parts) == 2 and ":" not in parts[0]:  
                time_str = parts[0].replace(" ", ":") + " " + parts[1]
        time_obj = datetime.datetime.strptime(time_str, "%I:%M %p")
        return time_obj.strftime("%H:%M")
    except ValueError:
        return None  

# Date input
def get_valid_date():
    while True:
        speak("Please say the meeting date as day and month, for example, eighteen February.")
        date_input = recognize_speech()
        if not date_input:
            continue
        try:
            day, month_str = date_input.split()
            day = int(day)
            current_year = datetime.datetime.now().year
            month = datetime.datetime.strptime(month_str, "%B").month
            meeting_date = datetime.date(current_year, month, day)
            if meeting_date < datetime.date.today():
                speak("You cannot schedule a meeting in the past.")
                continue
            return meeting_date
        except ValueError:
            speak("Invalid date. Please try again.")

# Time input
def get_valid_time():
    while True:
        speak("Now, say the time in twelve-hour format, for example, four fifteen PM.")
        time_input = recognize_speech()
        if not time_input:
            continue
        time_24 = convert_to_24_hour(time_input)
        if time_24:
            return time_24
        speak("Invalid time format. Please try again.")

# Add meeting
def add_meeting():
    meeting_date = get_valid_date()
    meeting_time = get_valid_time()
    while True:
        speak("Who is the meeting with?")
        person = recognize_speech()
        if not person:
            speak("Please say the name again.")
            continue  
        speak(f"You said {person}. Say yes to confirm.")
        confirmation = recognize_speech()
        if confirmation and "yes" in confirmation:
            break
    try:
        meeting_datetime = datetime.datetime.combine(
            meeting_date, datetime.datetime.strptime(meeting_time, "%H:%M").time()
        )
        meetings[meeting_datetime] = person
        save_meetings()
        speak(f"Meeting with {person} scheduled on {meeting_datetime.strftime('%d %B %Y at %I:%M %p')}")
    except ValueError:
        speak("Error scheduling the meeting.")

# Meeting reminder
def reminder(meeting_time):
    person = meetings[meeting_time]
    reminder_message = f"You have a meeting with {person} now."
    speak(reminder_message)

# Meeting checker
def check_meetings():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    for meeting_time in list(meetings.keys()):
        if now == meeting_time.strftime("%Y-%m-%d %H:%M"):
            reminder(meeting_time)

# Background scheduler
def run_scheduler():
    schedule.every(1).minutes.do(check_meetings)
    while True:
        schedule.run_pending()
        time.sleep(10)

# Only run loop if this file is the main one
if __name__ == "__main__":
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    while True:
        speak("Say 'schedule meeting' to set a new meeting, or 'exit' to stop.")
        command = recognize_speech()
        if command:
            if "schedule meeting" in command or "meeting" in command:
                add_meeting()
            elif "exit" in command:
                speak("Goodbye!")
                break
