import speech_recognition as sr
import pyttsx3
import pywhatkit
import time

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Contacts dictionary (Add more contacts as needed)
contacts = {
    "wahab": "here is your number",
    "alice": "+0987654321",
    "myself": "+9230000000",
    "tawab": "+9230000000"
}

def speak(text):
    """Convert text to speech"""
    print("🤖:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    """Recognize speech from the microphone"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print(f"🗣️ You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I could not understand. Please repeat.")
        return ""
    except sr.RequestError:
        speak("Could not connect to the internet. Please check your connection.")
        return ""

def get_recipient():
    """Keep asking for recipient until a valid contact is found"""
    while True:
        speak("Who do you want to message?")
        recipient_name = listen()
        
        for name in contacts:
            if name in recipient_name:
                return name  # Return the matched contact name
        
        speak("I could not find that contact. Please try again.")

def get_message():
    """Keep asking for message until a valid input is received"""
    while True:
        speak("What is your message?")
        message = listen()
        
        if message:
            return message  # Return the valid message
        
        speak("I did not hear a message. Please try again.")

def send_whatsapp_message():
    """Send a WhatsApp message using recognized speech"""
    speak("Hello! I can send a WhatsApp message for you.")
    
    recipient_name = get_recipient()
    message = get_message()
    
    speak(f"Sending message to {recipient_name}.")
    pywhatkit.sendwhatmsg_instantly(contacts[recipient_name], message)
    time.sleep(2)  # Wait to ensure the message is sent
    speak("Message sent successfully!")
