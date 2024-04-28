-- Creamos un bloque que tenga un cursor para empleados. Debemos crearlo con FOR 
-- UPDATE.
-- a. Por cada fila recuperada, si el salario es mayor de 8000 incrementamos el 
-- salario un 2% 
-- b. Si es menor de 8000 lo hacemos en un 3% o 
-- c. Debemos modificarlo con la cláusula CURRENT OF o Comprobar que los 
-- salarios se han modificado correctamente

CREATE OR REPLACE PROCEDURE actualizar_salarios AS
    CURSOR c_empleados IS
        SELECT employee_id, salary
        FROM employees
        FOR UPDATE;
    v_employee_id employees.employee_id%TYPE;
    v_salary employees.salary%TYPE;
BEGIN
    FOR emp_rec IN c_empleados LOOP
        v_employee_id := emp_rec.employee_id;
        v_salary := emp_rec.salary;
        
        IF v_salary > 8000 THEN
            v_salary := v_salary * 1.02; -- Incremento del 2%
        ELSE
            v_salary := v_salary * 1.03; -- Incremento del 3%
        END IF;
        
        UPDATE employees
        SET salary = v_salary
        WHERE CURRENT OF c_empleados;
    END LOOP;
    
    COMMIT; -- Confirmar los cambios
    DBMS_OUTPUT.PUT_LINE('Salarios actualizados correctamente.');
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK; -- Deshacer los cambios en caso de error
        DBMS_OUTPUT.PUT_LINE('Error: ' || SQLERRM);
END actualizar_salarios;
/



BEGIN
    actualizar_salarios;
END;
