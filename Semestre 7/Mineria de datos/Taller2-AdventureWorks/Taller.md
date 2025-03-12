Docente: Daniel Lopez

## Herramientas
- SQL Server
- Power BI

## Pasos

1. Tomar la base de datos de AdventureWorks e importarla a SQL Server.
2. Buscar el diccionario de datos y el esquema relacionado con Producción y Talento Humano.
3. Generar conclusiones basadas en datos.

[AdventureWorks Data Dictionary](https://dataedo.com/download/AdventureWorks.pdf)

## Consultas SQL

1. Mostrar el monto total de ventas por producto (nombre del producto). Mostrar el nombre del producto que más se vendió.
2. Mostrar el nombre del producto cuyas ventas fueron mayores.
3. Nombre y precio de los productos que no se repitan cuyo ID sea menor de 777.
4. Con las tablas `SalesOrderHeader`, `Product`, `SalesPerson`, `Customer`: Consultar nombre del cliente, del empleado y del producto de las órdenes con precio entre 10 y 30.
5. Con las tablas `SalesOrderHeader`, `SalesTerritory`: País a donde fueron las ventas más altas.
6. Ventas por territorio para todas las filas de `SalesOrderHeader`: Traer sólo los territorios que se pasen de $10 millones en ventas históricas, traer el total de las ventas y el `TerritoryID`.
7. Usando `Production.Product`: Si el valor en color no es NULL devolver “Sin color”. Si el color sí está, devolver el color.

## Tablero en Power BI

Haga el siguiente tablero en Power BI con los datos de AdventureWorks (lo más parecido posible).
