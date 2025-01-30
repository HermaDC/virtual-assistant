import costume_lib.agenda as agenda
import costume_lib.calendario as calendario
import os.path
import pywhatkit
import requests

meses = {
    "enero": "01", "febrero": "02", "marzo": "03", "abril": "04", "mayo": "05", "junio": "06",
    "julio": "07", "agosto": "08","septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"
}
WEATHER_DICT = {
        0: "Soleado",
        1: "Mayormente despejado",
        2: "Parcialmente nublado",
        3: "Nublado",
        45: "Neblina ligera",
        48: "Neblina densa",
        51: "Lluvia ligera",
        61: "Lluvia moderada",
        71: "Nieve ligera",
        80: "Chubascos ligeros",
        95: "Tormenta",
        96: "Tormenta severa"
    }

# Enviar mensaje de WhatsApp
def send_whatsapp_message(contact: str, mensage: str) -> str:
    """Envia un whatsapp"""
    b = contact.split("+34")
    try:
        b[1] 
        if len(b[1]) == 9:  #combrobar los caracters
            #es un movil
            numero_sin = int(b[1][0]) 
            if numero_sin == 6 or numero_sin == 7: #combrueba si es un movil
                pywhatkit.sendwhatmsg_instantly(contact, mensage)
                return(f"mensaje enviado a {contact}, mensaje: {mensage} sin contacto")

    except IndexError:
        a = agenda.buscar_contactos(contact)
        if a:
            nombre, numero = a
            pywhatkit.sendwhatmsg_instantly(numero, mensage)
            return(f"mensaje enviado a {numero}, mensaje: {mensage} con contacto")
        return("no se ha encontrado a la persona")

# Reproducir videos de YouTube
def search_google(search:str="") -> str:
    pywhatkit.search(search)
    return(f"buscando {search} en google")
def play_youtube(search:str="") -> str:
    pywhatkit.playonyt(search)
    return(f"Reproduciendo {search} en YouTube")
def check_weather():
    try:
        response = requests.get("ipinfo.io/json")
        response.raise_for_status()
        data = response.json()
        ciudad = data.get("city", "Desconocida")
        region = data.get("region", "Desconocida")
        pais = data.get("country", "Desconocido")
        coordenadas = data.get("loc", "0,0").split(",")
        latitud, longitud = map(float, coordenadas)

        print(f"Ubicación detectada: {ciudad}, {region}, {pais}")
        print(f"Coordenadas: Latitud {latitud}, Longitud {longitud}")
    except requests.RequestException as e:
        print("Error al obtener la ubicación:", e)
        return None, None
   
    if latitud and longitud:
        try:
            response = requests.get("https://api.open-meteo.com/v1/forecast", 
                                    params={"latitude": latitud, "longitude": longitud,"current_weather": True})
            response.raise_for_status()
            data = response.json()
            current_weather = data.get("current_weather", {})
            temperature = current_weather.get("temperature", "No disponible")
            weather_code = current_weather.get("weathercode", -1)

            return WEATHER_DICT.get(weather_code, "Condición desconocida"), temperature, ciudad
        except requests.RequestException as e:
            return("Error al consultar el clima:", e)


def create_note(content: str="") -> str:
    if content:
        with open("nota.txt", "a") as archivo:  # Guardar en un archivo "nota.txt"
            archivo.write(content + "\n")
        return("He guardado la nota.")
def read_notes() -> str:
    if os.path.exists("nota.txt"):
        with open("nota.txt", "r") as archivo:
            contenido = archivo.read()
        return(f"Estas son tus notas: {contenido}")
        
    else:
        return("No tienes ninguna nota guardada.")

def create_contact(nom: str="", number: str="", mail: str="") -> None:
    num = number.replace("más", "+").replace(" ", "")
    email = mail.replace("arroba", "@").replace("punto", ".").replace(" ", "")

    return (agenda.add_contact(nom, num, email))
def delete_contact(name: str):
    return agenda.delete_contact(name)


def show_calendar() -> str:
    return("buscando en el calendario", calendario.show_event())
def create_calendar(name: str="", date: str="", hora:str="") -> str:
    
    try:
        print(date)
        partes = date.split()
        dia = partes[0]
        mes = meses[partes[1]]
        año = partes[2]

        print(partes)
        format_date = f"{año}-{mes}-{dia.zfill(2)}"
        print(format_date)
    except ValueError:
        return("error en la fecha")
    print(name, date, hora, format_date)
    a = calendario.add_events(name, format_date, hora)
    if not a:
        return("ha ocurrido un error")
    else:
        return(a)