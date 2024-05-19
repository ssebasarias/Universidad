-- 5. Práctica 1 - bucles
-- a. Vamos a crear la tabla de multiplicar del 1 al 10, con los tres tipos de bucles: 
-- LOOP, WHILE y FOR

DECLARE
  numero NUMBER(2) := 1; -- Inicializamos numero a 1
  numero2 NUMBER(2) := 1; -- Inicializamos numero2 a 1
BEGIN
  LOOP
    EXIT WHEN numero > 10; -- Salimos del bucle cuando numero sea mayor que 10
    LOOP
      EXIT WHEN numero2 > 10; -- Salimos del bucle interno cuando numero2 sea mayor que 10
      DBMS_OUTPUT.PUT_LINE(numero || ' x ' || numero2 || ' = ' || numero * numero2);
      numero2 := numero2 + 1; -- Incrementamos numero2
    END LOOP;
    numero := numero + 1; -- Incrementamos numero
    numero2 := 1; -- Reiniciamos numero2 para el siguiente ciclo de numero
  END LOOP;
END;


-- WHILE
DECLARE
  numero NUMBER(2);
  numero2 NUMBER(2); 
BEGIN
  numero := 1;
  WHILE numero <= 10 LOOP
    numero2 := 1; 
    WHILE numero2 <= 10 LOOP
      DBMS_OUTPUT.PUT_LINE(numero || ' x ' || numero2 || ' = ' || numero * numero2);
      numero2 := numero2 + 1;
    END LOOP;
    numero := numero + 1;
  END LOOP;
END;

-- FOR
DECLARE
  numero NUMBER(2);
  numero2 NUMBER(2);
BEGIN
  FOR numero IN 1..10 LOOP
  FOR numero2 IN 1..10 LOOP
    DBMS_OUTPUT.PUT_LINE(numero || ' x ' || numero2 || ' = ' || numero * numero2);
    END LOOP;
  END LOOP;
END;
