-- 2. Visualizar iniciales de un nombre
-- a. Crea un bloque PL/SQL con tres variables VARCHAR2: 
-- i. Nombre
-- ii. apellido1
-- iii. apellido2
-- b. Debes visualizar las iniciales separadas por puntos. 
-- c. Además, siempre en mayúscula 
-- d. Por ejemplo, alberto pérez García debería aparecer--> A.P.G

DECLARE
  nombre VARCHAR2(50);
  apellido1 VARCHAR2(50);
  apellido2 VARCHAR2(50);
  iniciales VARCHAR2(50);
BEGIN
  DBMS_OUTPUT.PUT_LINE('Ingrese su nombre completo: ');
  nombre := DBMS_INPUT.GET_LINE;

  -- nombre
  iniciales := SUBSTR(nombre, 1, 1);

  -- primer apellido
  iniciales := iniciales || '.' || SUBSTR(apellido1, 1, 1);

  -- segundo apellido
  IF apellido2 IS NOT NULL THEN
    iniciales := iniciales || '.' || SUBSTR(apellido2, 1, 1);
  END IF;

  iniciales := UPPER(iniciales);

  DBMS_OUTPUT.PUT_LINE('Las iniciales son: ' || iniciales);
EXCEPTION
  WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('Error inesperado: ' || SQLCODE || ' - ' || SQLERRM);
END;
/