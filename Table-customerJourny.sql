WITH CleanedData AS (
    SELECT 
        JourneyID,  
        CustomerID,  
        ProductID,  
        VisitDate,  
        UPPER(Stage) AS Stage,  -- Conversion en majuscules pour éviter les différences de casse
        Action,  
        COALESCE(Duration, AVG(Duration) OVER (PARTITION BY VisitDate)) AS Duration,  -- Remplacer la durée manquante par la moyenne
        ROW_NUMBER() OVER (
            PARTITION BY CustomerID, ProductID, VisitDate, UPPER(Stage), Action  -- Partitionner pour identifier les doublons
            ORDER BY JourneyID  -- Garder le premier enregistrement dans chaque partition
        ) AS row_num  
    FROM 
        dbo.customer_journey  -- Table d'origine
)

SELECT 
    JourneyID,  
    CustomerID,  
    ProductID,  
    VisitDate,  
    Stage,  
    Action,  
    Duration
FROM 
    CleanedData
WHERE 
    row_num = 1;  -- Garder uniquement la première ligne dans chaque partition (sans doublons)
