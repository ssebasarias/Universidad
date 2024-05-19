-- Crear una función que tenga como parámetro un número de 
-- departamento y que devuelve la suma de los salarios de dicho 
-- departamento. La imprimimos por pantalla.
-- a. Si el departamento no existe debemos generar una excepción con dicho 
-- mensaje
-- b. Si el departamento existe, pero no hay empleados dentro, también debemos 
-- generar una excepción para indicarlo


CREATE OR REPLACE FUNCTION calcular_salario_departamento(p_department_id IN NUMBER) RETURN NUMBER AS
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

  RETURN v_total_salario;
END;
/



DECLARE
  v_resultado NUMBER;
BEGIN
  v_resultado := calcular_salario_departamento(p_department_id => 20);
  DBMS_OUTPUT.PUT_LINE('Salario total: ' || v_resultado);
END;
