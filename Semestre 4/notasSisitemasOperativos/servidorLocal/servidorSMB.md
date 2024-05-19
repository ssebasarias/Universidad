# Crear servidor SMB para conmpartir recursos (Paso a paso)

1. Actualizar el sistema operativo, esto con el fin de que no haya ningun problema al momento de intalar los paquetes necesarios.
    * sudo apt-get update: Comprueba si hay actaulizaciones para el sistema
    * sudo apt-get upgrade: istala las actaulizaciones del sistema

2. Instalar los paquetes necesarios para el servidor
    * sudo apt-get net-tools: Se usa usar el comando ifconfig para verificar la ip para conectarse al servidor
    * sudo apt install samba acl: instala todos los paqurtes y recursos para manipular samba

3. Encender y comprobar samba
    * sudo systemctl enable smbd: Enciende el servidor
    * sudo systemctl status smbd: Para verificar el estado del servidor, si esta o no corriendo

4. Crear una carpeta publica para compartir recursos 
    * sudo mkdir -p /home/samba: crea una carpeta en el repo de samba la cual se usara como ruta para poder comprartir recursos
    * ls -la /home/: Para verificar que la carpeta se haya creado correctamente
    * sudo nano /etc/samba/smb.conf: Ingersa a la carpeta de configuracion del servidor, dentro de ella se puede corregir la ip, el enrutador, los permisos, las condiciones para comparir recursos etc.
        * En el apartado [global] se borra el ";" par descomentar la ip y se edita la ruta de "eth0" a "enp0s3" ya que este es el que usa el servidor para proporcionar la ip.
        Se puede verificar usando el comando de "ifconfig" 
        * Se borra el ";" del apartado " bind interface only = yes"
        * Al final del archivo se agregan las configuraciones: 
        [share]
        comment = Samba directory
        path = /home/samba
        read only = no
        writable = yes
        browseable  yes
        guest ok = no

5. Creamos nuevo ususario para conectar al servidor
    * sudo smbpasswd -a nombre_ususario: Con esto se crea el usuario, despues de le asigna la nueva contrasela y acto seguid se confirma
    * sudo setfacl -R -m "u:nombre_usuario:rwx" /home/samba: De esta manerta se le conceden todos los permisos sobre la carpeta pubilica al nuevo usuario

6. Configurar cortafuegos
    * sudo ufw enable: Para activarlo
    * sudo ufw allow samba: Para darle permisis sobre el servicio samba 
    * sudo ufw allow samba: Para dar permisos sobre el servicio ssh

7. Se reinicia y verifica el estado del servidor para que las configuraciones queden aplicadas
    * sudo systemctl restart smbd: Para reiniciarlo
    * sudo systemctl status smbd: Para verificart que funcione correctamente

___________________________
## Fuentes
* https://www.youtube.com/watch?v=NXsl7WTdKjs