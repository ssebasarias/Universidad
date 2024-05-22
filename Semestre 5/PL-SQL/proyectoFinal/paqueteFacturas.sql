-- PAQUETE FACTURAS
-- a. PROCEDIMIENTOS 
    -- i. CREAR_FACTURA (COD_FACTURA, FECHA,DESCRIPCIÓN). 
    --     1. Crear una factura con los valores indicados en los parámetros 
    --     2. Debe comprobar que no se duplica 
    -- ii. ELIMINAR_FACTURA (cod_factura). 
    --     1. Debe borrar la factura indicada en el parámetro
    --     2. Debe borrar también las líneas de facturas asociadas en la tabla LINEAS_FACTURA.
    -- iv. MOD_FECHA (COD_FACTURA,FECHA).
    --     1. Debe modificar la descripción de la factura que tenga el código del parámetro con la nueva fecha
-- b. FUNCIONES 
--     i. NUM_FACTURAS(FECHA_INICIO,FECHA_FIN). 
--          1. Devuelve el número de facturas que hay entre esas fechas
--  ii. TOTAL_FACTURA(COD_FACTURA.) 
--     1. Devuelve el total de la factura con ese código. Debe hacer el sumatorio de “pvp*unidades” 
--     de las líneas de esa factura en la tabla LINEAS_FACTURA


CREATE OR REPLACE PACKAGE FACTURAS_PKG AS
    -- PROCEDIMIENTOS 
    PROCEDURE CREAR_FACTURA (p_cod_factura IN NUMBER, p_fecha IN DATE, p_descripcion IN VARCHAR2);
    PROCEDURE ELIMINAR_FACTURA (p_cod_factura IN NUMBER);
    PROCEDURE MOD_DESCRI (p_cod_factura IN NUMBER, p_nueva_descripcion IN VARCHAR2);
    PROCEDURE MOD_FECHA (p_cod_factura IN NUMBER, p_nueva_fecha IN DATE);

    -- FUNCIONES 
    FUNCTION NUM_FACTURAS (p_fecha_inicio IN DATE, p_fecha_fin IN DATE) RETURN NUMBER;
    FUNCTION TOTAL_FACTURA (p_cod_factura IN NUMBER) RETURN NUMBER;
END FACTURAS_PKG;
/

CREATE OR REPLACE PACKAGE BODY FACTURAS_PKG AS
    -- PROCEDIMIENTOS 
    -- i. CREAR_FACTURA (COD_FACTURA, FECHA,DESCRIPCIÓN). 
    --     1. Crear una factura con los valores indicados en los parámetros 
    --     2. Debe comprobar que no se duplica
    PROCEDURE CREAR_FACTURA (p_cod_factura IN NUMBER, p_fecha IN DATE, p_descripcion IN VARCHAR2) IS
        v_count NUMBER;
    BEGIN
        -- Verificar si ya existe una factura con el mismo código
        SELECT COUNT(*)
        INTO v_count
        FROM FACTURAS
        WHERE cod_factura = p_cod_factura;

        -- Si la factura ya existe, lanzar una excepción
        IF v_count > 0 THEN
            RAISE_APPLICATION_ERROR(-20001, 'Ya existe una factura con el código indicado.');
        END IF;

        -- Insertar la nueva factura si no existe duplicado
        INSERT INTO FACTURAS (cod_factura, Fecha, Descripcion)
        VALUES (p_cod_factura, p_fecha, p_descripcion);

        -- Confirmar la transacción
        COMMIT;

        -- Mostrar mensaje de éxito
        DBMS_OUTPUT.PUT_LINE('Factura creada exitosamente.');
    EXCEPTION
        WHEN OTHERS THEN
            -- Manejar cualquier error
            ROLLBACK;
            DBMS_OUTPUT.PUT_LINE('Error al crear la factura: ' || SQLERRM);
    END CREAR_FACTURA;


    -- ii. ELIMINAR_FACTURA (cod_factura). 
    --     1. Debe borrar la factura indicada en el parámetro
    --     2. Debe borrar también las líneas de facturas asociadas en la tabla LINEAS_FACTURA.
    PROCEDURE ELIMINAR_FACTURA (p_cod_factura IN NUMBER) IS
    BEGIN
        -- Borrar las líneas de factura asociadas
        DELETE FROM LINEAS_FACTURAS
        WHERE COD_FACTURA = p_cod_factura;

        -- Borrar la factura
        DELETE FROM FACTURAS
        WHERE COD_FACTURA = p_cod_factura;

        -- Confirmar la transacción
        COMMIT;

        -- Mostrar mensaje de éxito
        DBMS_OUTPUT.PUT_LINE('Factura y líneas de factura asociadas eliminadas exitosamente.');
    EXCEPTION
        WHEN OTHERS THEN
            -- Manejar cualquier error
            ROLLBACK;
            DBMS_OUTPUT.PUT_LINE('Error al eliminar la factura y sus líneas de factura asociadas: ' || SQLERRM);
    END ELIMINAR_FACTURA;

    PROCEDURE MOD_DESCRI (p_cod_factura IN NUMBER, p_nueva_descripcion IN VARCHAR2) IS
    BEGIN
        -- Actualizar la descripción de la factura
        UPDATE FACTURAS
        SET Descripcion = p_nueva_descripcion
        WHERE cod_factura = p_cod_factura;

        -- Confirmar la transacción
        COMMIT;

        -- Mostrar mensaje de éxito
        DBMS_OUTPUT.PUT_LINE('Descripción de la factura modificada exitosamente.');
    EXCEPTION
        WHEN OTHERS THEN
            -- Manejar cualquier error
            ROLLBACK;
            DBMS_OUTPUT.PUT_LINE('Error al modificar la descripción de la factura: ' || SQLERRM);
    END MOD_DESCRI;


    -- iv. MOD_FECHA (COD_FACTURA,FECHA).
    --     1. Debe modificar la descripción de la factura que tenga el código del parámetro con la nueva fecha
    PROCEDURE MOD_FECHA (p_cod_factura IN NUMBER, p_nueva_fecha IN DATE) IS
    BEGIN
        -- Actualizar la fecha de la factura
        UPDATE FACTURAS
        SET Fecha = p_nueva_fecha
        WHERE cod_factura = p_cod_factura;

        -- Confirmar la transacción
        COMMIT;

        -- Mostrar mensaje de éxito
        DBMS_OUTPUT.PUT_LINE('Fecha de la factura modificada exitosamente.');
    EXCEPTION
        WHEN OTHERS THEN
            -- Manejar cualquier error
            ROLLBACK;
            DBMS_OUTPUT.PUT_LINE('Error al modificar la fecha de la factura: ' || SQLERRM);
    END MOD_FECHA;

    -- FUNCIONES 
    --     i. NUM_FACTURAS(FECHA_INICIO,FECHA_FIN). 
