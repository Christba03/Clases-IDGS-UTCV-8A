-- Seed script: create the tienda database and populate sample data
CREATE DATABASE tienda;
\c tienda

CREATE TABLE clientes (
    cliente_id     SERIAL PRIMARY KEY,
    nombre         VARCHAR(50),
    apellido       VARCHAR(50),
    email          VARCHAR(100),
    fecha_registro TIMESTAMP DEFAULT NOW()
);

INSERT INTO clientes (nombre, apellido, email) VALUES
    ('Juan',   'Perez',     'juan@correo.com'),
    ('Maria',  'Lopez',     'maria@correo.com'),
    ('Carlos', 'Garcia',    'carlos@correo.com'),
    ('Ana',    'Martinez',  'ana@correo.com'),
    ('Luis',   'Hernandez', 'luis@correo.com');
