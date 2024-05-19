-- 1. Queremos calcular el impuesto de un producto 
-- a. El impuesto será del 21%. Le debemos poner en una constante 
-- b. Creamos una variable de tipo number (5,2) para poner el precio del producto
-- c. Creamos otra variable para el resultado. Le decimos que es del mismo tipo 
-- (type) que la anterior 

DECLARE
  IVA CONSTANT NUMBER := 21;
  precio_producto NUMBER(5,2) := 230.30;
  impuesto precio_producto%TYPE;

-- d. Hacemos el cálculo y visualizamos el resultado
BEGIN
  impuesto := precio_producto * (IVA / 100);

  DBMS_OUTPUT.PUT_LINE('El precio del producto es: ' || precio_producto);
  DBMS_OUTPUT.PUT_LINE('impuesto del producto es: ' || impuesto);

END;