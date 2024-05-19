-- 9. Creamos un TYPE RECORD que tenga las siguientes columnas 
-- NAME VARCHAR2(100), 
-- SAL EMPLOYEES.SALARY%TYPE,
-- COD_DEPT EMPLOYEES.DEPARTMENT_ID%TYPE); 
CREATE TYPE EMPLOYEE_RECORD AS OBJECT (
  NAME VARCHAR2(100),
  SAL EMPLOYEES.SALARY%TYPE,
  COD_DEPT EMPLOYEES.DEPARTMENT_ID%TYPE
);

-- a. Creamos un TYPE TABLE basado en el RECORD anterior
CREATE TYPE EMPLOYEES_TABLE AS TABLE OF EMPLOYEE_RECORD;

-- b. Mediante un bucle cargamos en la colección los empleados. El campo NAME 
-- debe contener FIRST_NAME y LAST_NAME concatenado. 
DECLARE
  emp_list EMPLOYEES_TABLE := EMPLOYEES_TABLE(); -- Declaración e inicialización de la colección
BEGIN
  FOR emp IN (SELECT FIRST_NAME || ' ' || LAST_NAME AS FULL_NAME, SALARY, DEPARTMENT_ID FROM EMPLOYEES) LOOP
    emp_list.EXTEND; -- Extendemos la colección en cada iteración
    emp_list(emp_list.LAST) := EMPLOYEE_RECORD(emp.FULL_NAME, emp.SALARY, emp.DEPARTMENT_ID); -- Asignamos los valores al registro de empleado y lo agregamos a la colección
  END LOOP;
END;

-- c. Para cargar las filas y siguiendo un ejemplo parecido que hemos visto en el 
-- vídeo usamos el EMPLOYEE_ID que va de 100 a 206 
DECLARE
  empleados EMPLOYEES_TABLE := EMPLOYEES_TABLE(); -- Declaración e inicialización de la colección de empleados
  empleado EMPLOYEE_RECORD; -- Declaración de una variable de tipo EMPLOYEE_RECORD
  i NUMBER;
BEGIN
  FOR i IN 100..206 LOOP
    SELECT first_name || ' ' || last_name, salary, department_id
    INTO empleado.NAME, empleado.SAL, empleado.COD_DEPT
    FROM employees
    WHERE employee_id = i;

    empleados.EXTEND; -- Extendemos la colección en cada iteración
    empleados(empleados.LAST) := empleado; -- Asignamos el registro del empleado a la última posición de la colección
  END LOOP;
END;


-- d. A partir de este momento y ya con la colección cargada, hacemos las 
-- siguientes operaciones, usando métodos de la colección. 
-- i. Visualizamos toda la colección 
-- ii. Visualizamos el primer empleado
-- iii. Visualizamos el último empleado 
-- iv. Visualizamos el número de empleados 
-- v. Borramos los empleados que ganan menos de 7000 y visualizamos de 
-- nuevo la colección 
-- vi. Volvemos a visualizar el número de empleados para ver cuantos se 
-- han borrado

FOR i IN 1..empleados.COUNT LOOP
  DBMS_OUTPUT.PUT_LINE('Empleado ' || i || ':');
  DBMS_OUTPUT.PUT_LINE('  Nombre: ' || empleados(i).NAME);
  DBMS_OUTPUT.PUT_LINE('  Salario: ' || empleados(i).SAL);
  DBMS_OUTPUT.PUT_LINE('  Código de departamento: ' || empleados(i).COD_DEPT);
END LOOP;

-- Visualización del primer empleado
DBMS_OUTPUT.PUT_LINE('Primer empleado:');
DBMS_OUTPUT.PUT_LINE('  Nombre: ' || empleados(1).NAME);
DBMS_OUTPUT.PUT_LINE('  Salario: ' || empleados(1).SAL);
DBMS_OUTPUT.PUT_LINE('  Código de departamento: ' || empleados(1).COD_DEPT);

-- Visualización del último empleado
DBMS_OUTPUT.PUT_LINE('Último empleado:');
DBMS_OUTPUT.PUT_LINE('  Nombre: ' || empleados(empleados.COUNT).NAME);
DBMS_OUTPUT.PUT_LINE('  Salario: ' || empleados(empleados.COUNT).SAL);
DBMS_OUTPUT.PUT_LINE('  Código de departamento: ' || empleados(empleados.COUNT).COD_DEPT);

-- Visualización del número de empleados
DBMS_OUTPUT.PUT_LINE('Número de empleados: ' || empleados.COUNT);

-- Borrar empleados con salario menor a 7000
FOR i IN empleados.COUNT REVERSE LOOP
  IF empleados(i).SAL < 7000 THEN
    empleados.DELETE(i);
  END IF;
END LOOP;

-- Visualización de la colección después de eliminar empleados
DBMS_OUTPUT.PUT_LINE('Empleados después de eliminar:');
FOR i IN 1..empleados.COUNT LOOP
  DBMS_OUTPUT.PUT_LINE('Empleado ' || i || ':');
  DBMS_OUTPUT.PUT_LINE('  Nombre: ' || empleados(i).NAME);
  DBMS_OUTPUT.PUT_LINE('  Salario: ' || empleados(i).SAL);
  DBMS_OUTPUT.PUT_LINE('  Código de departamento: ' || empleados(i).COD_DEPT);
END LOOP;

-- Visualización del nuevo número de empleados
DBMS_OUTPUT.PUT_LINE('Nuevo número de empleados: ' || empleados.COUNT);
