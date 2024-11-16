from datetime import datetime
import json
import os

# Ruta del archivo JSON donde se almacenarán los eventos
FILE_PATH = 'calendario.json'

# Cargar los eventos desde el archivo JSON
def cargar_eventos() -> list:
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r') as archivo:
            return json.load(archivo)
    return []

# Guardar los eventos en el archivo JSON
def guardar_eventos(eventos) -> None:
    with open(FILE_PATH, 'w') as archivo:
        json.dump(eventos, archivo, indent=4)

# Agregar un evento al calendario
def agregar_evento(nombre: str=None, fecha: str=None, hora="00:00") -> str:
    
    if not nombre:
        nombre = input("Nombre del evento: ")
        fecha_str = input("Fecha del evento (YYYY-MM-DD): ")
        hora_str = input("Hora del evento (HH:MM, 24h): ")
        print("\n")
        
        try:
            fecha = datetime.strptime(f"{fecha_str} {hora_str}", '%Y-%m-%d %H:%M')
        except ValueError:
            print("Formato de fecha u hora inválido. \n")
            return
        
        eventos = cargar_eventos()
        eventos.append({
            'nombre': nombre,
            'fecha': fecha_str,
            'hora': hora_str
        })

        return
    print(fecha, hora)
    try:
        fecha = datetime.strptime(f"{fecha} {hora}", '%Y-%m-%d %H:%M')   
    except ValueError:
        print("no vale")
        return

    eventos = cargar_eventos()
    print(f"nombre: {nombre} fecha: {str(fecha)} hora: {hora}")
    eventos.append({
            'nombre': nombre,
            'fecha': str(fecha),
            'hora': hora
        })

         
    guardar_eventos(eventos)
    print(f"Evento '{nombre}' agregado con éxito. \n \n")
    return f"Evento '{nombre}' agregado con éxito."

# Listar todos los eventos
def listar_eventos() -> str:
    eventos = cargar_eventos()
    if not eventos:
        print("No hay eventos programados.\n")
        #print("---+---+---+---+---+--- \n \n")
    else:
        print("Eventos programados:")
        for i, evento in enumerate(eventos, start=1):
            print(f"{i}. {evento['nombre']} - Fecha: {evento['fecha']} Hora: {evento['hora']}")
            return f"{i}. {evento['nombre']}. Fecha: {evento['fecha']}"

# Eliminar un evento
def eliminar_evento(num_evento: int=None) -> None:
    listar_eventos()
    eventos = cargar_eventos()
    if eventos:
        if not num_evento:
            try:
                num_evento = int(input("Número del evento a eliminar: "))
                evento = eventos.pop(num_evento - 1)
                guardar_eventos(eventos)
                print(f"Evento '{evento['nombre']}' eliminado con éxito.")
            except (IndexError, ValueError):
                print("Número de evento inválido.")
        evento = eventos.pop(num_evento - 1)
        guardar_eventos(eventos)

# Archivar eventos pasados
def archivar_eventos():
    eventos = cargar_eventos()
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
    guardar_eventos(eventos_activos)
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
            agregar_evento()
        elif opcion == '2':
            listar_eventos()
        elif opcion == '3':
            eliminar_evento()
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
