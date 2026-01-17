import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'agenda.db')

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contactos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT NOT NULL,
        email TEXT
    )''')

# Función para agregar un contacto
def add_contact(name: str, teleph="0", email="") -> str | None:
    """Adds a contact"""
    teleph = teleph.replace(" ", "")
    if teleph.startswith("+34") and len(teleph) == 12 and teleph[3] in "67":
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            # Insertar el contacto en la base de datos
            cursor.execute('''INSERT INTO contactos (nombre, telefono, email) VALUES (?, ?, ?)''', (name, teleph, email))

        return f"Contact {name} added."
    else:
        return f"Invalid number: {teleph}"
        
# Función para mostrar todos los contactos
def search_contact(filtro: str) -> tuple[str, int] | None:
    """Search for a contact"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contactos WHERE nombre LIKE ?", (filtro,))
        contactos = cursor.fetchall()
    if contactos:
        nombre, numero, email = contactos[0][1:4]
        print(f"\nName: {nombre}\nPhone: {numero}")
        return nombre, numero
    return None
    
def delete_contact(name: str) -> str:
    """Deletes a contact"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contactos WHERE nombre = ?", (name,))

    return f"{name} deleted."

# Función principal
def main() -> None:
    """Función no util. Es la interfaz"""
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
                print("\nInvalid option. Please try again.")
        except KeyboardInterrupt:
            conn.close()
            print("\nExiting...")
            break

    # Cerrar la conexión a la base de datos
    conn.close()

if __name__ == '__main__':
    main()
