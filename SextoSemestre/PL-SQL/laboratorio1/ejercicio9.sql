-- 9. Creamos un TYPE RECORD que tenga las siguientes columnas 
-- NAME VARCHAR2(100), 
-- SAL EMPLOYEES.SALARY%TYPE,
-- COD_DEPT EMPLOYEES.DEPARTMENT_ID%TYPE); 
-- a. Creamos un TYPE TABLE basado en el RECORD anterior
CREATE TYPE EMPLEADO AS OBJECT (
  NOMBRE VARCHAR2(100),
  SALARIO NUMBER(10,2),
  COD_DEPARTAMENTO NUMBER(4)
);

-- b. Mediante un bucle cargamos en la colección los empleados. El campo NAME 
-- debe contener FIRST_NAME y LAST_NAME concatenado. 
CREATE TYPE TABLE_EMPLEADOS AS TABLE OF EMPLEADO;

-- c. Para cargar las filas y siguiendo un ejemplo parecido que hemos visto en el 
-- vídeo usamos el EMPLOYEE_ID que va de 100 a 206 
DECLARE
  empleados TABLE_EMPLEADOS;
  empleado EMPLEADO;
  i NUMBER;
BEGIN
  FOR i IN 100..206 LOOP
    SELECT first_name, last_name, salary, department_id
    INTO empleado.NOMBRE, empleado.SALARIO, empleado.COD_DEPARTAMENTO
    FROM employees
    WHERE employee_id = i;

    empleados.EXTEND(empleado);
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
-- Visualización de toda la colección
FOR i IN 1..empleados.COUNT LOOP
  DBMS_OUTPUT.PUT_LINE('Empleado ' || i || ':');
  DBMS_OUTPUT.PUT_LINE('  Nombre: ' || empleados(i).NOMBRE);
  DBMS_OUTPUT.PUT_LINE('  Salario: ' || empleados(i).SALARIO);
  DBMS_OUTPUT.PUT_LINE('  Código de departamento: ' || empleados(i).COD_DEPARTAMENTO);
END LOOP;

-- Visualización del primer empleado
DBMS_OUTPUT.PUT_LINE('Primer empleado:');
DBMS_OUTPUT.PUT_LINE('  Nombre: ' || empleados(1).NOMBRE);
DBMS_OUTPUT.PUT_LINE('  Salario: ' || empleados(1).SALARIO);
DBMS_OUTPUT.PUT_LINE('  Código de departamento: ' || empleados(1).COD_DEPARTAMENTO);

-- Visualización del último empleado
DBMS_OUTPUT.PUT_LINE('Último empleado:');
DBMS_OUTPUT.PUT_LINE('  Nombre: ' || empleados(empleados.COUNT).NOMBRE);
DBMS_OUTPUT.PUT_LINE('  Salario: ' || empleados(empleados.COUNT).SALARIO);
DBMS_OUTPUT.PUT_LINE('  Código de departamento: ' || empleados(empleados.COUNT).COD_DEPARTAMENTO);

-- Visualización del número de empleados
DBMS_OUTPUT.PUT_LINE('Número de empleados: ' || empleados.COUNT);

-- Borrar empleados con salario menor a 7000
FOR i IN empleados.COUNT REVERSE LOOP
  IF empleados(i).SALARIO < 7000 THEN
    empleados.DELETE(i);
  END IF;
END LOOP;

-- Visualización de la colección después de eliminar empleados
DBMS_OUTPUT.PUT_LINE('Empleados después de eliminar:');
FOR i IN 1..empleados.COUNT LOOP
  DBMS_OUTPUT.PUT_LINE('Empleado ' || i || ':');
  DBMS_OUTPUT.PUT_LINE('  Nombre: ' || empleados(i).NOMBRE);
  DBMS_OUTPUT.PUT_LINE('  Salario: ' || empleados(i).SALARIO);
  DBMS_OUTPUT.PUT_LINE('  Código de departamento: ' || empleados(i).COD_DEPARTAMENTO);
END LOOP;

-- Visualización del nuevo número de empleados
DBMS_OUTPUT.PUT_LINE('Nuevo número de empleados: ' || empleados.COUNT);
