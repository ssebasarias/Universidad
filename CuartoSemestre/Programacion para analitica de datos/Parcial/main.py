import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

red_wines = pd.read_csv('Parcial/winequality-red.csv', sep=';')
white_wines = pd.read_csv('Parcial/winequality-white.csv', sep=';')

# Explorar los datos de los data sets
print(red_wines.head())
print(red_wines.info())

print(white_wines.head())
print(white_wines.info())

# Limpiar los datos duplicados 
red_wines.drop_duplicates(inplace=True)
white_wines.drop_duplicates(inplace=True)

# Seleccionar variables del data set
selected_cols = ['alcohol', 'quality', 'fixed acidity', 'volatile acidity', 'citric acid']

red_selection = red_wines[selected_cols]
white_selection = white_wines[selected_cols]

# Histogramas
fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(16,12))

for i, col in enumerate(selected_cols):
    ax = axs[i//2][i%2]
    sns.histplot(ax=ax, data=red_selection, x=col, bins=25, kde=True) 
    
plt.show()

# Scatterplots
sns.pairplot(data=red_selection, corner=True, diag_kind='hist')

# Correlaciones
sns.heatmap(data=red_selection.corr(), annot=True, cmap='coolwarm')