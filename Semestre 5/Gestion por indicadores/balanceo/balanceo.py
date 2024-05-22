import pandas as pd
import os
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler, SMOTE
from collections import Counter

# Ruta al archivo CSV
file_path = './Libro1.csv'  # Asegúrate de que esta ruta sea correcta

# Verificar si el archivo existe
if not os.path.isfile(file_path):
    raise FileNotFoundError(f'El archivo no se encontró: {file_path}')

# Intentar leer el archivo CSV con opciones adicionales
try:
    df = pd.read_csv(file_path, error_bad_lines=False, warn_bad_lines=True)  # Omitir líneas mal formateadas
except pd.errors.ParserError as e:
    print(f'Error leyendo el archivo CSV: {e}')
    exit()

# Verifica que se haya leído correctamente
print(df.head())

# Supongamos que la columna de características se llama 'features' y la columna objetivo se llama 'target'
# Ajusta esto según tu archivo CSV
# Aquí usaremos nombres de columna de ejemplo, asegúrate de reemplazarlos con los nombres correctos de tus columnas
X = df.drop('target', axis=1)
y = df['target']

print(f'Original dataset shape: {Counter(y)}')

# Selecciona la técnica de balanceo: RandomUnderSampler, RandomOverSampler o SMOTE
# Aquí usamos SMOTE como ejemplo
smote = SMOTE(random_state=42)
X_res, y_res = smote.fit_resample(X, y)

print(f'Resampled dataset shape: {Counter(y_res)}')

# Crear un nuevo DataFrame con los datos balanceados
df_res = pd.concat([pd.DataFrame(X_res, columns=X.columns), pd.DataFrame(y_res, columns=['target'])], axis=1)

# Guardar el nuevo DataFrame balanceado en un archivo CSV
output_path = './Libro1_balanceado.csv'  # Reemplaza con la ruta donde quieres guardar el archivo balanceado
df_res.to_csv(output_path, index=False)
print(f'Datos balanceados guardados en: {output_path}')
