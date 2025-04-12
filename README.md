# Instrucciones para Ejecutar el Programa

## **1. Requisitos Previos**
Antes de ejecutar el programa, asegúrate de tener lo siguiente instalado en tu sistema:
- **Python 3.8 o superior**: Puedes descargarlo desde [python.org](https://www.python.org/).
- **PostgreSQL**: Asegúrate de tener una base de datos PostgreSQL configurada y en funcionamiento.

---

## **2. Crear la Base de Datos y las Tablas**
1. Abre tu cliente de PostgreSQL (como `psql` o pgAdmin).
2. Crea una base de datos para el programa:
   ```sql
   CREATE DATABASE proyecto;
   ```
3. Conéctate a la base de datos:
   ```sql
   \c proyecto
   ```
4. Crea las tablas necesarias para el programa:

   ### Usuarios
   Almacena la información de los usuarios del sistema.
   ```sql
   CREATE TABLE usuarios (
       id_usuario SERIAL PRIMARY KEY,
       nombre VARCHAR(100) NOT NULL,
       email VARCHAR(100) UNIQUE NOT NULL,
       telefono VARCHAR(20),
       fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

   ### Espacios
   Define los espacios donde se realizan los eventos.
   ```sql
   CREATE TABLE espacios (
       id_espacio SERIAL PRIMARY KEY,
       nombre VARCHAR(100) NOT NULL,
       descripcion TEXT,
       capacidad INT
   );
   ```

   ### Eventos
   Guarda la información de los eventos programados.
   ```sql
   CREATE TABLE eventos (
       id_evento SERIAL PRIMARY KEY,
       nombre VARCHAR(100) NOT NULL,
       descripcion TEXT,
       fecha_inicio TIMESTAMP NOT NULL,
       fecha_fin TIMESTAMP NOT NULL,
       ubicacion VARCHAR(150),
       capacidad_total INT,
       tipo_evento VARCHAR(50)
   );
   ```

   ### Asientos
   Registra los asientos disponibles en los espacios.
   ```sql
   CREATE TABLE asientos (
       id_asiento SERIAL PRIMARY KEY,
       id_espacio INT REFERENCES espacios(id_espacio),
       tipo_asiento VARCHAR(50),
       estado VARCHAR(20) DEFAULT 'activo'
   );
   ```

   ### Reservas
   Administra las reservas de los eventos.
   ```sql
   CREATE TABLE reservas (
       id_reserva SERIAL PRIMARY KEY,
       id_usuario INT REFERENCES usuarios(id_usuario),
       id_evento INT REFERENCES eventos(id_evento),
       fecha_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       estado VARCHAR(30) DEFAULT 'pendiente'
   );
   ```

   ### Reserva de Asientos
   Asocia las reservas con los asientos específicos.
   ```sql
   CREATE TABLE reserva_asientos (
       id_reserva_asiento SERIAL PRIMARY KEY,
       id_reserva INT REFERENCES reservas(id_reserva),
       id_asiento INT REFERENCES asientos(id_asiento)
   );
   ```

   ### Pagos
   Registra los pagos de las reservas.
   ```sql
   CREATE TABLE pagos (
       id_pago SERIAL PRIMARY KEY,
       id_reserva INT REFERENCES reservas(id_reserva),
       monto NUMERIC(10, 2) NOT NULL,
       fecha_pago TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       metodo_pago VARCHAR(50),
       estado_pago VARCHAR(30) DEFAULT 'pendiente'
   );
   ```

   ### Check-in
   Registra la asistencia a los eventos.
   ```sql
   CREATE TABLE checkin (
       id_checkin SERIAL PRIMARY KEY,
       id_reserva INT REFERENCES reservas(id_reserva),
       fecha_checkin TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       estado VARCHAR(30) DEFAULT 'asistió'
   );
   ```

5. Inserta datos de ejemplo en las tablas:

   #### Usuarios
   ```sql
   INSERT INTO usuarios (nombre, email, telefono) VALUES
   ('Ana Torres', 'ana@example.com', '555-1234'),
   ('Luis Gómez', 'luis@example.com', '555-5678'),
   ('María Pérez', 'maria@example.com', '555-8765');
   ```

   #### Espacios
   ```sql
   INSERT INTO espacios (nombre, descripcion, capacidad) VALUES
   ('Sala Principal', 'Espacio central con mesas largas', 50),
   ('Terraza', 'Área exterior techada', 30);
   ```

   #### Eventos
   ```sql
   INSERT INTO eventos (nombre, descripcion, fecha_inicio, fecha_fin, ubicacion, capacidad_total, tipo_evento) VALUES
   ('Noche de Rol', 'Evento de Dungeons & Dragons', '2025-04-10 18:00', '2025-04-10 22:00', 'Sala Principal', 20, 'rol'),
   ('Torneo de Catan', 'Competencia amistosa de Catan', '2025-04-12 17:00', '2025-04-12 21:00', 'Terraza', 16, 'torneo');
   ```

   #### Asientos
   ```sql
   INSERT INTO asientos (id_espacio, tipo_asiento) VALUES
   (1, 'normal'),
   (1, 'normal'),
   (2, 'vip'),
   (2, 'vip');
   ```

   #### Reservas
   ```sql
   INSERT INTO reservas (id_usuario, id_evento, estado) VALUES
   (1, 1, 'confirmada'),
   (2, 1, 'pendiente'),
   (3, 2, 'confirmada');
   ```

   #### Reserva de Asientos
   ```sql
   INSERT INTO reserva_asientos (id_reserva, id_asiento) VALUES
   (1, 1),
   (2, 2),
   (3, 3);
   ```

   #### Pagos
   ```sql
   INSERT INTO pagos (id_reserva, monto, metodo_pago, estado_pago) VALUES
   (1, 150.00, 'tarjeta', 'pagado'),
   (3, 200.00, 'paypal', 'pagado');
   ```

   #### Check-in
   ```sql
   INSERT INTO checkin (id_reserva, estado) VALUES
   (1, 'asistió'),
   (2, 'no asistió'),
   (3, 'asistió');
   ```

---
## **3. Configurar el base de datos**
Configurar la base de datos para esto se debe realizar lo siguiente:
1.Dirigirse al apartado de Tool Workspace en PSQL hasta encontrar esta ventana

![image](https://github.com/user-attachments/assets/10fcc9a9-a39d-48c0-8a86-ad3a0026de33)

2. Luego encargate de seleccionar la base de datos en la cual se trabajo (siendo la base de datos llamada proyecto la que se utilizo)
   
![image](https://github.com/user-attachments/assets/3a9b569b-f60b-4802-af5e-21eb320a3bba)

4. Ya por ultimo ponle una contraseña facil de recordar y valida la coneccion usando la contraseña que siempre usas para acceder pgAdmin4
   
![image](https://github.com/user-attachments/assets/62a05e22-72ce-4134-b9f6-1ea55fa763db)

![image](https://github.com/user-attachments/assets/02e1a22c-2c52-468c-998a-9953580c1bf4)

## **4. Configurar el Entorno**
1. Crea un archivo llamado `.env` en el mismo directorio donde está el programa `main.py`.
2. Agrega las credenciales de tu base de datos PostgreSQL al archivo `.env`:
   ```
   DB_NAME=proyecto
   DB_USER=tu_usuario
   DB_PASSWORD=tu_contraseña
   DB_HOST=localhost
   DB_PORT=5432
   ```
![image](https://github.com/user-attachments/assets/d3a6d540-dc34-48e4-83b8-a43f75dd7abe)

Importante: Asegurarse que tanto la contraseña como el DB_port coincidan con lo colocado previamente 

---

## **5. Instalar las Bibliotecas Necesarias**
1. Abre una terminal o consola.
2. Asegúrate de estar en el mismo directorio donde está el archivo `main.py`.
3. Crea un entorno virtual (opcional pero recomendado):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
4. Instala las bibliotecas necesarias usando `pip`:
   ```bash
   pip install psycopg2-binary python-dotenv
   ```

---

## **6. Ejecutar el Programa**
1. En la terminal, asegúrate de estar en el directorio donde está el archivo `main.py`.
2. Ejecuta el programa:
   ```bash
   python main.py
   ```

---

## **7. Usar el Programa**
Cuando ejecutes el programa, verás un menú como este:
```
Menu:
--------------------------------
1. Conectar a la base de datos
2. Mostrar nombre de la base de datos
3. Mostrar contenido en tablas:
4. Simular reservas de asientos
5. Salir
6. Reiniciar estado de los asientos
--------------------------------
Seleccione una opcion:
```

### Opciones del Menú:
1. **Conectar a la base de datos**:
   - Establece la conexión con la base de datos PostgreSQL configurada en el archivo `.env`.

2. **Mostrar nombre de la base de datos**:
   - Muestra el nombre de la base de datos configurada.

3. **Mostrar contenido en tablas**:
   - Lista las tablas disponibles en la base de datos y permite ver su contenido.

4. **Simular reservas de asientos**:
   - Simula múltiples usuarios intentando reservar un asiento. Debes ingresar:
     - El ID del asiento a reservar.
     - El número de usuarios simultáneos (5, 10, 20, 30).
     - El nivel de aislamiento (`READ COMMITTED`, `REPEATABLE READ`, `SERIALIZABLE`).

5. **Salir**:
   - Cierra el programa.

6. **Reiniciar estado de los asientos**:
   - Restaura el estado de todos los asientos a su valor por defecto (`activo`).

---

## **8. Notas Adicionales**
- **Errores Comunes**:
  - Si ves un error relacionado con la conexión a la base de datos, verifica que las credenciales en el archivo `.env` sean correctas.
  - Si falta alguna biblioteca, asegúrate de instalarla con `pip`.

- **Pruebas de Concurrencia**:
  - Para observar diferencias en los niveles de aislamiento, prueba con múltiples usuarios simultáneos y diferentes niveles de aislamiento.

---

## **9. Ejemplo de Ejecución**
### Entrada:
```
Seleccione una opcion: 4
Ingrese el ID del asiento a reservar: 1
Ingrese el numero de usuarios simultaneos (5, 10, 20, 30): 5
Seleccione el nivel de aislamiento:
1. READ COMMITTED
2. REPEATABLE READ
3. SERIALIZABLE
Seleccione una opcion: 1
```

### Salida:
```
Simulando 5 usuarios con nivel de aislamiento: READ COMMITTED
Usuario 1: Reservo el asiento 1 exitosamente.
Usuario 2: El asiento 1 ya esta reservado o inactivo.
Usuario 3: El asiento 1 ya esta reservado o inactivo.
Usuario 4: El asiento 1 ya esta reservado o inactivo.
Usuario 5: El asiento 1 ya esta reservado o inactivo.
```

---

Siguiendo estos pasos, cualquier persona debería poder configurar y ejecutar el programa correctamente.
