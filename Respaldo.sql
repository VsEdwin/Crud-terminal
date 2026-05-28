CREATE DATABASE crud_usuarios;

USE crud_usuarios;

-- =====================================
-- TABLA USUARIOS
-- =====================================

CREATE TABLE t_usuarios(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    edad INT NOT NULL,
    telefono VARCHAR(20) NOT NULL
);

-- =====================================
-- TABLA ROLES
-- =====================================

CREATE TABLE t_roles(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_rol VARCHAR(50) NOT NULL
);

-- =====================================
-- INSERTAR ROLES
-- =====================================

INSERT INTO t_roles(nombre_rol)
VALUES
('Administrador'),
('Empleado'),
('Cliente');

-- =====================================
-- TABLA HISTORIAL SISTEMA
-- =====================================

CREATE TABLE t_historial_sistema(
    id INT AUTO_INCREMENT PRIMARY KEY,
    accion TEXT NOT NULL,
    fecha DATETIME NOT NULL
);