-- 6. Práctica 2-bucles •
-- a. Crear una variable llamada TEXTO de tipo VARCHAR2(100).
-- b. Poner alguna frase
-- c. Mediante un bucle, escribir la frase al revés, Usamos el bucle WHILE

DECLARE
  texto VARCHAR2(100) := 'Wasauki, no entregaste tu papeleo anoche';
  posicion NUMBER;
  caracter VARCHAR2(1);
  texto_invertido VARCHAR2(100);
BEGIN
  texto_invertido := '';
  posicion := LENGTH(texto);

  WHILE posicion >= 1 LOOP
    caracter := SUBSTR(texto, posicion, 1);

    texto_invertido := texto_invertido || caracter;

    posicion := posicion - 1;
  END LOOP;

  DBMS_OUTPUT.PUT_LINE('La frase al revés es: ' || texto_invertido);
END;
