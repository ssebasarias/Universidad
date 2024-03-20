-- 4. Crear una variable CHAR(1) denominada TIPO_PRODUCTO. 
-- a. Poner un valor entre "A" Y "E" 
-- b. Visualizar el siguiente resultado según el tipo de producto 
-- i. 'A' --> Electronica
-- ii. 'B' --> Informática
-- iii. 'C' --> Ropa
-- iv. 'D' --> Música 
-- v. 'E' --> Libros 
-- vi. Cualquier otro valor debe visualizar "El código es incorrecto


DECLARE
  tipo_producto CHAR(1);

BEGIN
  DBMS_OUTPUT.PUT_LINE('Ingrese el código del producto (A-E): ');
  tipo_producto := DBMS_INPUT.GET_LINE;

  IF tipo_producto IN ('A', 'B', 'C', 'D', 'E') THEN
    CASE tipo_producto
      WHEN 'A' THEN DBMS_OUTPUT.PUT_LINE('El producto es de tipo: Electronica');
      WHEN 'B' THEN DBMS_OUTPUT.PUT_LINE('El producto es de tipo: Informática');
      WHEN 'C' THEN DBMS_OUTPUT.PUT_LINE('El producto es de tipo: Ropa');
      WHEN 'D' THEN DBMS_OUTPUT.PUT_LINE('El producto es de tipo: Música');
      ELSE DBMS_OUTPUT.PUT_LINE('El producto es de tipo: Libros');
    END CASE;
  ELSE
    DBMS_OUTPUT.PUT_LINE('El código del producto es incorrecto.');
  END IF;
EXCEPTION
  WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('Error inesperado: ' || SQLCODE || ' - ' || SQLERRM);
END;
/
