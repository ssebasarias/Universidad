# Regresion lineal simple: Predecir el peso de los peces en funcion a su longitud:
from sklearn.linear_model import LinearRegression

# Seleccionar las variables predictoras y la variable objetivo
x = df[["Length_Vertical"]]
y = df["Weight"]

# Crear una instancia del modelo de regresión lineal
model = LinearRegression()

# Ajustar el modelo a los datos
model.fit(x, y)

# Hacer una predicción con una longitud vertical de 25 cm
prediction = model.predict([[30]])

# Imprimir la predicción
print(f"La predicción del modelo para un pez con una longitud vertical de 25 cm es {prediction[0]:.2f} gramos.")

#____________________
# Regresion lineal multiple: Predecir el peso de los peces en funcion a su longitud vertical y anchuratransversal:
from sklearn.linear_model import LinearRegression

# Seleccionar las variables predictoras y la variable objetivo
X = df[["Length_Vertical", "Width"]]
y = df["Weight"]

# Crear una instancia del modelo de regresión lineal
model = LinearRegression()

# Ajustar el modelo a los datos
model.fit(X, y)

# Hacer una predicción con una longitud vertical de 25 cm y una anchura transversal de 10 cm
prediction = model.predict([[25, 10]])

# Imprimir la predicción
print(f"La predicción del modelo para un pez con una longitud vertical de 25 cm y una anchura transversal de 10 cm es {prediction[0]:.2f} gramos.")


# Regresion lineal multiple: Predecir el peso de los peces en función de su longitud vertical, anchura transversal y su especie:
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression

# Seleccionar las variables predictoras y la variable objetivo
X = df[["Length_Diagonal", "Width", "Species"]]
y = df["Weight"]

# Crear un codificador one-hot para la variable categórica 'Species'
encoder = OneHotEncoder()
ct = ColumnTransformer([("encoder", encoder, [2])], remainder="passthrough")
X_encoded = ct.fit_transform(X)

# Crear una instancia del modelo de regresión lineal
model = LinearRegression()

# Ajustar el modelo a los datos
model.fit(X_encoded, y)

# Hacer una predicción para un Bass con una longitud vertical de 25 cm y una anchura transversal de 10 cm
prediction = model.predict([[1, 0, 0, 25, 10]])

# Imprimir la predicción
print(f"La predicción del modelo para un Bass con una longitud vertical de 25 cm y una anchura transversal de 10 cm es {prediction[0]:.2f} gramos.")
