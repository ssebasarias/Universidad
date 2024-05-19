# Importar las librerías
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Leer el data set
df = pd.read_csv("proyectoFinal/Fish.csv")

# Verificar el tipo de datos, el número de filas y columnas, y si hay valores nulos o duplicados
df.info()
df.shape
df.isnull().sum()
df.duplicated().sum()

# Limpiar y transformar los datos (en este caso no hay mucho que hacer, solo cambiar el nombre de una columna)
df = df.rename(columns={"Length1":"Length_Vertical", "Length2":"Length_Diagonal", "Length3":"Length_Cross"})

# Explorar los datos con estadísticas descriptivas y gráficos
df.describe()
df["Species"].value_counts()
df.corr()

# Hacer un histograma del peso de los peces
# muestra la distribución del peso de los peces
plt.hist(df["Weight"], bins=20) 
plt.xlabel("Weight (g)")
plt.ylabel("Frequency")
plt.title("Histogram of Fish Weight")
plt.show()

# Hacer un boxplot del peso de los peces según la especie
# muestra cómo varía el peso con cada especie de pez
sns.boxplot(x="Species", y="Weight", data=df) 
plt.xlabel("Species")
plt.ylabel("Weight (g)")
plt.title("Boxplot of Fish Weight by Species")
plt.show()

# Hacer un gráfico de dispersión del peso y la longitud vertical de los peces
# muestra si hay alguna relación entre el peso y la longitud vertical de los peces
plt.scatter(df["Weight"], df["Length_Vertical"])
plt.xlabel("Weight (g)")
plt.ylabel("Length Vertical (cm)")
plt.title("Scatterplot of Fish Weight and Length Vertical")
plt.show()


# Hacer un mapa de calor de la matriz de correlación entre las variables numéricas
# muestra las correlaciones entre todas las variables numéricas
sns.heatmap(df.corr(), annot=True, cmap="Blues")
plt.title("Heatmap of Correlation Matrix")
plt.show()