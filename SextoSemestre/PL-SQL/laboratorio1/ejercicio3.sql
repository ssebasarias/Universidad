-- 3. Averiguar el nombre del día que naciste, por ejemplo "Martes"

DECLARE
  dia NUMBER(2) := 26;
  mes NUMBER(2) := 07;
  anio NUMBER(4) := 2001;
  dia_semana NUMBER(1);

BEGIN
  -- Cálculo del día de la semana
  dia_semana := TO_NUMBER(TO_CHAR(TO_DATE(dia || '-' || mes || '-' || anio, 'DD-MM-YYYY'), 'D'));

  -- Visualización del resultado
  DBMS_OUTPUT.PUT_LINE('Usted nació un ' || CASE dia_semana
    WHEN 1 THEN 'Domingo'
    WHEN 2 THEN 'Lunes'
    WHEN 3 THEN 'Martes'
    WHEN 4 THEN 'Miércoles'
    WHEN 5 THEN 'Jueves'
    WHEN 6 THEN 'Viernes'
    ELSE 'Sábado'
  END || '.');
END;


