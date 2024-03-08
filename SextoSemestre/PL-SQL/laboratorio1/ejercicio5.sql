-- 5. Práctica 1 - bucles
-- a. Vamos a crear la tabla de multiplicar del 1 al 10, con los tres tipos de bucles: 
-- LOOP, WHILE y FOR

-- LOOP
DECLARE
  numero NUMBER(2);
BEGIN
  FOR numero IN 1..10 LOOP
    DBMS_OUTPUT.PUT_LINE(numero || ' x ' || numero || ' = ' || numero * numero);
  END LOOP;
END;
/

-- WHILE
DECLARE
  numero NUMBER(2);
BEGIN
  numero := 1;
  WHILE numero <= 10 LOOP
    DBMS_OUTPUT.PUT_LINE(numero || ' x ' || numero || ' = ' || numero * numero);
    numero := numero + 1;
  END LOOP;
END;
/

-- FOR
DECLARE
  numero NUMBER(2);
BEGIN
  FOR numero IN 1..10 LOOP
    DBMS_OUTPUT.PUT_LINE(numero || ' x ' || numero || ' = ' || numero * numero);
  END LOOP;
END;
/
