import random
from faker import Faker
import csv

# Generar objeto Faker
faker = Faker()

filename = "datosPrueba.csv"

# Lista que almacena todoslos sectores 
lista_sectores = ["salud", "minero", "educación", "financero", "agricola", "ganadero", "comercio"]

#Crear archivo CSV con cabeceras
csvfile = open(filename, 'w', newline='')
cabeceras = ['Nombre', 'Email', 'Fecha', 'Puntaje', 'Sector', 'Pais']
writer = csv.DictWriter(csvfile, fieldnames=cabeceras)
writer.writeheader()

# Genera una lista con email y paises unicos
emails_countries_list = []
for i in range(0, 50000000):  
    emails_countries_list.append((faker.email(), faker.country()))
    emails_countries_list = list(set(emails_countries_list))
emails_countries_list2 = emails_countries_list
emails_countries_list.extend(emails_countries_list2)

# Generar lista con los datos
for i in range(100000000):
    nombre = faker.name()
    email = faker.email()
    fecha = faker.date()
    puntaje = random.randint(0,100)
    sector = random.choice(lista_sectores)
    pais = faker.country()
    listaDatos = [nombre, email, fecha, puntaje, sector, pais]

    #Escribir los datos de la lista en el archivo CSV
    writer.writerow({'Nombre':nombre, 'Email':email, 'Fecha':fecha, 'Puntaje':puntaje, 'Sector':sector, 'Pais':pais})
