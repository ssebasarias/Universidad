-- Creamos la base de datos
CREATE DATABASE panic;

-- Cambiamos a la base de datos
\c panic;

-- Creamos la tabla para los puntos de encuentro
CREATE TABLE puntos_encuentro (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  latitud NUMERIC(10, 8) NOT NULL,
  longitud NUMERIC(11, 8) NOT NULL,
  descripcion VARCHAR(200)
);

-- Creamos la tabla para los participantes
CREATE TABLE participantes (
  id SERIAL PRIMARY KEY,
  nombre_completo VARCHAR(100) NOT NULL,
  identificacion_personal VARCHAR(20) NOT NULL,
  correo VARCHAR(50) NOT NULL,
  estado_salud VARCHAR(50),
  discapacidad BOOLEAN DEFAULT FALSE,
  ubicacion_latitud NUMERIC(10, 8),
  ubicacion_longitud NUMERIC(11, 8),
  telefono_propio VARCHAR(20),
  telefono_conocido VARCHAR(20)
);

-- Creamos la tabla para las actividades de los participantes
CREATE TABLE actividades (
  id SERIAL PRIMARY KEY,
  id_participante INTEGER NOT NULL REFERENCES participantes(id),
  id_punto_encuentro INTEGER NOT NULL REFERENCES puntos_encuentro(id),
  llegada TIMESTAMP,
  tiempo_llegada INTERVAL,
  ritmo_cardiaco INTEGER,
  registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Creamos una vista para las estadísticas generales
CREATE OR REPLACE VIEW estadisticas_generales AS
SELECT COUNT(DISTINCT participantes.id) AS num_participantes,
       COUNT(DISTINCT actividades.id_participante) AS num_llegaron,
       COUNT(DISTINCT actividades.id_punto_encuentro) AS num_puntos,
       AVG(EXTRACT(EPOCH FROM tiempo_llegada)) AS tiempo_promedio,
       MAX(EXTRACT(EPOCH FROM tiempo_llegada)) AS tiempo_maximo,
       MIN(EXTRACT(EPOCH FROM tiempo_llegada)) AS tiempo_minimo,
       MAX(ritmo_cardiaco) AS ritmo_cardiaco_maximo,
       MIN(ritmo_cardiaco) AS ritmo_cardiaco_minimo
FROM participantes
LEFT JOIN actividades ON participantes.id = actividades.id_participante;