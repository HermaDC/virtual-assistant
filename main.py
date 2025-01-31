import json
import os
import sys
import time
import threading

import PIL
from pystray import Icon, Menu, MenuItem
import costume_lib.directory as directory
import pyttsx3
import speech_recognition as sr
from tkinter import Label, Entry, ttk, Button, Tk, StringVar
from tkinter.ttk import Combobox

# Configure voice synthesis
engine = pyttsx3.init()

# Determinar la base del directorio dependiendo del entorno
if getattr(sys, 'frozen', False):  # Si está empaquetado con cx_Freeze
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Constants and initializer variables
months = {
    "january": "01", "february": "02", "march": "03", "april": "04",
    "may": "05", "june": "06", "july": "07", "august": "08",
    "september": "09", "october": "10", "november": "11", "december": "12"
}
def save_config(key: tuple, value: tuple):
    global WEATHER_KEY, LENGUAGE
    with open(os.path.join(BASE_DIR, "config.json"), "w") as f:
        config = {i: x for i, x in zip(key, value)}
        json.dump(config, f)
    WEATHER_KEY = config.get("weather-key", None)
    LENGUAGE = config.get("language", "En-U")

def load_config():
    """load the configuration from the config.json file if exists, 
    else creates a welcome window to set the configuration"""
    if os.path.exists(os.path.join(BASE_DIR, "config.json")):
        config = json.load(open(os.path.join(BASE_DIR, "config.json")))
        WEATHER_KEY = config.get("weater-key", None)
    else:
        root = Tk()
        root.title("Initial configuration")

        # Título de la ventana
        Label(root, text="Welcome to the App", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        # Selector de idioma
        Label(root, text="Select the lenguage:").grid(row=1, column=0, padx=10, pady=5)
        idioma_var = StringVar(value="Español")  # Valor por defecto
        idiomas = ["Español", "English"]
        idioma_combo = Combobox(root, textvariable=idioma_var, values=idiomas)
        idioma_combo.grid(row=1, column=1, padx=10, pady=5)

        # Entrada para la clave de API
        Label(root, text="weather API key:").grid(row=2, column=0, padx=10, pady=5)
        api_entry = Entry(root, show="*", width=30)
        api_entry.grid(row=2, column=1, padx=10, pady=5)
        idioma = idioma_var.get()
        if idioma in idiomas:
            idioma = "En-us" if idioma == "English" else "Es-es"

        # Botón para guardar la configuración
        guardar_btn = Button(root, text="Save configuration",
                              command=lambda:[save_config(("weather-key", "language"), (api_entry.get(), idioma) ), root.destroy()])
        guardar_btn.grid(row=3, column=0, columnspan=2, pady=20)

        # Ejecutar la ventana
        root.mainloop()

def config(icon, item):
    root = Tk()
    root.title("Barpsy Assistant Configuration")
    root.geometry("400x200")
    weather_label = Label(root, text="Introduce the weather API key").grid(row=0, column=0) 

    weather_entry = Entry(root, textvariable="hola")
    weather_entry.grid(row=0, column=1)
    print(weather_entry)
    cancel_button = Button(root, text="Cnacel", bg="red", command=root.destroy).grid(row=1, column=0)
    submit_button = Button(root, text="Save", bg="green", 
                            command=lambda: [save_config("weather-key", weather_entry.get()), root.destroy]).grid(row=1, column=1)
    root.mainloop()

def exit(icon, item):
    """Close the app"""
    print("Exiting...")
    icon.stop()
    time.sleep(0.25)
    os._exit(0)

def setup_tray_icon():
    global tray_icon
    tray_icon = Icon("Barpsy Assistant", image, menu=Menu(MenuItem("Exit", exit), MenuItem("Config", config)))
    tray_icon.run()

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
            #weather
            elif 'weather' or 'tell me de weather' in command:
                talk(directory.check_weather())
            # Other functions
            elif "open" in command:
                talk("Which application should I open?")
                instruction = listen()
                print(instruction)
                os.system(instruction) if instruction else None
            elif 'thanks' in command:
                talk("yourwelcome. Switching to standby mode.")
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
    # Construir la ruta al icono
    icon_path = os.path.join(BASE_DIR, "Icons", "microphone_64x64.png")

# Verificar si el archivo existe
    if not os.path.exists(icon_path):
        raise FileNotFoundError(f"Icon file not found: {icon_path}")
    icon_path = os.path.join(BASE_DIR, "Icons", "microphone_64x64.png")
    image = PIL.Image.open(icon_path)
    load_config()
    tray_thread = threading.Thread(target=setup_tray_icon, daemon=True)
    tray_thread.start()
    activate_assistant()