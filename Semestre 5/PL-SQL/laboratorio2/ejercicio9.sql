-- Crear una función llamada CREAR_REGION,
-- a. A la función se le debe pasar como parámetro un nombre de región y debe 
-- devolver un número, que es el código de región que calculamos dentro de la 
-- función
-- b. Se debe crear una nueva fila con el nombre de esa REGION
-- c. El código de la región se debe calcular de forma automática. Para ello se debe 
-- averiguar cual es el código de región más alto que tenemos en la tabla en ese 
-- momento, le sumamos 1 y el resultado lo ponemos como el código para la 
-- nueva región que estamos creando.
-- d. Si tenemos algún problema debemos generar un error
-- e. La función debe devolver el número que ha asignado a la región

CREATE OR REPLACE FUNCTION crear_region(
  p_region_name IN VARCHAR2
) RETURN NUMBER AS
  v_next_region_code NUMBER;
BEGIN
  -- Obtener el código de región más alto existente
  SELECT MAX(region_id) INTO v_next_region_code FROM regions;

  -- Si no hay registros en la tabla, asignamos el código 1
  IF v_next_region_code IS NULL THEN
    v_next_region_code := 1;
  ELSE
    -- Incrementamos el código en 1 para la nueva región
    v_next_region_code := v_next_region_code + 1;
  END IF;

  -- Insertar la nueva fila en la tabla de regiones
  INSERT INTO regions (region_id, region_name)
  VALUES (v_next_region_code, p_region_name);

  -- Devolver el código asignado a la nueva región
  RETURN v_next_region_code;
EXCEPTION
  WHEN OTHERS THEN
    -- Generar un error si hay algún problema
    RAISE_APPLICATION_ERROR(-20001, 'Error al crear la región: ' || SQLERRM);
END;
/



DECLARE
  v_new_region_name VARCHAR2(25) := 'Nueva Región';
  v_new_region_code NUMBER;
BEGIN
  v_new_region_code := crear_region(v_new_region_name);
  DBMS_OUTPUT.PUT_LINE('Código asignado a la región ' || v_new_region_name || ': ' || v_new_region_code);
END;
/
