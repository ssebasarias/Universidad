-- 6. Práctica 2-bucles •
-- a. Crear una variable llamada TEXTO de tipo VARCHAR2(100).
-- b. Poner alguna frase
-- c. Mediante un bucle, escribir la frase al revés, Usamos el bucle WHILE

DECLARE
  texto VARCHAR2(100);
  longitud NUMBER;
  posicion NUMBER;
  caracter VARCHAR2(1);
  texto_invertido VARCHAR2(100);
BEGIN
  DBMS_OUTPUT.PUT_LINE('Ingrese una frase: ');
  texto := DBMS_INPUT.GET_LINE;

  longitud := LENGTH(texto);

  texto_invertido := '';

  -- Bucle para recorrer la frase en orden inverso
  posicion := longitud;
  WHILE posicion >= 1 LOOP
    -- Extracción del caracter en la posición actual
    caracter := SUBSTR(texto, posicion, 1);

    -- Concatenación del caracter al texto invertido
    texto_invertido := texto_invertido || caracter;

    -- Decremento de la posición
    posicion := posicion - 1;
  END LOOP;

  DBMS_OUTPUT.PUT_LINE('La frase al revés es: ' || texto_invertido);
EXCEPTION
  WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('Error inesperado: ' || SQLCODE || ' - ' || SQLERRM);
END;
/
