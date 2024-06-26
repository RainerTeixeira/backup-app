SELECT *
FROM Sales.SalesOrderHeader



SELECT *
FROM Sales.SalesOrderHeader


SELECT SalesOrderID, DATEPART(DD,OrderDate) as Dia,DATEPART(MM,OrderDate) as Mes, DATEPART(YYYY,OrderDate) as Ano
FROM Sales.SalesOrderHeader

SELECT *
FROM Sales.SalesOrderHeader


SELECT AVG(TotalDue) as Media, DATEPART(YY,OrderDate) as Mes
FROM Sales.SalesOrderHeader
GROUP BY DATEPART(YY,OrderDate)
ORDER BY Mes;