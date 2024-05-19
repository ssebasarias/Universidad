-- Crear un bloque por el cual se de formato a un número de cuenta suministrado por 
-- completo, por ejmplo: 11111111111111111111
-- a. Formateado a: 1111-1111-11-1111111111
-- b. Debemos usar un parámetro de tipo IN-OUT

CREATE OR REPLACE PROCEDURE formatear_cuenta(p_numero_cuenta IN OUT VARCHAR2) AS
BEGIN
    -- Eliminar cualquier guión existente en el número de cuenta
    p_numero_cuenta := REPLACE(p_numero_cuenta, '-', '');

    -- Insertar guiones en posiciones específicas
    p_numero_cuenta := SUBSTR(p_numero_cuenta, 1, 4) || '-' ||
                      SUBSTR(p_numero_cuenta, 5, 4) || '-' ||
                      SUBSTR(p_numero_cuenta, 9, 2) || '-' ||
                      SUBSTR(p_numero_cuenta, 11);

    -- Mostrar el número de cuenta formateado
    DBMS_OUTPUT.PUT_LINE('Número de cuenta formateado: ' || p_numero_cuenta);
END formatear_cuenta;
/



DECLARE
    v_numero_cuenta VARCHAR2(30) := '11111111111111111'; -- Cambia este valor al número de cuenta deseado
BEGIN
    -- Llama al procedimiento para formatear el número de cuenta
    formatear_cuenta(p_numero_cuenta => v_numero_cuenta);
END;
