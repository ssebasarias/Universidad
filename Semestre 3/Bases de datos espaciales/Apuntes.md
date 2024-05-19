#### 07/03/2023
## GPS
Cuando se habla de GPS se habla de de un conjunto de satelites que ofecen informacion de la posicion en la cual se encuentra la antena receptora como un celular.
_____
#### 14/03/2023
## Base de datos relacional
las bases de datos relacionales son, como su nombre lo indica, bases de datos que sus elementos se relacionan entre si, siendo una llave primaria la forma en la que se indentifica unicamente ese elemento y la llave foranea la forma en la cual otra tabla relaciona el **comportamiento** de la otra tabla, por ejemplo, una hamburguesa esta relacionada a las ventas, la llave foranea de tal hamburguesa serianla cantidad de veces que fue vendida, es decir, la cantidad de veces que aparecio o interactuo con la otra tabla ventas.

## Bases de datos no SQL
Las bases de datos no SQL son aquellas no relaciones, y por ende son mas faciles de procesar

## Bases de datos espaciales
Son aquellas que puedes contener a los dos otros dos tipos de bases de datos, es decir, se puede almacenar, organizar y categorizar todo tipo de datos, procesando y analizando _datos brutos_, es decir, datos que de por si no dicen nada pero comparados con otros datos dan un contexto.
**NOTA:** los datos en bases de datos espaciales se les llama **GEODATOS_**.

## Repaso matematico
### Datos vectoriales: 
Es una reresentacion de una posicion o un punto en una linea.
### Datos matriciales:
Forma mas especific y detallada de representar un punto o una posición, por ejemplo, una imagen esta compuesta de varios pixceles, un pixel es como una matriz.

## Nota: 
Se realizo una aplicacion de ubicación con la API de Google maps en AppInventor.
__________
#### 23/03/2023
## Resumen de la clase
* Se instalo postgres y postgis con un ejemplo de una base de datos espacial.
* Se creo una base de datos prueba.

## Tarea
* Restaurar la base de datos que esta en el Drive usando el paso a paso del enlace.
______
#### 11/04/2023
# Proyecto _PANIC_ (Prevencion de desastres)
## Objetivos personales a desarrollar con el proyecto
* Mejorar las habilidades en diseño de base de datos
* Incorporar elementos espaciales para ser representados
* Realizar procesos de consulta sobre BD espaciales
* Fortalecer las habilidades en programación

# Proyecto _PANIC_
## Concepto base
A traves de una aplicacion movil, dar informacion al usuario de donde tiene que evacuar segun el lugar donde este ubicado, de tal forma que la aplicacion muestre en un plano de la estructura o mapa de la zona, la ubicacion mas cercana a la cual debe acuditr y las indicaciones para llegar a ella en caso de algun tipo de desastre.

## Requerimientos basicos
* Ubicar y registrar la cantidad de los puntos de encuentro. Debe de poder cargar cualquier tipo de plano o mapa.
* Registrar a los participantes. Ejemplo: nombre completo, identificacion personal e identificacion de la empresa, correo, estado de salud, discapacidad, ubicacion en tiempo real, telefono propio y de conocidos.
* Registrar toda la actividad de los participantes. Ejemplo: Cuantas personas estan registradas en la aplicacion, cuantas llegaron al punto de encuentro, a que hora llegaron al punto, cuanto tiempo se tardaron en llegar a punto, a que hora inicio el evento, a que hora finalizó, registrar ritmo cardiaco (En caso de que tenga algun dispositivo que pueda proporcionar esta informacion).
* Consultar los datos:
    * El participante mas rapido
    * El participante mas lento
    * Cuantos llegaron al punto de encuentro
    * Cuantas personas hay por punto de encuentro
    * Cuantas zonas habian disponibles
    * Estadisticas generales de las variables tomadas en cuenta para medir la actividad 

## Aportes
* Hacer la invasiva como la autenticacion de google
* Agregarle realidad virtual para hacer mas real el simulacro

## Preguntas
* ¿Que pasa si no tiene internet?


# Trabajo para la siguiente clase
Tener los mokups y el esquema de la base de datos que funcione para el proyecto