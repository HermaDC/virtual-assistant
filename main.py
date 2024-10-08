import pyttsx3
import speech_recognition as sr
import time
import directorio


# Configurar síntesis de voz
engine = pyttsx3.init()

#constantes y varibles inicializadoras
meses = {
    "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
    "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
    "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"
}


""""funciones de escucha y habla"""
def hablar(texto:str) -> None:
    """Habla un texto"""
    if texto:
        engine.say(texto)
        engine.runAndWait()  # Asegura que el mensaje se complete antes de continuar

# Configuración de reconocimiento de voz
def escuchar() -> str:
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
            hablar("Repite, no entendí eso.")
            return None
        except sr.RequestError:
            hablar("Error al conectar con el servicio de reconocimiento de voz.")
            return None


# Enviar mensaje de WhatsApp


""""funciones ejecucion
    son las que se encargan de gestionar todo"""
# Función principal que ejecuta las acciones después de la activación
def ejecutar_asistente() -> None:
    hablar("Estoy escuchando, ¿en qué puedo ayudarte?")
    
    while True:
        comando = escuchar()
        
        
        if comando:
                    if 'mensaje' in comando:
                        hablar("¿A quién le quieres enviar el mensaje?")
                        contacto = escuchar()
                        hablar("¿Qué mensaje le quieres enviar?")
                        mensaje = escuchar()
                        hablar(directorio.enviar_whatsapp(contacto, mensaje))

                    #notas
                    elif 'crear' in comando and 'nota' in comando:
                        hablar("¿Qué quieres que escriba en la nota?")
                        contenido = escuchar()
                        hablar(directorio.crear_nota(contenido))
                    elif 'leer' in comando and 'nota' in comando:
                        hablar(directorio.leer_nota())
                    #agenda
                    elif 'crear' in comando and 'contacto' in comando:
                        hablar("Diga nombre de la persona")
                        nom = escuchar()
                        hablar("Diga numero de telefono con prefijo")
                        numero = escuchar()
                        hablar("diga email")
                        email = escuchar()
                        hablar(directorio.crear_contacto(nom, numero, email))
                    elif 'borrar' in comando and 'contacto' in comando:
                        hablar("¿Que contacto quieres borrar?")
                        nombre = escuchar()
                        directorio.borrar_contacto(nombre)
                    #calendario
                    elif 'leer' in comando and 'calendario' in comando:
                        hablar(directorio.mostrar_calendario())
                    elif 'crear' in comando and 'calendario' in comando:  
                        hablar("estás creando un evento")
                        hablar("Indica nombre del evento.")
                        nombre = escuchar()
                        hablar("Di fecha del evento.")
                        fecha = escuchar()
                        hablar("Di hora del evento.")
                        hora = escuchar()
                        hablar(directorio.crear_calendario(nombre, fecha, hora))
                    
                    # Internet y youtube  
                    elif 'youtube' in comando or 'video' in comando:
                        hablar("¿Qué video te gustaría ver en YouTube?")
                        busqueda = escuchar()
                        hablar(directorio.reproducir_youtube(busqueda))
                    elif 'buscar' in comando and 'google' or 'busca' in comando:
                        hablar("¿Qué te gustaría buscar en Google?")
                        busqueda = escuchar()
                        hablar(directorio.buscar_google(busqueda))
                    # Otras funciones
                    elif 'gracias' in comando:
                        hablar("pasando a modo segundo plano")
                        
                        break
                    elif 'adiós' in comando or 'salir' in comando:
                        hablar("Hasta luego, ¡nos vemos pronto!")
                        raise SystemExit
                    else:
                        print("No entiendo ese comando. ¿Puedes repetirlo?")
        time.sleep(1)

# Función para activar el asistente al decir "Hey Barpsy"
def activar_asistente() -> None:
    r = sr.Recognizer()
    mic = sr.Microphone()

    print("listo...")
    hablar("Asistente listo. Di 'Hey Barpsy' para activarlo.")

    while True:
        with mic as source:
            print("Escuchando palabra clave...")
            audio = r.listen(source)
            try:
                comando = r.recognize_google(audio, language="es-ES").lower()
                print(f"Comando detectado: {comando}")
                if 'hey barsi' in comando:
                    hablar("Hola, Barpsy activado.")
                    ejecutar_asistente()  # Llama a la función principal
                    break
                elif 'salir' in comando or 'cerrar' in comando:
                    raise SystemExit
                else:
                    print("No se detectó la palabra clave.")
            except sr.UnknownValueError:
                print("No entendí el comando.")
            except sr.RequestError:
                hablar("Error al conectar con el servicio de reconocimiento de voz.")

            time.sleep(1)

if __name__ == "__main__":
    activar_asistente()
