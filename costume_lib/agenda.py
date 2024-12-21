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
def add_contact(name:str, teleph="0", email="") -> str:
    """Adds a contact"""
    #print(telefono)
    b = teleph.split("+34")
    try:
        b[1] 
        if len(b[1]) == 9:  #combrobar los caracters
            #print("es un telefono") 
            numero_sin = int(b[1][0]) 
            if numero_sin == 6 or numero_sin == 7: #combrueba si es un movil
                #print("es un movil")
                cursor.execute('''
                INSERT INTO contactos (nombre, telefono, email) VALUES (?, ?, ?)''', (name, teleph, email))
                conn.commit()
                if __name__ != "__main__":
                    conn.close()
                return(f'Contacto {name} agregado.')

    except IndexError:
        print(f"Numero no valido. Debe empezar con +34 {teleph}")
        return(f"Numero no valido. Debe empezar con +34 {teleph}")
        
# Función para mostrar todos los contactos
def search_contact(filtro: str) -> str:
    """Search for a contact"""
    cursor.execute("""SELECT * FROM contactos WHERE nombre like '{}'""".format(filtro))
    contactos = cursor.fetchall()
    try:
        tupla = contactos[0] #sacar datos de la base de datos
        nombre = tupla[1]
        numero = int(tupla[2])
        email = tupla[3]

        print(f"\nNombre: {nombre}\nTeléfono: {numero}")
        return nombre, numero
    except IndexError:
        return None
    
def delete_contact(nom: str) -> None:
    """deletes a contact"""
    cursor.execute(f"""DELETE FROM contactos WHERE nombre='{nom}'""")    
    conn.commit()
    if __name__ != "__main__":
        conn.close()    
    return f"{nom} borrado correctamente"

# Función principal
def main() -> None:
    """Funcion no util. Es la interfaz"""
    while True:

        try:
            print("\nAgenda de Contactos")
            print("1. Agregar contacto")
            print("2. Mostrar contactos")
            print("3. Eliminar contacto")
            print("4. Salir")
            opcion = input("Selecciona una opción: ")

            if opcion == '1':
                nombre = input("\nNombre: ")
                telefono = input("Teléfono: ")
                email = input("Email: ")
                print(add_contact(nombre, telefono, email))
            elif opcion == '2':
                nombre = input("\nNombre: ")
                print(search_contact(nombre))
            elif opcion == '3':
                nombre = input("\nNombre: ")
                delete_contact(nombre)
            elif opcion == '4':
                break
                
            else:
                print("\nOpción no válida. Inténtalo de nuevo.")
        except KeyboardInterrupt:
            conn.close()
            print("\nSaliendo...")
            break

    # Cerrar la conexión a la base de datos
    conn.close()

if __name__ == '__main__':
    main()
    