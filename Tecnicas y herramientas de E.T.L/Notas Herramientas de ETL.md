E -> Extracción
T -> Transformación
L -> Carga de datos
	
	Serie de tareas para centralizar los datos provenientes de diferentes fuentes, tranformarlos, automatizarlos 
	y mostrarlos en una herramienta de visualización para su analisis y posteriormente toma de decisiones.
	FUENTES INTERNAS -> - Servidores de la copañia
				  - Archivos
				  - CRM
	FUENTES EXTERNAS -> - APIs
				  - Bases de datos
	TIPOS DE DATOS -> - Estructurados (Datos de tipo filas y columnas como un .CSV)
				- Semi-estructurados (Informacion relvante dentro de u codigo, 
								por ejemplo ta información dentro de lasetiquetas html)       => ¡¡¡ INVESTIGAR !!!
				- No etructurados (Audios, PDFs, videos, imagenes)



# Taller
* Usando la pokeAPI obtener los datos de los primeros 151 pokemons 

https://pokeapi.co/api/v2/pokemon/?limit=151

* muestre el nombre, zona, habilidad (una celda nueva por habilidad), la url de la foto del pokemon, el ancho y alto del pookemon.
* usar 2 o 3 librerias (Request, json, pandas).
_________
# Taller 2
Crear 3 procesos de ETL en herramientas diferentes. (obligatorio que uno de esos proyectos consuma una API)