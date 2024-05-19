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

_________
Para cumplir con los requerimientos del proyecto PANIC, podemos utilizar las siguientes herramientas y tecnologías:

Base de datos: PostgresSQL
Lenguaje de programación: Python
Framework web: Flask
Lenguajes de marcado: HTML, CSS
Lenguaje de scripting en el lado del servidor: PHP
API de Maps de Google
Para comenzar, necesitaríamos crear una base de datos en PostgresSQL que contenga las tablas necesarias para registrar y almacenar información sobre los participantes, los puntos de encuentro y la actividad registrada.

Luego, podríamos utilizar Flask como nuestro framework web para crear una API que permita a la aplicación móvil y a la página web interactuar con la base de datos. Podemos utilizar la biblioteca Flask-Restful para crear una API RESTful fácilmente.

Para mostrar los mapas y las indicaciones de ubicación, podemos utilizar la API de Maps de Google. Para ello, necesitaríamos obtener una clave de API de Google y utilizarla en nuestra aplicación.

En cuanto a la aplicación móvil, podríamos desarrollarla utilizando un lenguaje de programación nativo para iOS o Android, o utilizar un framework multiplataforma como React Native o Flutter para crear aplicaciones móviles tanto para iOS como para Android.

En la página web, podemos utilizar HTML y CSS para crear el frontend y PHP para crear el backend. Utilizando PHP, podemos interactuar con la API creada con Flask y obtener información de la base de datos para mostrarla en la página web.

Para resumir, para crear el proyecto PANIC necesitaríamos:

PostgresSQL como base de datos
Python y Flask para crear una API RESTful
HTML, CSS y PHP para crear la página web
React Native o Flutter para crear la aplicación móvil
API de Maps de Google para mostrar los mapas y las indicaciones de ubicación.
