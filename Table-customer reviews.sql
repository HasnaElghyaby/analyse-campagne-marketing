SELECT 
		ReviewID,
		CustomerID,
		ProductID,
		ReviewDate,
		Rating,
		REPLACE(ReviewText,'  ',' ') as ReviewText
FROM dbo.customer_reviews
