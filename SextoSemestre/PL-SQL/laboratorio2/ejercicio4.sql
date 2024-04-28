-- Crear un procedimiento llamado “visualizar” que visualice el nombre y salario de 
-- todos los empleados

CREATE OR REPLACE PROCEDURE visualizar AS
    CURSOR c_empleados IS
        SELECT first_name, last_name, salary FROM employees;
BEGIN
    FOR emp_rec IN c_empleados LOOP
        DBMS_OUTPUT.PUT_LINE('Nombre: ' || emp_rec.first_name || ' ' || emp_rec.last_name || ', Salario: ' || emp_rec.salary);
    END LOOP;
END visualizar;
/



BEGIN
    visualizar;
END;