-- Modificar el programa anterior para incluir un parámetro que pase el número de 
-- departamento para que visualice solo los empleados de ese departamento
-- a. Debe devolver el número de empleados en una variable de tipo OUT

CREATE OR REPLACE PROCEDURE visualizar_empleados(p_department_id IN NUMBER, p_num_empleados OUT NUMBER) AS
BEGIN
    p_num_empleados := 0; 
    
    FOR emp_rec IN (SELECT first_name, last_name, salary FROM employees WHERE department_id = p_department_id) LOOP
        DBMS_OUTPUT.PUT_LINE('Nombre: ' || emp_rec.first_name || ' ' || emp_rec.last_name || ', Salario: ' || emp_rec.salary);
        p_num_empleados := p_num_empleados + 1;
    END LOOP;
END visualizar_empleados;
/


DECLARE
    v_num_empleados NUMBER;
BEGIN
    visualizar_empleados(p_department_id => 30, p_num_empleados => v_num_empleados);
    DBMS_OUTPUT.PUT_LINE('Número de empleados: ' || v_num_empleados);
END;