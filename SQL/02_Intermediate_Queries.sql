USE SalesAnalytics;

-- Monthly Sales Trend
SELECT
    YEAR(`Order Date`) AS Year,
    MONTH(`Order Date`) AS Month_No,
    MONTHNAME(`Order Date`) AS Month,
    ROUND(SUM(Sales),2) AS Total_Sales
FROM Orders
GROUP BY
    YEAR(`Order Date`),
    MONTH(`Order Date`),
    MONTHNAME(`Order Date`)
ORDER BY
    Year,
    Month_No;
    
-- Year-wise Sales
SELECT
    YEAR(`Order Date`) AS Year,
    ROUND(SUM(Sales),2) AS Total_Sales
FROM Orders
GROUP BY YEAR(`Order Date`)
ORDER BY Year;

-- Sales by Segment
SELECT
    Segment,
    ROUND(SUM(Sales),2) AS Total_Sales,
    ROUND(SUM(Profit),2) AS Total_Profit
FROM Orders
GROUP BY Segment
ORDER BY Total_Sales DESC;

-- Top 10 States by Sales
SELECT
    State,
    ROUND(SUM(Sales),2) AS Total_Sales
FROM Orders
GROUP BY State
ORDER BY Total_Sales DESC
LIMIT 10;

-- Top 10 Cities by Sales
SELECT
    City,
    ROUND(SUM(Sales),2) AS Total_Sales
FROM Orders
GROUP BY City
ORDER BY Total_Sales DESC
LIMIT 10;

-- Average Order Value
SELECT
    ROUND(SUM(Sales) / COUNT(DISTINCT `Order ID`),2) AS Average_Order_Value
FROM Orders;

-- Profit Margin
SELECT
    ROUND((SUM(Profit) / SUM(Sales)) * 100,2) AS Profit_Margin_Percentage
FROM Orders;

-- Discount Analysis
SELECT
    Discount,
    COUNT(*) AS Total_Orders,
    ROUND(SUM(Sales),2) AS Total_Sales,
    ROUND(SUM(Profit),2) AS Total_Profit
FROM Orders
GROUP BY Discount
ORDER BY Discount;

-- Sales by Sub-Category
SELECT
    `Sub-Category`,
    ROUND(SUM(Sales),2) AS Total_Sales
FROM Orders
GROUP BY `Sub-Category`
ORDER BY Total_Sales DESC;

-- Loss-Making Products
SELECT
    `Product Name`,
    ROUND(SUM(Profit),2) AS Total_Profit
FROM Orders
GROUP BY `Product Name`
HAVING Total_Profit < 0
ORDER BY Total_Profit;
