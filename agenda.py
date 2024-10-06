import sqlite3

# Conectar a la base de datos (se crea automáticamente si no existe)
conn = sqlite3.connect('agenda_contactos.db')
cursor = conn.cursor()

# Crear la tabla de contactos si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS contactos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT NOT NULL,
    email TEXT
)
''')

# Función para agregar un contacto
def agregar_contacto(nombre:str, telefono="0", email="") -> None:
    """Agrega un contacto a la agenda"""
    #print(telefono)
    b = telefono.split("+34")
    try:
        b[1] 
        if len(b[1]) == 9:  #combrobar los caracters
            #print("es un telefono") 
            numero_sin = int(b[1][0]) 
            if numero_sin == 6 or numero_sin == 7: #combrueba si es un movil
                #print("es un movil")
                cursor.execute('''
                INSERT INTO contactos (nombre, telefono, email)
                VALUES (?, ?, ?)
                ''', (nombre, telefono, email))
                conn.commit()
                print(f'Contacto {nombre} agregado.')

    except IndexError:
        print(f"Numero no valido. Debe empezar con +34 {telefono}")
        

# Función para mostrar todos los contactos
def buscar_contactos(filtro: str) -> str:
    """Busca un contacto en la agenda"""
    cursor.execute("""SELECT * FROM contactos WHERE nombre like '{}'""".format(filtro))
    contactos = cursor.fetchall()
    try:
        tupla = contactos[0] #sacar datos de la base de datos
        nombre = tupla[1]
        numero = int(tupla[2])
        email = tupla[3]

        print(f"Nombre: {nombre}\nTeléfono: {numero}")
        return nombre, numero
    except IndexError:
        return None
    

# Función principal
def main() -> None:
    """Funcion no util. Es la interfaz"""
    while True:

        try:
            print("\nAgenda de Contactos")
            print("1. Agregar contacto")
            print("2. Mostrar contactos")
            print("3. Salir")
            opcion = input("Selecciona una opción: ")

            if opcion == '1':
                nombre = input("Nombre: ")
                telefono = input("Teléfono: ")
                email = input("Email: ")
                agregar_contacto(nombre, telefono, email)
            elif opcion == '2':
                nombre = input("Nombre: ")
                buscar_contactos(nombre)
            elif opcion == '3':
                break
            else:
                print("Opción no válida. Inténtalo de nuevo.")
        except KeyboardInterrupt:
            print("\nSaliendo...")
            break

    # Cerrar la conexión a la base de datos
    conn.close()

if __name__ == '__main__':
    main()
