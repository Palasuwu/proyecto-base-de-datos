import threading
import psycopg2
import os
from dotenv import load_dotenv
from time import sleep

# Cargar las variables del archivo .env
load_dotenv()

# Obtener las variables de entorno
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Funcion para conectar a la base de datos
def conectar_base_datos():
    try:
        conexion = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Conexion exitosa a la base de datos :)")
        return conexion
    except Exception as error:
        print("Error al conectar a la base de datos:", error)
        return None

# Funcion para cerrar la conexion a la base de datos
def cerrar_conexion(conexion):
    if conexion:
        conexion.close()
        print("Conexion cerrada correctamente.")

# Funcion para mostrar el contenido de las tablas
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
        seleccion = int(input("Seleccione el numero de la tabla para ver su contenido (0 para regresar): "))
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
            print("Seleccion invalida. Intente de nuevo.")
    except ValueError:
        print("Entrada invalida. Por favor, ingrese un numero.")

# Funcion para reservar un asiento
def reservar_asiento(conexion, asiento_id, usuario_id, isolation_level):
    try:
        # Establecer el nivel de aislamiento para la transaccion
        cursor = conexion.cursor()
        cursor.execute(f"SET TRANSACTION ISOLATION LEVEL {isolation_level};")
        cursor.execute("BEGIN;")
        
        # Verificar si el asiento ya esta reservado
        cursor.execute("SELECT estado FROM asientos WHERE id_asiento = %s FOR UPDATE;", (asiento_id,))
        resultado = cursor.fetchone()
        
        if resultado and resultado[0] != 'activo':
            print(f"Usuario {usuario_id}: El asiento {asiento_id} ya esta reservado o inactivo.")
        else:
            # Reservar el asiento (marcar como reservado)
            cursor.execute("UPDATE asientos SET estado = 'reservado' WHERE id_asiento = %s;", (asiento_id,))
            print(f"Usuario {usuario_id}: Reservo el asiento {asiento_id} exitosamente.")
        
        # Confirmar la transaccion
        conexion.commit()
    except Exception as e:
        conexion.rollback()
        print(f"Usuario {usuario_id}: Error al intentar reservar el asiento {asiento_id}: {e}")
    finally:
        cursor.close()

# Funcion para obtener los asientos disponibles
def obtener_asientos_disponibles(conexion):
    try:
        cursor = conexion.cursor()
        # Obtener columnas relevantes de la tabla asientos
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

# Funcion para simular reservas de asientos
def simular_reservas(asiento_id, num_usuarios, isolation_level):
    # Conectar a la base de datos
    conexion = conectar_base_datos()
    if not conexion:
        return

    print(f"\nSimulando {num_usuarios} usuarios con nivel de aislamiento: {isolation_level}")
    
    # Mostrar asientos disponibles antes de iniciar la simulacion
    obtener_asientos_disponibles(conexion)

    # Crear multiples hilos para simular usuarios
    threads = []
    for usuario_id in range(1, num_usuarios + 1):
        thread = threading.Thread(target=reservar_asiento, args=(conexion, asiento_id, usuario_id, isolation_level))
        threads.append(thread)
        thread.start()
        sleep(0.1)  # Simular un pequeno retraso entre usuarios

    # Esperar a que todos los hilos terminen
    for thread in threads:
        thread.join()

    # Mostrar asientos disponibles despues de la simulacion
    obtener_asientos_disponibles(conexion)

    # Cerrar la conexion
    cerrar_conexion(conexion)

# Funcion principal del menu
def menu():
    conexion = None  # Inicializar la conexion fuera del bucle
    while True:
        print("\nMenu:")
        print("--------------------------------")
        print("1. Conectar a la base de datos")
        print("2. Mostrar nombre de la base de datos")
        print("3. Mostrar contenido en tablas:")
        print("4. Simular reservas de asientos")
        print("5. Salir")
        print("--------------------------------")

        opcion = input("Seleccione una opcion: ")

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
                # Mostrar asientos disponibles
                obtener_asientos_disponibles(conexion)
                
                # Submenu para la simulacion
                try:
                    asiento_id = int(input("Ingrese el ID del asiento a reservar: "))
                    num_usuarios = int(input("Ingrese el numero de usuarios simultaneos (5, 10, 20, 30): "))
                    
                    print("Seleccione el nivel de aislamiento:")
                    print("1. READ COMMITTED")
                    print("2. REPEATABLE READ")
                    print("3. SERIALIZABLE")
                    
                    nivel = input("Seleccione una opcion: ")
                    if nivel == "1":
                        isolation_level = "READ COMMITTED"
                    elif nivel == "2":
                        isolation_level = "REPEATABLE READ"
                    elif nivel == "3":
                        isolation_level = "SERIALIZABLE"
                    else:
                        print("Nivel de aislamiento no valido. Intente de nuevo.")
                        continue
                    
                    # Ejecutar la simulacion
                    simular_reservas(asiento_id, num_usuarios, isolation_level)
                except ValueError:
                    print("Entrada invalida. Por favor, ingrese un numero valido.")
            else:
                print("Primero debe conectar a la base de datos.")
        elif opcion == "5":
            print("Saliendo del programa...")
            cerrar_conexion(conexion)
            break
        else:
            print("Opcion no valida. Intente de nuevo.")

menu()
