
SELECT ProductID,ProductName, Price,
CASE 
	WHEN price < 50 THEN 'low'
	WHEN price BETWEEN 50 AND 200 THEN 'Medium'
	ELSE 'Hight'
END AS PriceCategory

FROM  dbo.products