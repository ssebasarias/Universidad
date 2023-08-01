import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datos
data = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/diamonds.csv")

# Mostrar título
st.title("Visualización de datos con Streamlit")

# Mostrar datos
st.subheader("Datos de diamantes")
st.write(data)

# Gráfico de barras
st.subheader("Gráfico de barras")
bar_plot = sns.countplot(x="cut", data=data)
st.pyplot(bar_plot.figure)

# Gráfico de dispersión
st.subheader("Gráfico de dispersión")
scatter_plot = plt.scatter(x="carat", y="price", data=data)
st.pyplot(scatter_plot.figure)

# Gráfico de líneas
st.subheader("Gráfico de líneas")
line_plot = sns.lineplot(x="carat", y="price", data=data)
st.pyplot(line_plot.figure)
