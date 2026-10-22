CREATE DATABASE marketing_analytics;

USE marketing_analytics;

CREATE TABLE customers (
    ID INT PRIMARY KEY,
    Year_Birth INT,
    Education VARCHAR(50),
    Marital_Status VARCHAR(50),
    Income DECIMAL(12,2),
    Kidhome INT,
    Teenhome INT,
    Dt_Customer DATE,
    Recency INT,
    MntWines DECIMAL(12,2),
    MntFruits DECIMAL(12,2),
    MntMeatProducts DECIMAL(12,2),
    MntFishProducts DECIMAL(12,2),
    MntSweetProducts DECIMAL(12,2),
    MntGoldProds DECIMAL(12,2),
    NumDealsPurchases INT,
    NumWebPurchases INT,
    NumCatalogPurchases INT,
    NumStorePurchases INT,
    NumWebVisitsMonth INT,
    AcceptedCmp1 TINYINT,
    AcceptedCmp2 TINYINT,
    AcceptedCmp3 TINYINT,
    AcceptedCmp4 TINYINT,
    AcceptedCmp5 TINYINT,
    Response TINYINT,
    Complain TINYINT
);
CREATE VIEW customer_analytics AS
SELECT
    ID,
    Year_Birth,
    2025 - Year_Birth AS Age,
    Education,
    Marital_Status,
    Income,
    Kidhome + Teenhome AS Children,

    MntWines +
    MntFruits +
    MntMeatProducts +
    MntFishProducts +
    MntSweetProducts +
    MntGoldProds AS Total_Spend,

    NumDealsPurchases +
    NumWebPurchases +
    NumCatalogPurchases +
    NumStorePurchases AS Total_Purchases,

    NumWebVisitsMonth,

    AcceptedCmp1,
    AcceptedCmp2,
    AcceptedCmp3,
    AcceptedCmp4,
    AcceptedCmp5,
    Response,

    AcceptedCmp1 +
    AcceptedCmp2 +
    AcceptedCmp3 +
    AcceptedCmp4 +
    AcceptedCmp5 +
    Response AS Total_Campaign_Accepted

FROM customers;


SELECT
    COUNT(*) AS Total_Customers,
    ROUND(AVG(Income), 2) AS Avg_Income,
    ROUND(AVG(Total_Spend), 2) AS Avg_Spend,
    ROUND(AVG(Total_Purchases), 2) AS Avg_Purchases,
    ROUND(AVG(NumWebVisitsMonth), 2) AS Avg_Web_Visits,
    ROUND(AVG(Response) * 100, 2) AS Response_Rate
FROM customer_analytics;

SELECT
    Education,
    COUNT(*) AS Customers,
    SUM(Response) AS Responders,
    ROUND(AVG(Response) * 100, 2) AS Response_Rate,
    ROUND(AVG(Total_Spend), 2) AS Avg_Spend
FROM customer_analytics
GROUP BY Education
ORDER BY Response_Rate DESC;


SELECT
    CASE
        WHEN Age < 30 THEN '18-29'
        WHEN Age < 40 THEN '30-39'
        WHEN Age < 50 THEN '40-49'
        WHEN Age < 60 THEN '50-59'
        ELSE '60+'
    END AS Age_Band,

    COUNT(*) AS Customers,
    ROUND(AVG(Response) * 100, 2) AS Response_Rate,
    ROUND(AVG(Total_Spend), 2) AS Avg_Spend

FROM customer_analytics
GROUP BY Age_Band
ORDER BY Response_Rate DESC;

SELECT
    ROUND(AVG(AcceptedCmp1) * 100, 2) AS Campaign1_Rate,
    ROUND(AVG(AcceptedCmp2) * 100, 2) AS Campaign2_Rate,
    ROUND(AVG(AcceptedCmp3) * 100, 2) AS Campaign3_Rate,
    ROUND(AVG(AcceptedCmp4) * 100, 2) AS Campaign4_Rate,
    ROUND(AVG(AcceptedCmp5) * 100, 2) AS Campaign5_Rate,
    ROUND(AVG(Response) * 100, 2) AS Latest_Response_Rate
FROM customers;


WITH ranked_customers AS (
    SELECT *,
           NTILE(10) OVER (
               ORDER BY
               MntWines +
               MntFruits +
               MntMeatProducts +
               MntFishProducts +
               MntSweetProducts +
               MntGoldProds
           ) AS spend_decile
    FROM customers
)

SELECT
    AVG(NumWebPurchases) AS Avg_Web_Purchases,
    AVG(NumCatalogPurchases) AS Avg_Catalog_Purchases,
    AVG(NumStorePurchases) AS Avg_Store_Purchases,
    AVG(NumDealsPurchases) AS Avg_Deal_Purchases,
    AVG(NumWebVisitsMonth) AS Avg_Web_Visits
FROM ranked_customers
WHERE spend_decile = 10;
