-- 3. Averiguar el nombre del día que naciste, por ejemplo "Martes"

DECLARE
  dia NUMBER(2);
  mes NUMBER(2);
  anio NUMBER(4);
  dia_semana NUMBER(1);

BEGIN
  DBMS_OUTPUT.PUT_LINE('Ingrese el día de su nacimiento: ');
  dia := TO_NUMBER(DBMS_INPUT.GET_LINE);

  DBMS_OUTPUT.PUT_LINE('Ingrese el mes de su nacimiento (1-12): ');
  mes := TO_NUMBER(DBMS_INPUT.GET_LINE);

  DBMS_OUTPUT.PUT_LINE('Ingrese el año de su nacimiento: ');
  anio := TO_NUMBER(DBMS_INPUT.GET_LINE);

  -- Cálculo del día de la semana
  dia_semana := MOD(1461 * (anio + 4800 + (mes - 14) // 12) / 4 + 367 * (mes - 2 - (mes - 14) // 12 * 12) / 12 - 3 * ((anio + 4900 + (mes - 14) // 12) / 100) + dia - 32045, 7) + 1;

  -- Visualización del resultado
  DBMS_OUTPUT.PUT_LINE('Usted nació un ' || CASE dia_semana
    WHEN 1 THEN 'Lunes'
    WHEN 2 THEN 'Martes'
    WHEN 3 THEN 'Miércoles'
    WHEN 4 THEN 'Jueves'
    WHEN 5 THEN 'Viernes'
    WHEN 6 THEN 'Sábado'
    ELSE 'Domingo'
  END || '.');
EXCEPTION
  WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('Error inesperado: ' || SQLCODE || ' - ' || SQLERRM);
END;
/