--          1. Devuelve el número de facturas que hay entre esas fechas
    FUNCTION NUM_FACTURAS (p_fecha_inicio IN DATE, p_fecha_fin IN DATE) RETURN NUMBER IS
        v_num_facturas NUMBER;
    BEGIN
        -- Contar el número de facturas entre las fechas especificadas
        SELECT COUNT(*)
        INTO v_num_facturas
        FROM FACTURAS
        WHERE Fecha BETWEEN p_fecha_inicio AND p_fecha_fin;

        RETURN v_num_facturas;
    EXCEPTION
        WHEN OTHERS THEN
            -- Manejar cualquier error
            DBMS_OUTPUT.PUT_LINE('Error al calcular el número de facturas: ' || SQLERRM);
            RETURN -1; -- Valor de retorno indicando error
    END NUM_FACTURAS;


    --  ii. TOTAL_FACTURA(COD_FACTURA.) 
    --     1. Devuelve el total de la factura con ese código. Debe hacer el sumatorio de “pvp*unidades” 
    --     de las líneas de esa factura en la tabla LINEAS_FACTURA
    FUNCTION TOTAL_FACTURA (p_cod_factura IN NUMBER) RETURN NUMBER IS
        v_total NUMBER := 0;
    BEGIN
        -- Calcular el total de la factura sumando el producto del precio por unidad
        -- de cada línea de la factura
        SELECT SUM(PVP * UNIDADES)
        INTO v_total
        FROM LINEAS_FACTURAS
        WHERE COD_FACTURA = p_cod_factura;

        RETURN v_total;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            -- Manejar el caso donde no se encuentran líneas para el código de factura dado
            DBMS_OUTPUT.PUT_LINE('No se encontraron líneas de factura para el código especificado.');
            RETURN NULL; -- Indicar que no se encontraron datos

        WHEN OTHERS THEN
            -- Manejar cualquier otro error
            DBMS_OUTPUT.PUT_LINE('Error al calcular el total de la factura: ' || SQLERRM);
            RETURN -1; -- Valor de retorno indicando error
    END TOTAL_FACTURA;
END FACTURAS_PKG;
/




-- Ejecutar los procedimientos del paquete FACTURAS_PKG --

-- Crear una nueva factura
BEGIN
    FACTURAS_PKG.CREAR_FACTURA(6, TO_DATE('2024-05-10', 'YYYY-MM-DD'), 'Compra de muebles');
END;
/

-- Modificar la descripción de una factura existente
BEGIN
    FACTURAS_PKG.MOD_DESCRI(6, 'Compra de muebles para la oficina');
END;
/

-- Modificar la fecha de una factura existente
BEGIN
    FACTURAS_PKG.MOD_FECHA(6, TO_DATE('2024-05-15', 'YYYY-MM-DD'));
END;
/

-- Eliminar una factura
BEGIN
    FACTURAS_PKG.ELIMINAR_FACTURA(6);
END;
/

-- Calcular el número de facturas entre dos fechas
DECLARE
    num_facturas NUMBER;
BEGIN
    num_facturas := FACTURAS_PKG.NUM_FACTURAS(TO_DATE('2024-04-01', 'YYYY-MM-DD'), TO_DATE('2024-05-31', 'YYYY-MM-DD'));
    DBMS_OUTPUT.PUT_LINE('Número de facturas entre las fechas especificadas: ' || num_facturas);
END;
/

-- Calcular el total de una factura
DECLARE
    total_factura NUMBER;
BEGIN
    total_factura := FACTURAS_PKG.TOTAL_FACTURA(1); -- Suponiendo que quieres calcular el total de la factura con el código 1
    IF total_factura IS NOT NULL THEN
        DBMS_OUTPUT.PUT_LINE('Total de la factura: ' || total_factura);
    END IF;
END;
/
