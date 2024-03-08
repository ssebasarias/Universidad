-- 8. Práctica 4-bucles
-- a. Debemos crear una variable llamada NOMBRE
-- b. Debemos pintar tantos asteriscos como letras tenga el nombre. Usamos un 
-- bucle FOR
-- c. Por ejemplo, Alberto → ******* 
-- d. por ejemplo, Pedro → ***** 5. 

DECLARE
  nombre VARCHAR2(50);
  longitud NUMBER;
BEGIN
  -- Ingreso del nombre
  DBMS_OUTPUT.PUT_LINE('Ingrese su nombre: ');
  nombre := DBMS_INPUT.GET_LINE;

  -- Obtención de la longitud del nombre
  longitud := LENGTH(nombre);

  -- Impresión de asteriscos
  DBMS_OUTPUT.PUT_LINE('Nombre: ' || nombre);
  DBMS_OUTPUT.PUT_LINE('Longitud: ' || longitud);
  FOR i IN 1..longitud LOOP
    DBMS_OUTPUT.PUT('*');
  END LOOP;

END;
/

-- e. Práctica 5 – bucles
-- i. Creamos dos variables numéricas, "inicio y fin" 
-- ii. Las inicializamos con algún valor: 
-- iii. Debemos sacar los números que sean múltiplos de 4 de ese rango

DECLARE
  inicio NUMBER;
  fin NUMBER;
  numero NUMBER;
BEGIN
  -- Ingreso del rango
  DBMS_OUTPUT.PUT_LINE('Ingrese el valor inicial: ');
  inicio := TO_NUMBER(DBMS_INPUT.GET_LINE);

  DBMS_OUTPUT.PUT_LINE('Ingrese el valor final: ');
  fin := TO_NUMBER(DBMS_INPUT.GET_LINE);

  -- Impresión de los múltiplos de 4
  DBMS_OUTPUT.PUT_LINE('Múltiplos de 4 entre ' || inicio || ' y ' || fin);
  FOR numero IN inicio..fin LOOP
    IF MOD(numero, 4) = 0 THEN
      DBMS_OUTPUT.PUT_LINE(numero);
    END IF;
  END LOOP;

END;
/
