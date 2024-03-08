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