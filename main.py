import calendario
import os.path
import pyttsx3
import pywhatkit
import speech_recognition as sr
import time
import agenda

# Configurar síntesis de voz
engine = pyttsx3.init()

#constantes y varibles inicializadoras

meses = {
    "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
    "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
    "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"
}

""""funciones de escucha y habla"""
def hablar(texto):
    engine.say(texto)
    engine.runAndWait()  # Asegura que el mensaje se complete antes de continuar

# Configuración de reconocimiento de voz
def escuchar():
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
def enviar_whatsapp(contacto, mensaje):
   
      
    b = contacto.split("+34")
    try:
        b[1] 
        if len(b[1]) == 9:  #combrobar los caracters
            print("es un telefono") 
            numero_sin = int(b[1][0]) 
            if numero_sin == 6 or numero_sin == 7: #combrueba si es un movil
                print("es un movil")
                pywhatkit.sendwhatmsg_instantly(contacto, mensaje)
                hablar(f"mensaje enviado a {contacto}, mensaje: {mensaje} sin vbse")

    except IndexError:
        a = agenda.buscar_contactos(contacto)
        if a:
            nombre, numero = a
            pywhatkit.sendwhatmsg_instantly(numero, mensaje)
            hablar(f"mensaje enviado a {numero}, mensaje: {mensaje} con base")
        hablar("no se ha encontrado a la persona")

def crear_contacto():
    hablar("Diga nombre de la persona")
    nom = escuchar()
    hablar("Diga numero de telefono con prefijo")
    numero = escuchar()
    hablar("diga email")
    email = escuchar()
    num = numero.replace("más", "+")
    num = numero.replace(" ", "")
    
    print(num)
    b = num.split("+34")
    try:
        b[1] 
        if len(b[1]) == 9:  #combrobar los caracters
            print("es un telefono") 
            numero_sin = int(b[1][0]) 
            if numero_sin == 6 or numero_sin == 7: #combrueba si es un movil
                print("es un movil")
                agenda.agregar_contacto(nom, num, email)

    except IndexError:
        hablar("No se ha indicado prefijo")

# Reproducir videos de YouTube
def reproducir_youtube(busqueda):
    pywhatkit.playonyt(busqueda)
    hablar(f"Reproduciendo {busqueda} en YouTube")

def buscar_google(busqueda):
    pywhatkit.search(busqueda)
    hablar(f"buscando {busqueda} en google")


""""funcinones relacionadas con cosas de recordatorios"""

def crear_nota():
    hablar("¿Qué quieres que escriba en la nota?")
    contenido = escuchar()
    
    if contenido:
        with open("nota.txt", "a") as archivo:  # Guardar en un archivo "nota.txt"
            archivo.write(contenido + "\n")
        hablar("He guardado la nota.")

def leer_nota():
    if os.path.exists("nota.txt"):
        with open("nota.txt", "r") as archivo:
            contenido = archivo.read()
        hablar("Estas son tus notas:")
        hablar(contenido)
    else:
        hablar("No tienes ninguna nota guardada.")

def mostrar_calendario():
    hablar("buscando en el calendario")
    hablar(calendario.listar_eventos())

def crear_calendario():
    hablar("estás creando un evento")
    hablar("Indica nombre del evento.")
    nombre = escuchar()
    hablar("Di fecha del evento.")
    fecha = escuchar()
    hablar("Di hora del evento.")
    hora = escuchar()
    try:
        partes = fecha.split()
        dia = partes[0]
        mes = meses[partes[2]]
        año = partes[4]

        fecha_format = f"{año}-{mes}-{dia.zfill(2)}"
    except:
        hablar("error en la fecha")
        return
    print(nombre, fecha, hora, fecha_format)
    a = calendario.agregar_evento(nombre, fecha_format, hora)
    if not a:
        hablar("ha ocurrido un error")
        return
    else:
        hablar(a)
    


""""funciones ejecucion
    son las que se encargan de gestionar todo"""
# Función principal que ejecuta las acciones después de la activación
def ejecutar_asistente():
    hablar("Estoy escuchando, ¿en qué puedo ayudarte?")
    
    while True:
        comando = escuchar()
        
        if comando:
            if 'mensaje' in comando:
                hablar("¿A quién le quieres enviar el mensaje?")
                contacto = escuchar()
                hablar("¿Qué mensaje le quieres enviar?")
                mensaje = escuchar()
                enviar_whatsapp(contacto, mensaje)
                print(mensaje)
                
            elif 'youtube' in comando or 'video' in comando:
                hablar("¿Qué video te gustaría ver en YouTube?")
                busqueda = escuchar()
                reproducir_youtube(busqueda)
                print(busqueda)
            
            elif 'buscar' in comando or 'busca' in comando:
                hablar("¿Qué te gustaría buscar en Google?")
                busqueda = escuchar()
                buscar_google(busqueda)
            
            elif 'nota' in comando and 'crear' in comando:
                crear_nota()
            
            elif 'nota' in comando and 'leer' in comando:
                leer_nota()
            
            elif 'crear' in comando and 'contacto' in comando:
                crear_contacto()

            elif 'calendario' in comando and 'leer' in comando:
                mostrar_calendario()
            
            elif 'calendario' in comando and 'crear' in comando:    
                crear_calendario()

            elif 'gracias' in comando:
                hablar("pasando a modo segundo plano")
                activar_asistente()
                break

            elif 'adiós' in comando or 'salir' in comando:
                hablar("Hasta luego, ¡nos vemos pronto!")
                raise SystemExit
                
            else:
                hablar("No entiendo ese comando. ¿Puedes repetirlo?")
        time.sleep(1)

# Función para activar el asistente al decir "Hey Barpsy"
def activar_asistente():
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
