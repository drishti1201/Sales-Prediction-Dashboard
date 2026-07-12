CREATE DATABASE SalesAnalytics;
USE SalesAnalytics;
SELECT * FROM Orders LIMIT 10; 

-- Total Sales
SELECT ROUND(SUM(Sales),2) AS Total_Sales
FROM Orders;

-- Total Profit
SELECT ROUND(SUM(Profit),2) AS Total_Profit
FROM Orders;

-- Total Orders
SELECT COUNT(DISTINCT `Order ID`) AS Total_Orders
FROM Orders;

-- Total Customers
SELECT COUNT(DISTINCT `Customer ID`) AS Total_Customers
FROM Orders;

-- Total Products
SELECT COUNT(DISTINCT `Product Name`) AS Total_Products
FROM Orders;

-- Sales by Category
SELECT Category,
ROUND(SUM(Sales),2) AS Sales
FROM Orders
GROUP BY Category
ORDER BY Sales DESC;

-- Profit by Category
SELECT Category,
ROUND(SUM(Profit),2) AS Profit
FROM Orders
GROUP BY Category
ORDER BY Profit DESC;

-- Region-wise Sales
SELECT Region,
ROUND(SUM(Sales),2) AS Sales
FROM Orders
GROUP BY Region
ORDER BY Sales DESC;

-- op 10 Customers
SELECT
`Customer Name`,
ROUND(SUM(Sales),2) AS TotalSales
FROM Orders
GROUP BY `Customer Name`
ORDER BY TotalSales DESC
LIMIT 10;

-- Top 10 Products
SELECT
`Product Name`,
ROUND(SUM(Sales),2) AS TotalSales
FROM Orders
GROUP BY `Product Name`
ORDER BY TotalSales DESC
LIMIT 10;



