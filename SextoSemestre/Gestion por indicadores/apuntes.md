# apuntes

## Formula para conocer el poder predictivo de la tabla de confusion

Para evaluar el poder predictivo de un modelo a partir de su tabla de confusión, se pueden utilizar varias métricas. Aquí te presento algunas de las más comunes:

1. **Precisión (Accuracy)**: Mide la proporción de predicciones correctas (tanto positivas como negativas) entre el total de casos.
   $$ \text{Precisión} = \frac{TP + TN}{TP + TN + FP + FN} $$

2. **Sensibilidad (Recall o Tasa de Verdaderos Positivos)**: Mide la proporción de positivos reales que fueron identificados correctamente.
   $$ \text{Sensibilidad} = \frac{TP}{TP + FN} $$

3. **Especificidad (Tasa de Verdaderos Negativos)**: Mide la proporción de negativos reales que fueron identificados correctamente.
   $$ \text{Especificidad} = \frac{TN}{TN + FP} $$

4. **Valor Predictivo Positivo (VPP o Precision)**: Mide la proporción de positivos predichos que son verdaderos positivos.
   $$ \text{VPP} = \frac{TP}{TP + FP} $$

5. **Valor Predictivo Negativo (VPN)**: Mide la proporción de negativos predichos que son verdaderos negativos.
   $$ \text{VPN} = \frac{TN}{TN + FN} $$

6. **F1-Score**: Es la media armónica de la precisión y la sensibilidad, y se utiliza para comparar la precisión de diferentes modelos.
   $$ \text{F1-Score} = 2 \times \frac{\text{Precisión} \times \text{Sensibilidad}}{\text{Precisión} + \text{Sensibilidad}} $$

Estas métricas te ayudarán a entender mejor el rendimiento de tu modelo de clasificación¹².

Origen: Conversación con Bing, 18/3/2024
(1) Cómo interpretar la matriz de confusión: ejemplo práctico. https://telefonicatech.com/blog/como-interpretar-la-matriz-de-confusion-ejemplo-practico.
(2) Matriz de confusión — Aprendizaje automático — DATA SCIENCE. https://datascience.eu/es/aprendizaje-automatico/matriz-de-confusion/.
(3) ¿Qué es una matriz de confusión? - Unite.AI. https://www.unite.ai/es/que-es-una-matriz-de-confusion/.

______________________________________
# FINAL

Realizar una aplicacion real de todo lo visto (futbol, salud, marketing, etc)

* Limpieza: se normalizan y vuelven numericos los datos 
* Preparacion de datos: 
   * Buscar outliers o datos atipicos para determinar cuales son las variable que pueden llegar a generar ruido, esto se puede hacer observando el histograma y validar si tiene o no un sesgo
   * Eliminar los datos atipicos de cada columna de datos que se vea afectada
* Regresion logistica o multiple