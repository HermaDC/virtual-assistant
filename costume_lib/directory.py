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
    0: "Sunny",
    1: "Mostly clear",
    2: "Partly cloudy",
    3: "Cloudy",
    45: "Light fog",
    48: "Dense fog",
    51: "Light rain",
    61: "Moderate rain",
    71: "Light snow",
    80: "Light showers",
    95: "Thunderstorm",
    96: "Severe thunderstorm"
}

# Enviar mensaje de WhatsApp
def send_whatsapp_message(contact: str, mensage: str) -> str:
    """Send a WhatsApp message"""
    b = contact.split("+34")
    try:
        b[1] 
        if len(b[1]) == 9:  # Check the number of characters
            # It's a mobile number
            numero_sin = int(b[1][0]) 
            if numero_sin == 6 or numero_sin == 7:  # Check if it's a mobile number
                pywhatkit.sendwhatmsg_instantly(contact, mensage)
                return(f"Message sent to: {contact}, message: {mensage}")
            return "Not a mobile phone number"  # Already in messages.po
    except IndexError:
        a = agenda.buscar_contactos(contact)
        if a:
            nombre, numero = a
            pywhatkit.sendwhatmsg_instantly(numero, mensage)
            return(f"Message sent to: {numero}, message: {mensage}")
        return "Person not found"  # Already in messages.po
    # Ensure a string is always returned
    return "Invalid contact format"  # Already in messages.po

# Reproducir videos de YouTube
def search_google(search:str="") -> str:
    pywhatkit.search(search)
    return f"searching {search} in google"  # Already in messages.po
def play_youtube(search:str="") -> str:
    pywhatkit.playonyt(search)
    return f"Playing {search} in YouTube"  # Already in messages.po
def check_weather():
    try:
        response = requests.get("https://ipinfo.io/json")
        response.raise_for_status()
        data = response.json()
        city = data.get("city", "Unknown")
        region = data.get("region", "Unknown")
        country = data.get("country", "Unknown")
        coordinates = data.get("loc", "0,0").split(",")
        latitude, longitude = map(float, coordinates)

        print(f"Detected location: {city}, {region}, {country}")
        print(f"Coordinates: Latitude {latitude}, Longitude {longitude}")
    except requests.RequestException as e:
        return "Error while getting the location:", e

    if latitude and longitude:
        try:
            response = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={"latitude": latitude, "longitude": longitude, "current_weather": True}
            )
            response.raise_for_status()
            data = response.json()
            current_weather = data.get("current_weather", {})
            temperature = current_weather.get("temperature", "Not available")
            weather_code = current_weather.get("weathercode", -1)

            return WEATHER_DICT.get(weather_code, "Unknown code"), temperature, city
        except requests.RequestException as e:
            return "Error while searching for weather:", e


def create_note(content: str="") -> str|None:
    if content:
        with open("nota.txt", "a") as archivo:  # Save to a file "nota.txt"
            archivo.write(content + "\n")
        return "Note saved successfully"  # Already in English
    else:
        return "No content to save"  # Already in English
def read_notes() -> str:
    if os.path.exists("nota.txt"):
        with open("nota.txt", "r") as archivo:
            contenido = archivo.read()
        return f"These are your notes: {contenido}"  # Already in English
        
    else:
        return "No notes found"  # Already in English

def create_contact(nom: str="", number: str="", mail: str="") -> None|str:
    num = number.replace("más", "+").replace(" ", "")
    email = mail.replace("arroba", "@").replace("punto", ".").replace(" ", "").replace("dot", ".").replace("at", "@")

    return (agenda.add_contact(nom, num, email))
def delete_contact(name: str):
    return agenda.delete_contact(name)


def show_calendar() -> tuple[str, str]:
    return "searching in calendar", calendario.show_event()  # Already in English

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
        return "Error in the date format"  # Already in English
    print(name, date, hora, format_date)
    a = calendario.add_events(name, format_date, hora)
    if not a:
        return "An error occurred"  # Already in English
    else:
        return a