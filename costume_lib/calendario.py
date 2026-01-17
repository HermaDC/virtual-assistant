from datetime import datetime
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta del archivo JSON donde se almacenarán los eventos
FILE_PATH = os.path.join(BASE_DIR, 'calendario.json')

# Cargar los eventos desde el archivo JSON
def load_events() -> list:
    """return a list of all the events"""
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r') as file:
            return json.load(file)
    return []

# Guardar los eventos en el archivo JSON
def save_events(events) -> None:

    with open(FILE_PATH, 'w') as file:
        json.dump(events, file, indent=4)

# Updated `add_events` to improve error handling and validation
def add_events(name: str = "", date: str = "", hour: str = "00:00") -> str | None:
    """Adds an event to the events list"""
    try:
        fecha = datetime.strptime(f"{date} {hour}", '%Y-%m-%d %H:%M')
    except ValueError:
        return "Invalid date or time format."

    eventos = load_events()
    eventos.append({
        'nombre': name,
        'fecha': date,
        'hora': hour
    })
    save_events(eventos)
    return f"Event '{name}' added successfully."

# Updated `show_event` to improve formatting
def show_event() -> str:
    """Returns all the events saved"""
    eventos = load_events()
    if not eventos:
        return "No events scheduled."
    resultado = "Scheduled events:\n"
    for i, evento in enumerate(eventos, start=1):
        resultado += f"{i}. {evento['nombre']} - Date: {evento['fecha']} Time: {evento['hora']}.\n"
    return resultado

# Updated `delete_event` to improve error handling
def delete_event(num_evento: int = 0) -> str:
    """Deletes a saved event"""
    eventos = load_events()
    if not eventos:
        return "No events to delete."
    try:
        evento = eventos.pop(num_evento - 1)
        save_events(eventos)
        return f"Event '{evento['nombre']}' deleted successfully."
    except (IndexError, ValueError):
        return "Invalid event number."

# Archivar eventos pasados
def archivar_eventos():
    eventos = load_events()
    eventos_activos = []
    eventos_archivados = []
    ahora = datetime.now()

    for evento in eventos:
        fecha_evento = datetime.strptime(f"{evento['fecha']} {evento['hora']}", '%Y-%m-%d %H:%M')
        if fecha_evento < ahora:
            eventos_archivados.append(evento)
        else:
            eventos_activos.append(evento)
    
    # Guardar eventos activos y archivar los pasados
    save_events(eventos_activos)
    with open('eventos_archivados.json', 'w') as archivo:
        json.dump(eventos_archivados, archivo, indent=4)

    print(f"{len(eventos_archivados)} events archived.")  # Updated to English

# Menú principal
def menu() -> None:
    while True:
        print("\n--- Calendario de Eventos ---")
        print("1. Agregar evento")
        print("2. Listar eventos")
        print("3. Eliminar evento")
        print("4. Archivar eventos pasados")
        print("5. Salir\n")
        opcion = input("Elige una opción: ")
        
        if opcion == '1':
            add_events()
        elif opcion == '2':
            show_event()
        elif opcion == '3':
            delete_event()
        elif opcion == '4':
            archivar_eventos()
        elif opcion == '5':
            print("Exiting the calendar.")  # Updated to English
            break
        else:
            print("Invalid option. Please try again.")  # Updated to English

# Ejecutar el menú principal
if __name__ == "__main__":
    menu()
