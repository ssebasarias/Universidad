# Metodologias Data Mining

Variables latentes: son un conjunto de variables observables, cada una tiene sus variables debe de estar relacionada.

## Pasos para construir un modelo

1. Evaluacion de modelo de medicioMarcar las relaciones (entender los datos y entender cuales son las variables latentes).
    1.1. Evalucaion de la validez convergente: Las variables latentes se comporten como una unidad teorica (todos los items pertenecen al mismo fenomeno).
        - Indicadores: Cargas estandarizadas (umbral > 0,6), fiabilidad compuesta o rho a (umbral 0,6) y varianza extraida media -  AVE (0,5).
    1.2. Evaluacion de la valiedez discriminante: Que las variables latentes sean diferentes
    1.3. Evaluacion de validez discriminante: las variables latentes sean diferentes. HTMT menor a 0,9, cargas cruzadas (buscar que las relaciones con items de otras variables sean menores a 0,6 si se puede)
        resumen:
        CONVERGENCIA: que todas se relacionan en un mismo fenomeno
        DISCRIMINANCIA: que hay dos fenomenos diferentes

    1.4. Bajar indicadores:
    - calcular > algoritmo pls > eliminar las que estan por debajo de 0,6.
    - criterios de calidad > resumen (mirar el alpha...)

2. Evaluacion del modelo estructural: evaluar las relaciones entre las variables

    2.1. Coeficiente Path (umbral de mayor a 0,1): signo (positivo o negativo)
    inner model > path coeficients and t value

    2.2. Significancia estadistica: t value (1,6 mayor a 2,5) y los intervalos (NO deben pasar por 0)
    informe de bootstraping > coeficiente path > intervalos de confianza

    R CUADRADO: poder predictivo del modelo
    MEDIACION PARCIAL: cuando las relaciones tanto directas como indirectas son significativas
    MEDIACION TOTAL: Cuando la relacion directa no es significativa, pero la indirecta si lo es

_________________________________________________________________
r poder predifcrivo dentro de la muestra 
q fuera de la meustra

_______________________________________________________________________________
CLUSTERIZACION
Agrupaciones que tienen caracteristicas similares a la categorizacion pero que estas no estas ya estructuradas, es decir, la categorizacion ya existe, categoria hombre y categoreia mujer, en cambio los datos cluster no.
Agrupacion de datos con caracteristicas similares

## Pregunta de investigacion

cual es el tipo de empresa que prevalece en el sector manufactutra colombiana?

## Apuntes de la base de datos cluster

Dos tipos de empresa => 

1. inovvacion - prospectora 
El analisis de las empresas de inovacion se enfocan en lo externo a la empresa, es decir, item como el crecimiento de la empresa, productos innovadores, competencia del mercado, publicidad, etc etc

2. eficiencia operacional - defensora
El analisis de estas empresas se enfocan en lo interno de la empresa, analisar sus procesos de procesos como la eficiencia y claidad de la empresa

## paso a paso aplicacion SPSS

1. Cargar datos tipo excel
2. cambiar datos a escala
3. Agregar etiquetas
4. agregar escala liker al apartado de valores a las variables etiquetadas
5. Analizar datos con metodo cluster
	5.1. Cluster jerarquico (en el caso de esta base de datos solo son 2 cluster, inovacion y eficiencia operacional)
	5.2. Usando las variables de etiqueta y la variable cluster generada se genera la moda para comprobar que cluster es 1 y cual es 2
	5.3. Teniendo en cuenta el dato anterior ir a frecuencia para determinar los porcentajes de la influencia de los datos  (en este caso, las Empresas Tradicionales son el 76% de la manufacutura colombiana y el porcenje restante es de empresas innovadoras)

## Vocabulario

**Discretizacion** : convertir un grupo de variables en una vaiable unica
