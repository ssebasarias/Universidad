-- 7. Práctica 3 - bucles
-- a. Usando la práctica anterior, si en el texto aparece el carácter "x" debe salir del 
-- bucle. Es igual en mayúsculas o minúsculas. 
-- b. Debemos usar la cláusula EXIT.

DECLARE
  texto VARCHAR2(100);
  longitud NUMBER;
  posicion NUMBER;
  caracter VARCHAR2(1);
  texto_invertido VARCHAR2(100);
BEGIN
  DBMS_OUTPUT.PUT_LINE('Ingrese una frase: ');
  texto := DBMS_INPUT.GET_LINE;

  -- Obtención de la longitud de la frase
  longitud := LENGTH(texto);

  -- Inicialización de la variable para el texto invertido
  texto_invertido := '';

  -- Bucle para recorrer la frase en orden inverso
  posicion := longitud;
  WHILE posicion >= 1 LOOP
    -- Extracción del caracter en la posición actual
    caracter := SUBSTR(texto, posicion, 1);

    -- Salida del bucle si el caracter es "x" o "X"
    IF caracter IN ('x', 'X') THEN
      EXIT;
    END IF;

    -- Concatenación del caracter al texto invertido
    texto_invertido := texto_invertido || caracter;

    -- Decremento de la posición
    posicion := posicion - 1;
  END LOOP;

  -- Visualización del texto invertido
  DBMS_OUTPUT.PUT_LINE('La frase al revés hasta "x" es: ' || texto_invertido);
EXCEPTION
  WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('Error inesperado: ' || SQLCODE || ' - ' || SQLERRM);
END;
/
