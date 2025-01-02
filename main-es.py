import time
import os
import threading
import sys

from PIL import Image
from pystray import Icon, Menu, MenuItem
import costume_lib.directory as directory
import pyttsx3
import speech_recognition as sr


# Configurar síntesis de voz
engine = pyttsx3.init()

# Determinar la base del directorio dependiendo del entorno
if getattr(sys, 'frozen', False):  # Si está empaquetado con cx_Freeze
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construir la ruta al icono
icon_path = os.path.join(BASE_DIR, "Icons", "microphone_64x64.png")

# Verificar si el archivo existe
if not os.path.exists(icon_path):
    print(f"Error: El archivo no existe en {icon_path}")

# Constantes y variables inicializadoras
meses = {
    "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
    "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
    "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"
}

def exit(icon, item):
    """Cierra la aplicación."""
    print("Exiting...")
    icon.stop()
    time.sleep(0.25)
    os._exit(0)

def setup_tray_icon():
    global tray_icon
    tray_icon = Icon("Barpsy Assistant", image, menu=Menu(MenuItem("Exit", exit)))
    tray_icon.run()

""""Funciones de escucha y habla"""
def talk(texto:str) -> None:
    """Habla un texto"""
    if texto:
        engine.say(texto)
        engine.runAndWait()  # Asegura que el mensaje se complete antes de continuar

# Configuración de reconocimiento de voz
def listen() -> str:
    """Escucha y devuelve un string"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        audio = r.listen(source)
        try:
            comando = r.recognize_google(audio, language="es-ES")
            print(f"Comando recibido: {comando}")
            return comando.lower()
        except sr.UnknownValueError:
            talk("Repite, no entendí eso.")
            return None
        except sr.RequestError:
            talk("Error al conectar con el servicio de reconocimiento de voz.")
            return None

""""Funciones de ejecución"""
# Función principal que ejecuta las acciones después de la activación
def run_assistant() -> None:
    talk("Estoy escuchando, ¿en qué puedo ayudarte?")
    while True:
        comand = listen()
        if comand:
            # Lógica para procesar comandos
            pass  # Resto de tus funciones

# Función para activar el asistente al decir "Hey Barpsy"
def activar_asistente() -> None:
    r = sr.Recognizer()
    mic = sr.Microphone()

    print("listo...")
    talk("Asistente listo. Di 'Hey Barpsy' para activarlo.")

    while True:
        with mic as source:
            print("Escuchando palabra clave...")
            audio = r.listen(source)
            try:
                comand = r.recognize_google(audio, language="es-ES").lower()
                print(f"Comando detectado: {comand}")
                if 'hey barsi' in comand:
                    talk("Hola, Barpsy activado.")
                    run_assistant()  # Llama a la función principal
                    break
                elif 'salir' in comand or 'cerrar' in comand:
                    raise SystemExit
                else:
                    print("No se detectó la palabra clave.")
            except sr.UnknownValueError:
                print("No entendí el comando.")
            except sr.RequestError:
                talk("Error al conectar con el servicio de reconocimiento de voz.")

            time.sleep(1)

if __name__ == "__main__":
    # Cargar la imagen usando una ruta relativa
    icon_path = os.path.join(BASE_DIR, "Icons", "microphone_64x64.png")
    image = Image.open(icon_path)
    tray_thread = threading.Thread(target=setup_tray_icon, daemon=True)
    tray_thread.start()
    activar_asistente()
