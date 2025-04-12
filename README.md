### SQL para la creación de la base de datos y tablas:

```sql
-- Crear base de datos
CREATE DATABASE proyecto;

-- Tabla: usuarios
CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: espacios
CREATE TABLE espacios (
    id_espacio SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    capacidad INT
);

-- Tabla: eventos
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

-- Tabla: asientos
CREATE TABLE asientos (
    id_asiento SERIAL PRIMARY KEY,
    id_espacio INT REFERENCES espacios(id_espacio),
    tipo_asiento VARCHAR(50),
    estado VARCHAR(20) DEFAULT 'activo'
);

-- Tabla: reservas
CREATE TABLE reservas (
    id_reserva SERIAL PRIMARY KEY,
    id_usuario INT REFERENCES usuarios(id_usuario),
    id_evento INT REFERENCES eventos(id_evento),
    fecha_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(30) DEFAULT 'pendiente'
);

-- Tabla: reserva_asientos
CREATE TABLE reserva_asientos (
    id_reserva_asiento SERIAL PRIMARY KEY,
    id_reserva INT REFERENCES reservas(id_reserva),
    id_asiento INT REFERENCES asientos(id_asiento)
);

-- Tabla: pagos
CREATE TABLE pagos (
    id_pago SERIAL PRIMARY KEY,
    id_reserva INT REFERENCES reservas(id_reserva),
    monto NUMERIC(10, 2) NOT NULL,
    fecha_pago TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metodo_pago VARCHAR(50),
    estado_pago VARCHAR(30) DEFAULT 'pendiente'
);

-- Tabla: checkin
CREATE TABLE checkin (
    id_checkin SERIAL PRIMARY KEY,
    id_reserva INT REFERENCES reservas(id_reserva),
    fecha_checkin TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(30) DEFAULT 'asistió'
);

-- Insertar datos

-- Usuarios
INSERT INTO usuarios (nombre, email, telefono) VALUES
('Ana Torres', 'ana@example.com', '555-1234'),
('Luis Gómez', 'luis@example.com', '555-5678'),
('María Pérez', 'maria@example.com', '555-8765');

-- Espacios
INSERT INTO espacios (nombre, descripcion, capacidad) VALUES
('Sala Principal', 'Espacio central con mesas largas', 50),
('Terraza', 'Área exterior techada', 30);

-- Eventos
INSERT INTO eventos (nombre, descripcion, fecha_inicio, fecha_fin, ubicacion, capacidad_total, tipo_evento) VALUES
('Noche de Rol', 'Evento de Dungeons & Dragons', '2025-04-10 18:00', '2025-04-10 22:00', 'Sala Principal', 20, 'rol'),
('Torneo de Catan', 'Competencia amistosa de Catan', '2025-04-12 17:00', '2025-04-12 21:00', 'Terraza', 16, 'torneo');

-- Asientos
INSERT INTO asientos (id_espacio, tipo_asiento) VALUES
(1, 'normal'),
(1, 'normal'),
(2, 'vip'),
(2, 'vip');

-- Reservas
INSERT INTO reservas (id_usuario, id_evento, estado) VALUES
(1, 1, 'confirmada'),
(2, 1, 'pendiente'),
(3, 2, 'confirmada');

-- Reserva_Asientos
INSERT INTO reserva_asientos (id_reserva, id_asiento) VALUES
(1, 1),
(2, 2),
(3, 3);

-- Pagos
INSERT INTO pagos (id_reserva, monto, metodo_pago, estado_pago) VALUES
(1, 150.00, 'tarjeta', 'pagado'),
(3, 200.00, 'paypal', 'pagado');

-- Check-in
INSERT INTO checkin (id_reserva, estado) VALUES
(1, 'asistió'),
(2, 'no asistió'),
(3, 'asistió');
