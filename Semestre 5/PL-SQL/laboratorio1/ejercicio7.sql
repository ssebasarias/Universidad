-- 7. Práctica 3 - bucles
-- a. Usando la práctica anterior, si en el texto aparece el carácter "x" debe salir del 
-- bucle. Es igual en mayúsculas o minúsculas. 
-- b. Debemos usar la cláusula EXIT.

DECLARE
  texto VARCHAR2(100) := 'El profesor Utonio usó la sustancia x para crear a las chicas superpoderosas';
  posicion NUMBER;
  caracter VARCHAR2(1);
  texto_invertido VARCHAR2(100);
BEGIN
  texto_invertido := '';
  posicion := LENGTH(texto);

  WHILE posicion >= 1 LOOP
    caracter := SUBSTR(texto, posicion, 1);

-- a. Usando la práctica anterior, si en el texto aparece el carácter "x" debe salir del 
-- bucle. Es igual en mayúsculas o minúsculas. 
    IF caracter IN ('x', 'X') THEN
      EXIT; -- b. Debemos usar la cláusula EXIT.
    END IF;

    texto_invertido := texto_invertido || caracter;

    posicion := posicion - 1;
  END LOOP;

  DBMS_OUTPUT.PUT_LINE('La frase al revés es: ' || texto_invertido);
  DBMS_OUTPUT.PUT_LINE('La frase original es: ' || texto);
END;