-- Modificar el programa anterior para incluir un parámetro de tipo OUT por el que vaya 
-- el número de empleados afectados por la query. Debe ser visualizada en el programa
-- que llama a la función. De esta forma vemos que se puede usar este tipo de 
-- parámetros también en una función

CREATE OR REPLACE FUNCTION calcular_salario_departamento(
  p_department_id IN NUMBER,
  p_num_empleados OUT NUMBER
) RETURN NUMBER AS
  v_total_salario NUMBER := 0;
BEGIN
  SELECT SUM(salary) INTO v_total_salario
  FROM employees
  WHERE department_id = p_department_id;

  IF department_id IS NULL THEN
    RAISE_APPLICATION_ERROR(-20001, 'No se encontró el departamento ' || p_department_id);
  END IF;
  IF v_total_salario IS NULL THEN
    RAISE_APPLICATION_ERROR(-20001, 'No se encontraron empleados en el departamento ' || p_department_id);
  END IF;

  p_num_empleados := SQL%ROWCOUNT;

  RETURN v_total_salario;
END;
/



DECLARE
  v_department_id NUMBER := 10;
  v_total_salary NUMBER;
  v_num_empleados NUMBER;
BEGIN
  v_total_salary := calcular_salario_departamento(v_department_id, v_num_empleados);
  DBMS_OUTPUT.PUT_LINE('Total salario para el departamento ' || v_department_id || ': ' || v_total_salary);
  DBMS_OUTPUT.PUT_LINE('Número de empleados afectados: ' || v_num_empleados);
END;
/
