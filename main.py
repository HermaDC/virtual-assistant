import json
import os
import sys
import time
from typing import Any
import threading

import gettext
import PIL
from pystray import Icon, Menu, MenuItem
import costume_lib.directory as directory
import pyttsx3
import speech_recognition as sr
from tkinter import Label, Entry, ttk, Button, Tk, StringVar
from tkinter.ttk import Combobox

#TODO add multi lenguage babel

# Configure voice synthesis
engine = pyttsx3.init()
DEFAULT_LANGUAGE = "En-US"

# Determinar la base del directorio dependiendo del entorno
if getattr(sys, 'frozen', False):  # Si está empaquetado con cx_Freeze
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "r") as f:
        try:
            existing_config = json.load(f)
            lang = existing_config.get("language", DEFAULT_LANGUAGE).lower()
        except json.JSONDecodeError:
            lang = DEFAULT_LANGUAGE
else:
    lang = DEFAULT_LANGUAGE

# NUEVO: preparar gettext con idioma correcto
locales_dir = os.path.join(BASE_DIR, "locales")
translation = gettext.translation('messages', localedir=locales_dir, languages=[lang], fallback=True)
translation.install()
_ = translation.gettext

# Constants and initializer variables
months = {
    "january": "01", "february": "02", "march": "03", "april": "04",
    "may": "05", "june": "06", "july": "07", "august": "08",
    "september": "09", "october": "10", "november": "11", "december": "12"
}
def save_config(key: tuple, value: tuple):
    global WEATHER_KEY, LANGUAGE
    with open(os.path.join(BASE_DIR, "config.json"), "w") as f:
        config = {i: x for i, x in zip(key, value)}
        json.dump(config, f)
    WEATHER_KEY = config.get("weather-key", None)
    LANGUAGE = config.get("language", "En-US")

def set_language(lang_code: str):
    global _, translation, LANGUAGE
    LANGUAGE = lang_code
    translation = gettext.translation('messages', localedir=locales_dir, languages=[lang_code], fallback=True)
    translation.install()
    _ = translation.gettext

def load_config():
    """load the configuration from the config.json file if exists, 
    else creates a welcome window to set the configuration"""
    global WEATHER_KEY, LANGUAGE
    if os.path.exists(os.path.join(BASE_DIR, "config.json")):
        config = json.load(open(os.path.join(BASE_DIR, "config.json")))
        WEATHER_KEY = config.get("weather-key", None)  # Fixed typo here
        LANGUAGE = config.get("language", "en")
    else:
        root = Tk()
        root.title("Initial configuration")

        # Título de la ventana
        Label(root, text="Welcome to the App", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)

        # Selector de idioma
        Label(root, text="Select the language:").grid(row=1, column=0, padx=10, pady=5)
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
            idioma = "En-US" if idioma == "English" else "Es-ES"

        # Botón para guardar la configuración
        guardar_btn = Button(root, text="Save configuration",
                              command=lambda:[save_config(("weather-key", "language"), (api_entry.get(), idioma) ), set_language(idioma), root.destroy()])
        guardar_btn.grid(row=3, column=0, columnspan=2, pady=20)

        # Ejecutar la ventana
        root.mainloop()

def config(icon, item):
    root = Tk()
    root.title("Initial configuration")

    # Título de la ventana
    Label(root, text="Welcome to the App", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)

    # Selector de idioma
    Label(root, text="Select the language:").grid(row=1, column=0, padx=10, pady=5)
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
        idioma = "En-US" if idioma == "English" else "Es-ES"

    # Botón para guardar la configuración
    guardar_btn = Button(root, text="Save configuration",
                          command=lambda:[save_config(("weather-key", "language"), (api_entry.get(), idioma) ),
                                          set_language(idioma), root.destroy()])
    guardar_btn.grid(row=3, column=0, columnspan=2, pady=20)

    # Ejecutar la ventana
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
def talk(text: Any) -> None:
    """Speaks a given text"""
    if text:
        translated = _(text)
        engine.say(translated)
        engine.runAndWait()  # Ensures the message is completed before continuing

# Voice recognition configuration
def listen() -> str | None:
    """Listens and returns a string"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio, language=LANGUAGE)
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
    talk(_("I'm listening, how can I help you?"))

    commands = {
        "send_message": _("send a message"),
        "create_note": _("create a note"),
        "read_notes": _("read the notes"),
        "create_contact": _("create a contact"),
        "delete_contact": _("delete a contact"),
        "read_calendar": _("read the calendar"),
        "create_event": _("create an event"),
        "youtube": _("youtube"),
        "video": _("video"),
        "search": _("search"),
        "search_google": _("search google"),
        "weather": _("weather"),
        "weather_alt": _("tell me the weather"),
        "open": _("open"),
        "thanks": _("thanks"),
        "goodbye": _("goodbye"),
        "exit": _("exit")
    }

    while True:
        command = listen()
        if command:
            if commands["send_message"] in command:
                talk(_("Who do you want to send the message to?"))
                contact = listen()
                talk(_("What message do you want to send?"))
                message = listen()
                if contact and message:
                    talk(directory.send_whatsapp_message(contact, message))

            elif commands["create_note"] in command:
                talk(_("What do you want me to write in the note?"))
                content = listen()
                if content:
                    talk(directory.create_note(content))

            elif commands["read_notes"] in command:
                talk(directory.read_notes())

            elif commands["create_contact"] in command:
                talk(_("Say the person's name."))
                name = listen()
                talk(_("Say the phone number with the country code."))
                number = listen()
                talk(_("Say the email address."))
                email = listen()
                if name and number and email:
                    talk(directory.create_contact(name, number, email))

            elif commands["delete_contact"] in command:
                talk(_("Which contact do you want to delete?"))
                name = listen()
                if name:
                    directory.delete_contact(name)

            elif commands["read_calendar"] in command:
                talk(directory.show_calendar())

            elif commands["create_event"] in command:
                talk(_("You are creating an event."))
                talk(_("Specify the name of the event."))
                name = listen()
                talk(_("State the event date."))
                date = listen()
                talk(_("State the event time."))
                hour = listen()
                if name and date and hour:
                    talk(directory.create_calendar(name, date, hour))

            elif commands["youtube"] in command or commands["video"] in command:
                talk(_("What video would you like to watch on YouTube?"))
                search = listen()
                if search:
                    talk(directory.play_youtube(search))

            elif commands["search"] in command or commands["search_google"] in command:
                talk(_("What would you like to search for on Google?"))
                search = listen()
                if search:
                    talk(directory.search_google(search))

            elif commands["weather"] in command or commands["weather_alt"] in command:
                talk(directory.check_weather())

            elif commands["open"] in command:
                talk(_("Which application should I open?"))
                instruction = listen()
                os.system(instruction) if instruction else None

            elif commands["thanks"] in command:
                talk(_("You're welcome. Switching to standby mode."))
                activate_assistant()
                break

            elif commands["goodbye"] in command or commands["exit"] in command:
                talk(_("Goodbye, see you soon!"))
                raise SystemExit

            else:
                print(_("I don't understand that command. Can you repeat it?"))

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
                command = r.recognize_google(audio, language=LANGUAGE).strip().lower()  # Normalize input
                print(f"Keyword detected: {command}")
                if 'hey barsi' in command:
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