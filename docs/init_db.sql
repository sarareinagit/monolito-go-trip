-- Crear base de datos
CREATE DATABASE IF NOT EXISTS go_trip;
USE go_trip;

-- Crear tabla reservas
CREATE TABLE IF NOT EXISTS reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_cliente VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    destino VARCHAR(100) NOT NULL,
    fecha_salida DATE NOT NULL,
    fecha_regreso DATE NOT NULL,
    num_personas INT NOT NULL CHECK (num_personas > 0),
    tipo_paquete ENUM('economico','estandar','lujo') NOT NULL,
    tipo_viaje ENUM('ocio','familiar','aventura','naturaleza','gastronomico','cultural') NOT NULL,
    forma_pago ENUM('pago_unico','a_plazos') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Datos de ejemplo
INSERT INTO reservas 
(nombre_cliente, email, telefono, destino, fecha_salida, fecha_regreso, num_personas, tipo_paquete, tipo_viaje, forma_pago)
VALUES 
('Carlos Martinez','carlos@example.com','654321987','Nueva York','2026-05-10','2026-05-20',2,'estandar','ocio','pago_unico'),
('Laura Gomez','laura@example.com','612345678','Tokio','2026-06-01','2026-06-14',1,'lujo','cultural','a_plazos'),
('Pedro Sanchez','pedro@example.com','699887766','Costa Rica','2026-07-05','2026-07-15',4,'economico','naturaleza','pago_unico'),
('Ana Ruiz','ana@example.com','677889900','Marruecos','2026-09-10','2026-09-20',3,'estandar','aventura','a_plazos'),
('Miguel Torres','miguel@example.com','688774455','San Sebastian','2026-08-01','2026-08-07',2,'lujo','gastronomico','pago_unico');
