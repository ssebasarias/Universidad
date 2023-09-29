02/08/23

Todo discpositivo tecnologico es conocido como artefacto computacional o digital, ya sea telefono, computador, arduino. smar tv, etc.

## ARQUITECTURA DEL COMPUTADOR
Se habla sobre la evolucion de la tecnologia y las maquinas computacionales desde el abaco, pasand por la maquina de pascal, eniac, turing, ps ibm y la computadora actual.
Se habla de tajetas gaficas, ,arcas y transistores microscopicos que lo componen. 

__________________
14/08/23

## Maquina virtual:
Es un sistema operativo derivado del sistema operativo nativo.

## Cliente/servidor:
Es como un punto de encuentro en la nube o en linea donde varios usuarios para pueden conectarse mediante un puerto para pder usar los servicios y/o informacion almacenaa ahi, funciona como una tienda, la cual espera a que un cliente entre para poder antenderlo, un ejemplo de servidores pueden ser: 
  * Apache
  * Postgres
  * Mysql
  * SSH

### NOTA:
TCP/IP es el protocolo base para trabajar esta area. Ejemplo: 140.12.1.27. 
Las redes privadas son las que empiezan por **10, 193 ó 172**, de resto todas las direcciones son publicas.

__________________
16/08/23

## COMANDOS LINUX
* sudo -i: para ingresar como administrador
* apt: para conectarme al repositorio en la nube o en linea y obtener lo que necesito
  * apt-get update (actualiza el sistema)
  * apt-get upgrade (descarga los archivos que debe descargar de la actualizacion)
  * apt_get install net-tools (para instalar paquetes o herramientas de para ver el estado de la red)
  * apt-cache search (Busca a traves de palabras clave paquetes que esten en el repositorio) Ej: apt-cache search Apache2
* whoami: Para saber en que usuario estoy (el usuario **1000** es el usuario que cree, el root es el usuario **1**)
* poweroff: para apagar verdaderamente la maquina
* clear: para limpiar la pantalla o eliminar los comandos que hice anteriormente
* ifconfing (es un comando que muestra las caracteristicas de la tarjeta de red) __nota: solo funciona si se tien intalado el paquete net-tools__
* ssh user@IP (para conectarse remotamente a un servidor) ejemplo: ssh maria@192.168.0.85
* ctrl + alt + f1 o fn (para intercambiar entre terminales)
* chmod (para otorgar permisos a un archivo) ejemplo: chmod 740 archivo.txt
* chown ()
* wget (Para clonar una pagina y obtener la informacion de ella, esto puede servir para descargar un archivo)

## COMANDOS WINDOWS
* ping (para saber si estoy conectado a un dispositivo o una red) __ejemplo: ping 10.0.2.15__

## APLICACIONES 
* PuTTY (herramienta que ayuda a conectarse entre dispositivos usando la IP)

_____________________
28/08/23

## CONECTARSE ENTRE MAQUINAS EN UNA RED LOCAL
Se convierte una maquina en eun servidor local abriendo los puertos de la maquina y haciendo otorgando permisos para que otra maquina usando puTTY pueda ingresar con la IP o por medio de linux con el comando ssh y el usuario e IP con la que se va a conectar.

_____________________
30/08/23

## SISTEMA OPERATIV0 
### FUNCIONES
* Algunos sistemas operativos funcionan para un tipo de hardware especifico, si desaparece el hardware desaparece el SO
* El almacenamiento de los SO funcionan con algunos tipos como:
   * FAT 16/32
   * NTFS
   * EXT3/4 (la mas usada actualmente)
 Estas funciones son necesarias para las rutas de almacenamiento sea mas eficinte, tanto la ruta relativa como la absoluta

### COMPONENSTES DEL SO (capas)
* 1) **Hardware:** Determina como debe de ser el sistema operativo y que debe de tener segun sus componentes para poder soportarlo
* 2) Nucleo
* 3) Api del nucleo - servicios: Es lo que hace que sea posible convertir la maquina en un servidos, entre otras funciones
* 4) sistema de archivos - drivers: Necesarios para poder que el SO reconosca los componentes o HARDWARE, un ejemplo claro son los drivers necesarios para usar una tarjeta grafica
* 5) Interfaz - aplicativos
* 6) Usuario final

### TIPOS DE SO
#### MONOLITICO:
Solo se podia realizar una tarea o proceso a la vez y si se bloqueaba una tarea se bloqueaba toda la maquina

#### MICRO KERNEL
Sistema operativo multi tarea y multi plataforma, ya que soporta casi cualquier tipo de hardware y tiene forma de modificarla para poder adaptarla de mejor manera a algo mas especifico y hacerla mas eficiente para el tipo de dispositivo especifico, es decir, se puede usar solo una parte del SO especifica para mejorar la eficiencia. Algunas de las caracteristicas de este SO son:
 * Seguro
 * bajo rendimiento
 * se ejecuta con provilegios
 * escalable
 * simple mantenimiento
 * multi tarea para realizar procesos divididos en modo kernel y modo usuario

#### ESTRUCTURA DE VM (maquina virtual)
Es usada para aprovehcar al maximo los recursos potentes de una maquina, de esta manera se puede ejecutar no solo varios procesos sino tambien hacerlo en diferentes tipos de SO.

#### ARQUITECTURA DE MAC OS
Esta esta contruida por una base de SO linux llamada Darwin, un conjunti de estructuras de aplicaciones, estructura de graficos y por ultimo la interfaz de usuario.

#### ARQUITECTURA DE WINDOWS


#### AEQUITECTURA DE LINUX


### TEMAS A CONSULTAR 
* Caracteristicas de las redes inalambricas y el protocolo 802.11 abcg
* Caracteristicas del cable micro USB, C y HDMI
* 

_____________________
13/09/23

## Puertos

* Samba   445 
* SSH     22
* FTP     21
* Telnet  23
* Apache  80 / Nginx  80 

# Tarea
Crear una pagina y subirla al  servidor apache usando linux como servidor y logrando verla desde cualquier dispositivo en la misma red
Ruta de apache: /var/www/html

## Consulta "Que es y como se instala Nginx"

__________________
20/09/23

# Descargar e instalar apache compilado

1. Dentro de la carpeta 'httpd-2.4' se descarga todos los archivos descomprimidos 
2. ./configure --prefix=Nombre_carpeta
3. make
4. make install
5.  
