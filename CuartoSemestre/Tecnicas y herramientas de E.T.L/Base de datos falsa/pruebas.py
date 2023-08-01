lista1 = [x for x in range(5)]

lista2 = [x for x in range(5, 10)]
lista3 = [x for x in range(5, 10)]
lista1.extend(lista2)
lista1.extend(lista3)
print(lista1)