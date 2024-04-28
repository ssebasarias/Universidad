-- Vamos averiguar cuáles son los JEFES (MANAGER_ID) de cada departamento. En la 
-- tabla DEPARTMENTS figura el MANAGER_ID de cada departamento, que a su vez es 
-- también un empleado. Hacemos un bloque con dos cursores. (Esto se puede hacer 
-- fácilmente con una sola SELECT pero vamos a hacerlo de esta manera para probar 
-- parámetros en cursores).
-- a. El primero de todos los empleados o El segundo de departamentos, 
-- buscando el MANAGER_ID con el parámetro que se le pasa. 
-- b. Por cada fila del primero, abrimos el segundo cursor pasando el 
-- EMPLOYEE_ID 
-- c. Si el empleado es MANAGER_ID en algún departamento debemos pintar el 
-- Nombre del departamento y el nombre del MANAGER_ID diciendo que es el 
-- jefe. 
-- d. Si el empleado no es MANAGER de ningún departamento debemos poner “No 
-- es jefe de nada”

CREATE OR REPLACE PROCEDURE mostrar_jefes AS
    CURSOR c_empleados IS
        SELECT employee_id, first_name, last_name, manager_id
        FROM employees;
    v_employee_id employees.employee_id%TYPE;
    v_first_name employees.first_name%TYPE;
    v_last_name employees.last_name%TYPE;
    v_manager_id employees.manager_id%TYPE;
    v_department_name departments.department_name%TYPE;
BEGIN
    FOR emp_rec IN c_empleados LOOP
        v_employee_id := emp_rec.employee_id;
        v_first_name := emp_rec.first_name;
        v_last_name := emp_rec.last_name;
        v_manager_id := emp_rec.manager_id;
        
        BEGIN
            SELECT department_name INTO v_department_name
            FROM departments
            WHERE manager_id = v_employee_id;
        EXCEPTION
            WHEN NO_DATA_FOUND THEN
                v_department_name := NULL;
        END;
        
        IF v_department_name IS NOT NULL THEN
            DBMS_OUTPUT.PUT_LINE(v_first_name || ' ' || v_last_name || ' (jefe de ' || v_department_name || ')');
        ELSE
            DBMS_OUTPUT.PUT_LINE(v_first_name || ' ' || v_last_name || ' (no es jefe de nada)');
        END IF;
    END LOOP;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
END mostrar_jefes;
/


BEGIN
    mostrar_jefes;
END;



