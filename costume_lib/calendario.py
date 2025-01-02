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

# Agregar un evento al calendario
def add_events(name: str=None, date: str=None, hour="00:00") -> str:
    """adds a avent to the events list"""
    if not name:
        name = input("Nombre del evento: ")
        date_str = input("Fecha del evento (YYYY-MM-DD): ")
        hour_str = input("Hora del evento (HH:MM, 24h): ")
        print("\n")
        
        try:
            date = datetime.strptime(f"{date_str} {hour_str}", '%Y-%m-%d %H:%M')
        except ValueError:
            print("Formato de fecha u hora inválido. \n")
            return
        
        eventos = load_events()
        eventos.append({
            'nombre': name,
            'fecha': date_str,
            'hora': hour_str
        })

        return
    print(date, hour)
    try:
        fecha = datetime.strptime(f"{date} {hour}", '%Y-%m-%d %H:%M')   
    except ValueError:
        print("no vale")
        return

    eventos = load_events()
    print(f"nombre: {name} fecha: {str(fecha)} hora: {hour}")
    eventos.append({
            'nombre': name,
            'fecha': str(fecha),
            'hora': hour
        })

         
    save_events(eventos)
    print(f"Evento '{name}' agregado con éxito. \n \n")
    return f"Evento '{name}' agregado con éxito."

# Listar todos los eventos
def show_event() -> str:
    """returns all the events saved"""
    eventos = load_events()
    if not eventos:
        return "No hay eventos programados.\n"
    else:
        resultado = "Eventos programados:\n"
        for i, evento in enumerate(eventos, start=1):
            resultado += f"{i}. {evento['nombre']} - Fecha: {evento['fecha']} Hora: {evento['hora']}.\n"
        return resultado


# Eliminar un evento
def delete_event(num_evento: int=None) -> None:
    """deletes a saved event"""
    show_event()
    eventos = load_events()
    if eventos:
        if not num_evento:
            try:
                num_evento = int(input("Número del evento a eliminar: "))
                evento = eventos.pop(num_evento - 1)
                save_events(eventos)
                print(f"Evento '{evento['nombre']}' eliminado con éxito.")
            except (IndexError, ValueError):
                print("Número de evento inválido.")
        evento = eventos.pop(num_evento - 1)
        save_events(evento)

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

    print(f"{len(eventos_archivados)} eventos archivados.")

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
            print("Saliendo del calendario.")
            break
        else:
            print("Opción inválida. Inténtalo de nuevo.")

# Ejecutar el menú principal
if __name__ == "__main__":
    menu()
