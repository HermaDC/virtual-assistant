import directory
import pyttsx3
import speech_recognition as sr
import time
import os

# Configure voice synthesis
engine = pyttsx3.init()

# Constants and initializer variables
months = {
    "january": "01", "february": "02", "march": "03", "april": "04",
    "may": "05", "june": "06", "july": "07", "august": "08",
    "september": "09", "october": "10", "november": "11", "december": "12"
}

"""Listening and speaking functions"""
def talk(text: str) -> None:
    """Speaks a given text"""
    if text:
        engine.say(text)
        engine.runAndWait()  # Ensures the message is completed before continuing

# Voice recognition configuration
def listen() -> str:
    """Listens and returns a string"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio, language="en-US")
            print(f"Command received: {command}")
            return command.lower()
        except sr.UnknownValueError:
            talk("Please repeat, I didn't understand that.")
            return None
        except sr.RequestError:
            talk("Error connecting to the voice recognition service.")
            return None

"""Execution functions
    These manage all operations"""
# Main function that executes actions after activation
def run_assistant() -> None:
    talk("I'm listening, how can I help you?")
    while True:
        command = listen()
        if command:
            if 'send a message' in command:
                talk("Who do you want to send the message to?")
                contact = listen()
                talk("What message do you want to send?")
                message = listen()
                talk(directory.send_whatsapp_message(contact, message))
            # Notes
            elif ('create' in command and 'note' in command) or "create a note" in command:
                talk("What do you want me to write in the note?")
                content = listen()
                talk(directory.create_note(content))
            elif ('read' in command and 'note' in command) or "read the notes" in command:
                talk(directory.read_notes())
            # Contacts
            elif ('create' in command and 'contact' in command) or "create a contact" in command:
                talk("Say the person's name.")
                name = listen()
                talk("Say the phone number with the country code.")
                number = listen()
                talk("Say the email address.")
                email = listen()
                talk(directory.create_contact(name, number, email))
            elif ('delete' in command and 'contact' in command) or "delete a contact" in command:
                talk("Which contact do you want to delete?")
                name = listen()
                directory.delete_contact(name)
            # Calendar
            elif ('read' in command and 'calendar' in command) or "read the calendar" in command:
                talk(directory.show_calendar())
            elif ('create' in command and 'calendar' in command) or "create an event" in command:
                talk("You are creating an event.")
                talk("Specify the name of the event.")
                name = listen()
                talk("State the event date.")
                date = listen()
                talk("State the event time.")
                time = listen()
                talk(directory.create_calendar(name, date, time))
            # Internet and YouTube
            elif 'youtube' in command or 'video' in command:
                talk("What video would you like to watch on YouTube?")
                search = listen()
                talk(directory.play_youtube(search))
            elif ('search' in command and 'google') or 'search' in command:
                talk("What would you like to search for on Google?")
                search = listen()
                talk(directory.search_google(search))
            # Other functions
            elif "open" in command:
                talk("Which application should I open?")
                instruction = listen()
                print(instruction)
                os.system(instruction) if instruction else None
            elif 'thanks' in command:
                talk("Switching to standby mode.")
                activate_assistant()
                break
            elif 'goodbye' in command or 'exit' in command:
                talk("Goodbye, see you soon!")
                raise SystemExit
            else:
                print("I don't understand that command. Can you repeat it?")
        time.sleep(1)

# Function to activate the assistant when "Hey Barpsy" is said
def activate_assistant() -> None:
    r = sr.Recognizer()
    mic = sr.Microphone()

    print("Ready...")
    talk("Assistant ready. Say 'Hey Barpsy' to activate it.")

    while True:
        with mic as source:
            print("Listening for the keyword...")
            audio = r.listen(source)
            try:
                command = r.recognize_google(audio, language="en-US").lower()
                print(f"Keyword detected: {command}")
                if 'hey barpsy' in command:
                    talk("Hello, Barpsy activated.")
                    run_assistant()  # Calls the main function
                    break
                elif 'exit' in command or 'close' in command:
                    raise SystemExit
                else:
                    print("Keyword not detected.")
            except sr.UnknownValueError:
                print("I didn't understand the command.")
            except sr.RequestError:
                talk("Error connecting to the voice recognition service.")

            time.sleep(1)

if __name__ == "__main__":
    activate_assistant()
