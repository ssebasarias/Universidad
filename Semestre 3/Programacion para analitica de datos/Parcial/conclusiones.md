# Resumen y explicación del codigo
Este código utiliza las bibliotecas Pandas, Matplotlib y Seaborn para analizar dos conjuntos de datos de vinos. Primero, los datos se leen con `read_csv` y se imprimen los primeros registros y la información del conjunto de datos con los métodos `head` e `info`, para analizar los datos que se tiene  en los data sets y tomar desiciones.

Luego, los datos duplicados se eliminan con `drop_duplicates`. A continuación, se seleccionan ciertas variables del conjunto de datos mediante la creación de nuevas variables `red_selection` y `white_selection`.

Después se grafican histogramas utilizando Seaborn. El método `subplots` de Matplotlib crea una matriz de gráficos y el bucle `for` dibuja un histograma por cada variable seleccionada en cada uno de estos gráficos. Finalmente, se muestra la matriz de histogramas con `plt.show()`. 

Luego, se utiliza `sns.pairplot` para graficar un scatterplot entre todas las variables seleccionadas. También se especifica que solo se muestre la mitad superior e izquierda del gráfico con el argumento `corner=True`, y se especifca `diag_kind='hist'` para mostrar histogramas en los diagonales.

Finalmente, se utiliza `sns.heatmap` para calcular y visualizar la correlación entre las variables del conjunto de datos seleccionado. El argumento `annot=True` permite mostrar los valores de correlación en los cuadros de color. El argumento `cmap='coolwarm'` establece la paleta de colores utilizada para el mapa de calor.

# Conclusión
Con los histogramas podemos apreciar cómo están distribuidas cada una de las variables en el conjunto de datos y visualizar la forma de la campana, lo que nos puede indicar si siguen una distribución normal o no. El gráfico de correlación indica qué variables están más correlacionadas con otras. De esta forma, podemos descubrir relaciones interesantes que pueden ser útiles para análisis posteriores.

## Nota:
Los tados se pueden visualizar en la imagen adjunta.