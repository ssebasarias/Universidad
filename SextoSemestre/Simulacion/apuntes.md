# Apuntes Simulacion

## Formulas

### Exactitud

La exactitud del modelo se calcula sumando los verdaderos positivos (VP) y los verdaderos negativos (VN), y luego dividiendo por el total de casos. Usando la matriz de confusión proporcionada:

$$ \text{Exactitud} = \frac{VP + VN}{VP + FN + FP + VN} $$

Ejemplo:

$$ \text{Exactitud} = \frac{30 + 40}{30 + 20 + 10 + 40} = \frac{70}{100} = 0.70 $$

Por lo tanto, la respuesta correcta es la opción **a. 0.70**.

______________________________________________

### Especificidad

La especificidad del modelo se calcula con la fórmula:

$$ \text{Especificidad} = \frac{VN}{VN + FP} $$

Ejemplo:
**matriz de confusión con 40 VP, 10 FN, 20 FP y 30 VN**
Donde VN son los Verdaderos Negativos y FP son los Falsos Positivos. Utilizando los valores de la matriz de confusión proporcionada

$$ \text{Especificidad} = \frac{30}{30 + 20} = \frac{30}{50} = 0.60 $$

Por lo tanto, la respuesta correcta es la opción **d. 0.60**.

______________________________________________

### Presicion

La precisión se calcula con la fórmula:

$$ \text{Precisión} = \frac{VP}{VP + FP} $$

Donde VP son los Verdaderos Positivos y FP son los Falsos Positivos. Utilizando los valores de la matriz de confusión proporcionada:

$$ \text{Precisión} = \frac{40}{40 + 20} = \frac{40}{60} = \frac{2}{3} \approx 0.67 $$

Por lo tanto, con los valores dados de 40 VP, 10 FN, 20 FP y 30 VN, la precisión del modelo es aproximadamente **0.67**.
