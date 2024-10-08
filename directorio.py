import pywhatkit
import agenda
import os.path
import calendario

meses = {
    "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
    "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
    "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"
}



# Enviar mensaje de WhatsApp
def enviar_whatsapp(contacto: str, mensaje: str) -> str:
    """Envia un whatsapp"""
    b = contacto.split("+34")
    try:
        b[1] 
        if len(b[1]) == 9:  #combrobar los caracters
            #es un movil
            numero_sin = int(b[1][0]) 
            if numero_sin == 6 or numero_sin == 7: #combrueba si es un movil
                pywhatkit.sendwhatmsg_instantly(contacto, mensaje)
                return(f"mensaje enviado a {contacto}, mensaje: {mensaje} sin vbse")

    except IndexError:
        a = agenda.buscar_contactos(contacto)
        if a:
            nombre, numero = a
            pywhatkit.sendwhatmsg_instantly(numero, mensaje)
            return(f"mensaje enviado a {numero}, mensaje: {mensaje} con base")
        return("no se ha encontrado a la persona")

# Reproducir videos de YouTube
def buscar_google(busqueda:str="") -> str:
    pywhatkit.search(busqueda)
    return(f"buscando {busqueda} en google")
def reproducir_youtube(busqueda:str="") -> str:
    pywhatkit.playonyt(busqueda)
    return(f"Reproduciendo {busqueda} en YouTube")

def crear_nota(contenido: str="") -> str:

    if contenido:
        with open("nota.txt", "a") as archivo:  # Guardar en un archivo "nota.txt"
            archivo.write(contenido + "\n")
        return("He guardado la nota.")
def leer_nota() -> str:
    if os.path.exists("nota.txt"):
        with open("nota.txt", "r") as archivo:
            contenido = archivo.read()
        return(f"Estas son tus notas: {contenido}")
        
    else:
        return("No tienes ninguna nota guardada.")

def crear_contacto(nom: str="", numero: str="", email: str="") -> None:
    num = numero.replace("más", "+")
    num = numero.replace(" ", "")

    return (agenda.agregar_contacto(nom, num, email))
def borrar_contacto(nombre: str):
    return agenda.borrar_contacto(nombre)


def mostrar_calendario() -> str:
    return("buscando en el calendario", calendario.listar_eventos())
def crear_calendario(nombre: str="", fecha: str="", hora:str="") -> str:
    
    try:
        print(fecha)
        partes = fecha.split()
        dia = partes[0]
        mes = meses[partes[1]]
        año = partes[2]

        print(partes)
        fecha_format = f"{año}-{mes}-{dia.zfill(2)}"
        print(fecha_format)
    except ValueError:
        return("error en la fecha")
        return
    print(nombre, fecha, hora, fecha_format)
    a = calendario.agregar_evento(nombre, fecha_format, hora)
    if not a:
        return("ha ocurrido un error")
    else:
        return(a)