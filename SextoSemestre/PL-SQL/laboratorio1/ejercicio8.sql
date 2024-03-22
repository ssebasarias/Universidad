-- 8. Práctica 4-bucles
-- a. Debemos crear una variable llamada NOMBRE
-- b. Debemos pintar tantos asteriscos como letras tenga el nombre. Usamos un 
-- bucle FOR
-- c. Por ejemplo, Alberto → ******* 
-- d. por ejemplo, Pedro → ***** 5. 

DECLARE
  nombre VARCHAR2(50) := 'Sebastian';
  longitud NUMBER;
  caracteres VARCHAR2(50);
BEGIN
  longitud := LENGTH(nombre);

  DBMS_OUTPUT.PUT_LINE('Nombre: ' || nombre);
  DBMS_OUTPUT.PUT_LINE('Numero de caracteres: ' || longitud);
  FOR i IN 1..longitud LOOP
  caracteres := caracteres || '*'
  END LOOP;
  DBMS_OUTPUT.PUT_LINE(caracteres);
END;

-- e. Práctica 5 – bucles
-- i. Creamos dos variables numéricas, "inicio y fin" 
-- ii. Las inicializamos con algún valor: 
-- iii. Debemos sacar los números que sean múltiplos de 4 de ese rango

DECLARE
  inicio NUMBER := 1;
  fin NUMBER := 15;
  numero NUMBER;
BEGIN
  DBMS_OUTPUT.PUT_LINE('Múltiplos de 4 entre ' || inicio || ' y ' || fin);
  FOR numero IN inicio..fin LOOP
    IF MOD(numero, 4) = 0 THEN
      DBMS_OUTPUT.PUT_LINE(numero);
    END IF;
  END LOOP;

END;
