-- PAQUETE LINEA_FACTURAS
--     a. PROCEDIMIENTOS 
--         i. CREAR_LINEA (COD_FACTURA, COD_PRODUCTO, UNIDADES, 
--         FECHA) 
--             1. Procedimiento para insertar una línea de Factura
--             2. Debe comprobar que existe ya la factura antes de insertar el 
--             registro.
--             3. También debemos comprobar que existe el producto en la 
--             tabla de PRODUCTOS.
--             4. El PVP debemos seleccionarlo de la tabla PRODUCTOS
--        ii. ELIMINAR_LINEA (cod_factura, COD_PRODUCTO )
--             1. Eliminar la línea con esa clave primaria
    -- iii. MOD_PRODUCTO(COD_FACTURA,COD_PRODUCTO,PARAMETRO) 
    --     1. Se trata de 2 métodos sobrecargados, es decir el segundo 
    --     parámetro debe admitir los siguientes valores:
    --         a. MOD_PRODUCTO(COD_FACTURA,COD_PRODUCTO, 
    --         UNIDADES)
    --         b. MOD_PRODUCTO(COD_FACTURA,COD_PRODUCTO, 
    --         FECHA) 
    --     2. Por tanto, debe modificar o bien unidades si se le pasa un 
    --     NUMBER o bien la fecha si se le pasa un DATE

-- b. FUNCIONES
--     i. NUM_LINEAS(COD_FACTURA)
--         1. Devuelve el número de líneas de la factura
-- c. TRIGGERS
--     i. Triggers de tipo sentencia
--         1. Creamos 2 triggers de tipo SENTENCIA, uno para la tabla 
--         FACTURAS y otro para la tabla LINEAS_FACTURA 
--         2. Cada cambio en alguna de las tablas (Insert, update, delete), 
--         debe generar una entrada en la tabla CONTROL_LOG con los 
--         datos siguientes: 
--             a. Tabla (FACTURAS O LONEAS_FACTURA) 
--             b. Fecha → usamos la función SYSDATE
--             c. Usuario que lo ha realizado → función USER 
--             d. Operación realizada (I-U-D)
-- ii. Trigger de tipo fila
--     1. La columna TOTAL_VENDIDO, de la tabla PRODUCTOS 
--     mantiene el total de ventas de un determinado producto.
--     2. PARA controlaro, creamos un Trigger de tipo fila sobre la tabla 
--     LINEAS_FACTURA, de forma que cada vez que se añada, 
--     cambie o borre una línea se actualice en la tabla PRODUCTOS 
--     la columna TOTAL_VENDIDO. 
--     3. Si se inserta una nueva línea con ese producto, se debe añadir 
--     el total al campo. 
--     4. Si se borra la línea debemos restar el total 
--     5. Si se modifica, debemos comprobar si el valor antiguo era 
--     superior al nuevo y sumamos o restamos dependiendo del 
--     resultado


CREATE OR REPLACE PACKAGE LINEA_FACTURAS AS
    PROCEDURE CREAR_LINEA (
        p_COD_FACTURA IN LINEAS_FACTURAS.COD_FACTURA%TYPE,
        p_COD_PRODUCTO IN LINEAS_FACTURAS.COD_PRODUCTO%TYPE,
        p_UNIDADES IN LINEAS_FACTURAS.UNIDADES%TYPE,
        p_FECHA IN LINEAS_FACTURAS.FECHA%TYPE
    );
    
    PROCEDURE ELIMINAR_LINEA (
        p_COD_FACTURA IN LINEAS_FACTURAS.COD_FACTURA%TYPE,
        p_COD_PRODUCTO IN LINEAS_FACTURAS.COD_PRODUCTO%TYPE
    );
    
    PROCEDURE MOD_PRODUCTO (
        p_COD_FACTURA IN LINEAS_FACTURAS.COD_FACTURA%TYPE,
        p_COD_PRODUCTO IN LINEAS_FACTURAS.COD_PRODUCTO%TYPE,
        p_PARAMETRO IN NUMBER
    );
    
    PROCEDURE MOD_FECHA (
        p_COD_FACTURA IN LINEAS_FACTURAS.COD_FACTURA%TYPE,
        p_COD_PRODUCTO IN LINEAS_FACTURAS.COD_PRODUCTO%TYPE,
        p_PARAMETRO IN DATE
    );
    
    FUNCTION NUM_LINEAS (
        p_COD_FACTURA IN LINEAS_FACTURAS.COD_FACTURA%TYPE
    ) RETURN NUMBER;
    
END LINEA_FACTURAS;
/

