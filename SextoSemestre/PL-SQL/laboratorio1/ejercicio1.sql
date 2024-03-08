-- 1. Queremos calcular el impuesto de un producto 
-- a. El impuesto será del 21%. Le debemos poner en una constante 
-- b. Creamos una variable de tipo number (5,2) para poner el precio del producto
-- c. Creamos otra variable para el resultado. Le decimos que es del mismo tipo 
-- (type) que la anterior 
-- d. Hacemos el cálculo y visualizamos el resultado

DECLARE
  -- Constante para el porcentaje de impuesto
  const IVA NUMBER := 21;

  -- Variable para el precio del producto
  precio_producto NUMBER(5,2);

  -- Variable para el resultado del impuesto
  impuesto NUMBER(5,2);

BEGIN
  -- Ingreso del precio del producto
  BEGIN
    DBMS_OUTPUT.PUT_LINE('Ingrese el precio del producto: ');
    precio_producto := TO_NUMBER(DBMS_INPUT.GET_LINE);
  EXCEPTION
    WHEN INVALID_NUMBER THEN
      RAISE_APPLICATION_ERROR(-20001, 'Valor no numérico ingresado.');
  END;

  -- Cálculo del impuesto
  impuesto := precio_producto * IVA / 100;

  -- Visualización del resultado
  DBMS_OUTPUT.PUT_LINE('El impuesto del producto es: ' || impuesto);

EXCEPTION
  WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('Error inesperado: ' || SQLCODE || ' - ' || SQLERRM);
END;
/
