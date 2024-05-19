# Laboratorio Cohorte I

Se deberá presentar el código PL/SQL (En bloques anónimos con gestión de excepciones)
que dé solución a los siguientes puntos.

    1. Queremos calcular el impuesto de un producto.
        a. El impuesto será del 21%. Le debemos poner en una constante.
        b. Creamos una variable de tipo number (5,2) para poner el precio del producto
        c. Creamos otra variable para el resultado. Le decimos que es del mismo tipo (type) que la anterior.
        d. Hacemos el cálculo y visualizamos el resultado

    2. Visualizar iniciales de un nombre
        a. Crea un bloque PL/SQL con tres variables VARCHAR2: 
        i. Nombre
        ii. apellido1
        iii. apellido2
        b. Debes visualizar las iniciales separadas por puntos. 
        c. Además, siempre en mayúscula 
        d. Por ejemplo, alberto pérez García debería aparecer--> A.P.G
        
    3. Averiguar el nombre del día que naciste, por ejemplo "Martes"
    
    4. Crear una variable CHAR(1) denominada TIPO_PRODUCTO. 
        a. Poner un valor entre "A" Y "E" 
        b. Visualizar el siguiente resultado según el tipo de producto 
        i. 'A' --> Electronica
        ii. 'B' --> Informática
        iii. 'C' --> Ropa
        iv. 'D' --> Música 
        v. 'E' --> Libros 
        vi. Cualquier otro valor debe visualizar "El código es incorrecto

    5. Práctica 1 - bucles
        a. Vamos a crear la tabla de multiplicar del 1 al 10, con los tres tipos de bucles: 
        LOOP, WHILE y FOR
    
    6. Práctica 2-bucles •
        a. Crear una variable llamada TEXTO de tipo VARCHAR2(100).
        b. Poner alguna frase
        c. Mediante un bucle, escribir la frase al revés, Usamos el bucle WHILE 

    7. Práctica 3 - bucles
        a. Usando la práctica anterior, si en el texto aparece el carácter "x" debe salir del bucle. Es igual en mayúsculas o minúsculas. 
        b. Debemos usar la cláusula EXIT.
    
    8. Práctica 4-bucles
        a. Debemos crear una variable llamada NOMBRE
        b. Debemos pintar tantos asteriscos como letras tenga el nombre. Usamos un bucle FOR
        c. Por ejemplo, Alberto → ******* 
        d. por ejemplo, Pedro → ***** 5. 
        e. Práctica 5 – bucles
        i. Creamos dos variables numéricas, "inicio y fin" 
        ii. Las inicializamos con algún valor: 
        iii. Debemos sacar los números que sean múltiplos de 4 de ese rango

    9. Creamos un TYPE RECORD que tenga las siguientes columnas 
        NAME VARCHAR2(100), 
        SAL EMPLOYEES.SALARY%TYPE,
        COD_DEPT EMPLOYEES.DEPARTMENT_ID%TYPE); 
        a. Creamos un TYPE TABLE basado en el RECORD anterior
        b. Mediante un bucle cargamos en la colección los empleados. El campo NAME debe contener FIRST_NAME y LAST_NAME concatenado. 
        c. Para cargar las filas y siguiendo un ejemplo parecido que hemos visto en el vídeo usamos el EMPLOYEE_ID que va de 100 a 206 
        d. A partir de este momento y ya con la colección cargada, hacemos las siguientes operaciones, usando métodos de la colección. 
        i. Visualizamos toda la colección 
        ii. Visualizamos el primer empleado
        iii. Visualizamos el último empleado 
        iv. Visualizamos el número de empleados 
        v. Borramos los empleados que ganan menos de 7000 y visualizamos de nuevo la colección 
        vi. Volvemos a visualizar el número de empleados para ver cuantos se han borrado
