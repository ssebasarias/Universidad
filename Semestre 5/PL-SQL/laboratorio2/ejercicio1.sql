-- Hacer un programa que tenga un cursor que vaya visualizando los salarios de los 
-- empleados. Si en el cursor aparece el jefe (Steven King) se debe generar un 
-- RAISE_APPLICATION_ERROR indicando que el sueldo del jefe no se puede ver.

CREATE OR REPLACE PROCEDURE mostrar_salarios AS
    CURSOR c_empleados IS
        SELECT first_name, last_name, salary
        FROM employees;
    v_first_name employees.first_name%TYPE;
    v_last_name employees.last_name%TYPE;
    v_salary employees.salary%TYPE;
BEGIN
    FOR emp_rec IN c_empleados LOOP
        v_first_name := emp_rec.first_name;
        v_last_name := emp_rec.last_name;
        v_salary := emp_rec.salary;
        
        IF v_first_name = 'Steven' AND v_last_name = 'King' THEN
            DBMS_OUTPUT.PUT_LINE('El salario del jefe no se puede ver.');
        ELSE
            DBMS_OUTPUT.PUT_LINE(v_first_name || ' ' || v_last_name || ': ' || v_salary);
        END IF;
    END LOOP;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
END mostrar_salarios;
/




BEGIN
    mostrar_salarios;
END;
