USE SalesAnalytics;

-- Top 5 Customers Using RANK()
SELECT
    `Customer Name`,
    ROUND(SUM(Sales),2) AS Total_Sales,
    RANK() OVER (ORDER BY SUM(Sales) DESC) AS Customer_Rank
FROM Orders
GROUP BY `Customer Name`
LIMIT 5;

-- Top Product in Each Category (ROW_NUMBER + CTE)
WITH ProductSales AS (
    SELECT
        Category,
        `Product Name`,
        ROUND(SUM(Sales),2) AS Total_Sales,
        ROW_NUMBER() OVER (
            PARTITION BY Category
            ORDER BY SUM(Sales) DESC
        ) AS rn
    FROM Orders
    GROUP BY Category, `Product Name`
)

SELECT
    Category,
    `Product Name`,
    Total_Sales
FROM ProductSales
WHERE rn = 1;

-- Running Total of Monthly Sales
SELECT
    YEAR(`Order Date`) AS Year,
    MONTH(`Order Date`) AS Month,
    ROUND(SUM(Sales),2) AS Monthly_Sales,

    ROUND(
        SUM(SUM(Sales)) OVER(
            ORDER BY YEAR(`Order Date`),
                     MONTH(`Order Date`)
        ),2
    ) AS Running_Total

FROM Orders
GROUP BY
    YEAR(`Order Date`),
    MONTH(`Order Date`);
    
-- Previous Month Sales (LAG)
SELECT
    YEAR(`Order Date`) AS Year,
    MONTH(`Order Date`) AS Month,
    ROUND(SUM(Sales),2) AS Monthly_Sales,

    LAG(ROUND(SUM(Sales),2))
    OVER(
        ORDER BY YEAR(`Order Date`),
                 MONTH(`Order Date`)
    ) AS Previous_Month_Sales

FROM Orders
GROUP BY
    YEAR(`Order Date`),
    MONTH(`Order Date`);
    
-- Create a Sales Summary View
CREATE OR REPLACE VIEW Sales_Summary AS
SELECT
    Category,
    Region,
    ROUND(SUM(Sales),2) AS Total_Sales,
    ROUND(SUM(Profit),2) AS Total_Profit
FROM Orders
GROUP BY Category, Region;

SELECT * FROM Sales_Summary;

-- Highest Profit Product in Each Category
WITH ProfitRank AS
(
SELECT

Category,

`Product Name`,

ROUND(SUM(Profit),2) AS Profit,

DENSE_RANK() OVER
(
PARTITION BY Category
ORDER BY SUM(Profit) DESC
) AS Rank_No

FROM Orders

GROUP BY Category,`Product Name`
)

SELECT *

FROM ProfitRank

WHERE Rank_No=1;

-- Top 3 Customers in Every Region
WITH CustomerSales AS
(
SELECT

Region,

`Customer Name`,

ROUND(SUM(Sales),2) AS Sales,

ROW_NUMBER() OVER
(
PARTITION BY Region
ORDER BY SUM(Sales) DESC
) AS rn

FROM Orders

GROUP BY Region,`Customer Name`
)

SELECT *

FROM CustomerSales

WHERE rn<=3;