CREATE OR REPLACE PACKAGE BODY LINEA_FACTURAS AS
    PROCEDURE CREAR_LINEA (
        p_COD_FACTURA IN LINEAS_FACTURAS.COD_FACTURA%TYPE,
        p_COD_PRODUCTO IN LINEAS_FACTURAS.COD_PRODUCTO%TYPE,
        p_UNIDADES IN LINEAS_FACTURAS.UNIDADES%TYPE,
        p_FECHA IN LINEAS_FACTURAS.FECHA%TYPE
    )
    AS
        v_PVP PRODUCTOS.PVP%TYPE;
    BEGIN
        -- Comprobar si la factura existe
        IF NOT EXISTS (SELECT 1 FROM FACTURAS WHERE COD_FACTURA = p_COD_FACTURA) THEN
            RAISE_APPLICATION_ERROR(-20001, 'La factura especificada no existe.');
        END IF;

        -- Comprobar si el producto existe
        IF NOT EXISTS (SELECT 1 FROM PRODUCTOS WHERE COD_PRODUCTO = p_COD_PRODUCTO) THEN
            RAISE_APPLICATION_ERROR(-20002, 'El producto especificado no existe.');
        END IF;

        -- Obtener el PVP del producto
        SELECT PVP INTO v_PVP FROM PRODUCTOS WHERE COD_PRODUCTO = p_COD_PRODUCTO;

        -- Insertar la línea de factura
        INSERT INTO LINEAS_FACTURAS (COD_FACTURA, COD_PRODUCTO, PVP, UNIDADES, FECHA)
        VALUES (p_COD_FACTURA, p_COD_PRODUCTO, v_PVP, p_UNIDADES, p_FECHA);

        -- Registrar la operación en el control de log
        INSERT INTO CONTROL_LOG (COD_EMPLEADO, FECHA, TABLA_AFECTADA, COD_OPERACION)
        VALUES (1, SYSDATE, 'LINEAS_FACTURAS', 'I');

        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END CREAR_LINEA;

    PROCEDURE ELIMINAR_LINEA (
        p_COD_FACTURA IN LINEAS_FACTURAS.COD_FACTURA%TYPE,
        p_COD_PRODUCTO IN LINEAS_FACTURAS.COD_PRODUCTO%TYPE
    )
    AS
    BEGIN
        -- Eliminar la línea de factura
        DELETE FROM LINEAS_FACTURAS
        WHERE COD_FACTURA = p_COD_FACTURA
        AND COD_PRODUCTO = p_COD_PRODUCTO;

        -- Registrar la operación en el control de log
        INSERT INTO CONTROL_LOG (COD_EMPLEADO, FECHA, TABLA_AFECTADA, COD_OPERACION)
        VALUES (1, SYSDATE, 'LINEAS_FACTURAS', 'D');

        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END ELIMINAR_LINEA;

    PROCEDURE MOD_PRODUCTO (
        p_COD_FACTURA IN LINEAS_FACTURAS.COD_FACTURA%TYPE,
        p_COD_PRODUCTO IN LINEAS_FACTURAS.COD_PRODUCTO%TYPE,
        p_PARAMETRO IN NUMBER
    )
    AS
    BEGIN
        -- Modificar las unidades de la línea de factura
        UPDATE LINEAS_FACTURAS
        SET UNIDADES = p_PARAMETRO
        WHERE COD_FACTURA = p_COD_FACTURA
        AND COD_PRODUCTO = p_COD_PRODUCTO;

        -- Registrar la operación en el control de log
        INSERT INTO CONTROL_LOG (COD_EMPLEADO, FECHA, TABLA_AFECTADA, COD_OPERACION)
        VALUES (1, SYSDATE, 'LINEAS_FACTURAS', 'U');

        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END MOD_PRODUCTO;

    PROCEDURE MOD_FECHA (
        p_COD_FACTURA IN LINEAS_FACTURAS.COD_FACTURA%TYPE,
        p_COD_PRODUCTO IN LINEAS_FACTURAS.COD_PRODUCTO%TYPE,
        p_PARAMETRO IN DATE
    )
    AS
    BEGIN
        -- Modificar la fecha de la línea de factura
        UPDATE LINEAS_FACTURAS
        SET FECHA = p_PARAMETRO
        WHERE COD_FACTURA = p_COD_FACTURA
        AND COD_PRODUCTO = p_COD_PRODUCTO;

        -- Registrar la operación en el control de log
        INSERT INTO CONTROL_LOG (COD_EMPLEADO, FECHA, TABLA_AFECTADA, COD_OPERACION)
        VALUES (1, SYSDATE, 'LINEAS_FACTURAS', 'U');

        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            RAISE;
    END MOD_FECHA;

    FUNCTION NUM_LINEAS (
        p_COD_FACTURA IN LINEAS_FACTURAS.COD_FACTURA%TYPE
    ) RETURN NUMBER
    AS
        v_NUMERO_LINEAS NUMBER;
    BEGIN
        -- Contar el número de líneas de la factura
        SELECT COUNT(*)
        INTO v_NUMERO_LINEAS
        FROM LINEAS_FACTURAS
        WHERE COD_FACTURA = p_COD_FACTURA;

        RETURN v_NUMERO_LINEAS;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RETURN 0; -- Devuelve 0 si no se encuentra ninguna línea para la factura especificada
        WHEN OTHERS THEN
            RAISE;
    END NUM_LINEAS;

END LINEA_FACTURAS;
/

CREATE OR REPLACE TRIGGER TR_FACTURAS_CONTROL_LOG
AFTER INSERT OR UPDATE OR DELETE ON FACTURAS
FOR EACH ROW
DECLARE
    v_COD_OPERACION CHAR(1);
BEGIN
    -- Determinar el código de operación basado en el tipo de evento del trigger
    IF INSERTING THEN
        v_COD_OPERACION := 'I';
    ELSIF UPDATING THEN
        v_COD_OPERACION := 'U';
    ELSE
        v_COD_OPERACION := 'D';
    END IF;

    -- Insertar un registro en la tabla CONTROL_LOG
    INSERT INTO CONTROL_LOG (COD_EMPLEADO, FECHA, TABLA_AFECTADA, COD_OPERACION)
    VALUES (:NEW.COD_EMPLEADO, SYSDATE, 'FACTURAS', v_COD_OPERACION);
END;
/
