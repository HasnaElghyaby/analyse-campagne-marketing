
SELECT  c.CustomerID,
		c.CustomerName,
		c.Email,
		c.Age,
		c.Gender,
		g.country,
		g.city

FROM customers c
LEFT JOIN geography g ON c.GeographyID = g.GeographyID