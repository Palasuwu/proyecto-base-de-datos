import threading
import psycopg2
import os
from dotenv import load_dotenv
from time import sleep

# Cargar las variables del .env
load_dotenv()

# Obtener las variables de entorno
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def conectar_base_datos():
    try:
        conexion = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Conexión exitosa a la base de datos :)")
        return conexion
    except Exception as error:
        print("Error al conectar a la base de datos:", error)
        return None

def cerrar_conexion(conexion):
    if conexion:
        conexion.close()
        print("Conexión cerrada correctamente.")

def mostrar_contenido_tabla(conexion):
    cursor = conexion.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    tablas = cursor.fetchall()

    if not tablas:
        print("No hay tablas disponibles en la base de datos.")
        return

    print("Tablas en la base de datos:")
    for i, tabla in enumerate(tablas, start=1):
        print(f"{i}. {tabla[0]}")

    try:
        seleccion = int(input("Seleccione el número de la tabla para ver su contenido (0 para regresar): "))
        if seleccion == 0:
            return
        elif 1 <= seleccion <= len(tablas):
            nombre_tabla = tablas[seleccion - 1][0]
            cursor.execute(f"SELECT * FROM {nombre_tabla}")
            filas = cursor.fetchall()
            print(f"Contenido de la tabla '{nombre_tabla}':")
            for fila in filas:
                print(fila)
        else:
            print("Selección inválida. Intente de nuevo.")
    except ValueError:
        print("Entrada inválida. Por favor, ingrese un número.")

def reservar_asiento(conexion, asiento_id, usuario_id, isolation_level):
    try:
        # Set the isolation level for the transaction
        cursor = conexion.cursor()
        cursor.execute(f"SET TRANSACTION ISOLATION LEVEL {isolation_level};")
        cursor.execute("BEGIN;")
        
        # Check if the seat is already reserved
        cursor.execute("SELECT estado FROM asientos WHERE id_asiento = %s FOR UPDATE;", (asiento_id,))
        resultado = cursor.fetchone()
        
        if resultado and resultado[0] != 'activo':
            print(f"Usuario {usuario_id}: El asiento {asiento_id} ya está reservado o inactivo.")
        else:
            # Reserve the seat (mark as reserved)
            cursor.execute("UPDATE asientos SET estado = 'reservado' WHERE id_asiento = %s;", (asiento_id,))
            print(f"Usuario {usuario_id}: Reservó el asiento {asiento_id} exitosamente.")
        
        # Commit the transaction
        conexion.commit()
    except Exception as e:
        conexion.rollback()
        print(f"Usuario {usuario_id}: Error al intentar reservar el asiento {asiento_id}: {e}")
    finally:
        cursor.close()

def obtener_asientos_disponibles(conexion):
    try:
        cursor = conexion.cursor()
        # Fetch relevant columns from the asientos table
        cursor.execute("SELECT id_asiento, estado, tipo_asiento FROM asientos;")
        asientos = cursor.fetchall()
        print("Asientos disponibles:")
        for asiento in asientos:
            estado = "Disponible" if asiento[1] == 'activo' else f"Reservado o inactivo"
            print(f"Asiento ID: {asiento[0]} - Tipo: {asiento[2]} - Estado: {estado}")
    except Exception as e:
        print(f"Error al obtener los asientos: {e}")
    finally:
        cursor.close()

def simular_reservas(asiento_id, num_usuarios, isolation_level):
    # Connect to the database
    conexion = conectar_base_datos()
    if not conexion:
        return

    print(f"\nSimulando {num_usuarios} usuarios con nivel de aislamiento: {isolation_level}")
    
    # Show available seats before starting the simulation
    obtener_asientos_disponibles(conexion)

    # Create multiple threads to simulate users
    threads = []
    for usuario_id in range(1, num_usuarios + 1):
        thread = threading.Thread(target=reservar_asiento, args=(conexion, asiento_id, usuario_id, isolation_level))
        threads.append(thread)
        thread.start()
        sleep(0.1)  # Simulate a small delay between users

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Show available seats after the simulation
    obtener_asientos_disponibles(conexion)

    # Close the connection
    cerrar_conexion(conexion)

def menu():
    conexion = None  # Initialize the connection outside the loop
    while True:
        print("\nMenú:")
        print("--------------------------------")
        print("1. Conectar a la base de datos")
        print("2. Mostrar nombre de la base de datos")
        print("3. Mostrar contenido en tablas:")
        print("4. Simular reservas de asientos")
        print("5. Salir")
        print("--------------------------------")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            conexion = conectar_base_datos()
        elif opcion == "2":
            print("Nombre de la base de datos:", DB_NAME)
        elif opcion == "3":
            if conexion:
                mostrar_contenido_tabla(conexion)
            else:
                print("Primero debe conectar a la base de datos.")
        elif opcion == "4":
            if conexion:
                # Display available seats
                obtener_asientos_disponibles(conexion)
                
                # Submenu for simulation
                try:
                    asiento_id = int(input("Ingrese el ID del asiento a reservar: "))
                    num_usuarios = int(input("Ingrese el número de usuarios simultáneos (5, 10, 20, 30): "))
                    
                    print("Seleccione el nivel de aislamiento:")
                    print("1. READ COMMITTED")
                    print("2. REPEATABLE READ")
                    print("3. SERIALIZABLE")
                    
                    nivel = input("Seleccione una opción: ")
                    if nivel == "1":
                        isolation_level = "READ COMMITTED"
                    elif nivel == "2":
                        isolation_level = "REPEATABLE READ"
                    elif nivel == "3":
                        isolation_level = "SERIALIZABLE"
                    else:
                        print("Nivel de aislamiento no válido. Intente de nuevo.")
                        continue
                    
                    # Run the simulation
                    simular_reservas(asiento_id, num_usuarios, isolation_level)
                except ValueError:
                    print("Entrada inválida. Por favor, ingrese un número válido.")
            else:
                print("Primero debe conectar a la base de datos.")
        elif opcion == "5":
            print("Saliendo del programa...")
            cerrar_conexion(conexion)
            break
        else:
            print("Opción no válida. Intente de nuevo.")

menu()
