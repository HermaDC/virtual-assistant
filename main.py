import directorio
import pyttsx3
import speech_recognition as sr
import time
import os

# Configurar síntesis de voz
engine = pyttsx3.init()

#constantes y varibles inicializadoras
meses = {
    "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
    "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
    "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"
}

""""funciones de escucha y habla"""
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

""""funciones ejecucion
    son las que se encargan de gestionar todo"""
# Función principal que ejecuta las acciones después de la activación
def run_assistant() -> None:
    talk("Estoy escuchando, ¿en qué puedo ayudarte?")
    while True:
        comand = listen()
        if comand:
                    if 'Manda un mensaje' in comand:
                        talk("¿A quién le quieres enviar el mensaje?")
                        contact = listen()
                        talk("¿Qué mensaje le quieres enviar?")
                        mensage = listen()
                        talk(directorio.send_whatsapp_message(contact, mensage))
                    #notas
                    elif ('crear' in comand and 'nota' in comand) or "crea una nota" in comand:
                        talk("¿Qué quieres que escriba en la nota?")
                        content = listen()
                        talk(directorio.create_note(content))
                    elif ('leer' in comand and 'nota' in comand) or "lee las notas" in comand:
                        talk(directorio.read_notes())
                    #agenda
                    elif ('crear' in comand and 'contacto' in comand) or "crea un contacto" in comand:
                        talk("Diga nombre de la persona")
                        nom = listen()
                        talk("Diga numero de telefono con prefijo")
                        name = listen()
                        talk("diga email")
                        email = listen()
                        talk(directorio.create_contact(nom, name, email))
                    elif ('borrar' in comand and 'contacto' in comand) or "borra un contacto" in comand:
                        talk("¿Que contacto quieres borrar?")
                        name = listen()
                        directorio.delete_contact(name)
                    #calendario
                    elif ('leer' in comand and 'calendario' in comand) or "lee el calendario" in comand:
                        talk(directorio.show_calendar())
                    elif ('crear' in comand and 'calendario' in comand) or "crea un evento" in comand:  
                        talk("estás creando un evento")
                        talk("Indica nombre del evento.")
                        name = listen()
                        talk("Di fecha del evento.")
                        date = listen()
                        talk("Di hora del evento.")
                        hour = listen()
                        talk(directorio.create_calendar(name, date, hour))
                    # Internet y youtube  
                    elif 'youtube' in comand or 'video' in comand:
                        talk("¿Qué video te gustaría ver en YouTube?")
                        search = listen()
                        talk(directorio.play_youtube(search))
                    elif ('buscar' in comand and 'google') or 'busca' in comand:
                        talk("¿Qué te gustaría buscar en Google?")
                        search = listen()
                        talk(directorio.search_google(search))
                    # Otras funciones
                    elif "abre" in comand:
                        talk("¿qué aplicación abro?")
                        instrucc = listen()
                        print(instrucc)
                        os.system(instrucc) if instrucc else None
                    elif 'gracias' in comand:
                        talk("pasando a modo segundo plano")
                        activar_asistente()
                        break
                    elif 'adiós' in comand or 'salir' in comand:
                        talk("Hasta luego, ¡nos vemos pronto!")
                        raise SystemExit
                    else:
                        print("No entiendo ese comando. ¿Puedes repetirlo?")
        time.sleep(1)

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
    activar_asistente()