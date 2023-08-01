<?php
$host = 'localhost';
$port = '5432';
$dbname = 'PANIC';
$user = 'postgres';
$password = 'sisas0091';

// Conexión a la base de datos usando pg_connect
$dbconn = pg_connect("host={$host} port={$port} dbname={$dbname} user={$user} password={$password}");

if (!$dbconn) {
    die("Error en la conexión: " . pg_last_error());
}

$nombre = $_POST['nombre'];
$correo = $_POST['correo'];
$estado_salud = $_POST['estado_salud'];
$discapacidad = $_POST['discapacidad'];
$telefono = $_POST['telefono'];
$tel_conocido = $_POST['tel_conocido'];

// Ejecución de consulta SQL usando pg_query
$result = pg_query($dbconn, "INSERT INTO participantes (nombre, correo, estado_salud, discapacidad, telefono, tel_conocido)
                            VALUES ('{$nombre}', '{$correo}', '{$estado_salud}', '{$discapacidad}', '{$telefono}', '{$tel_conocido}')");

if (!$result) {
    die("Error en la consulta: " . pg_last_error());
} else {
    echo "Registro insertado correctamente.";
}

// Cerrar conexión
pg_close($dbconn);
?>
