/* =====================================================================
   E-COMMERCE INSIGHTS  —  SQL Server (SSMS)
   Table: dbo.ecommerce_clean
   ---------------------------------------------------------------------
   Organized into 3 dashboard themes. Run each query (highlight it + F5),
   note the result, and use it to build the matching Tableau chart.
   ===================================================================== */


/* #####################################################################
   DASHBOARD 1  —  EXECUTIVE OVERVIEW
   Business question: "How is the business performing overall?"
   ##################################################################### */

-- 1.1  HEADLINE KPIs  ->  big number cards at the top of the dashboard
SELECT
    ROUND(SUM(Total_Sales), 2)     AS total_revenue,
    COUNT(*)                       AS total_orders,
    ROUND(AVG(Total_Sales), 2)     AS avg_order_value,
    ROUND(AVG(Customer_Rating), 2) AS avg_rating
FROM dbo.ecommerce_clean;

-- 1.2  REVENUE BY CATEGORY  ->  bar chart (which product line earns most?)
SELECT
    Product_Category,
    COUNT(*)                       AS orders,
    ROUND(SUM(Total_Sales), 2)     AS revenue,
    ROUND(AVG(Total_Sales), 2)     AS avg_order_value
FROM dbo.ecommerce_clean
WHERE Product_Category IS NOT NULL
GROUP BY Product_Category
ORDER BY revenue DESC;

-- 1.3  MONTHLY REVENUE TREND  ->  line chart (is the business growing?)
SELECT
    FORMAT(Order_Date, 'yyyy-MM')  AS month,
    COUNT(*)                       AS orders,
    ROUND(SUM(Total_Sales), 2)     AS revenue
FROM dbo.ecommerce_clean
WHERE Order_Date IS NOT NULL
GROUP BY FORMAT(Order_Date, 'yyyy-MM')
ORDER BY month;

-- 1.4  TOP 10 PRODUCTS BY REVENUE  ->  horizontal bar chart (star products)
SELECT TOP 10
    Product_Name,
    SUM(Quantity)                  AS units_sold,
    ROUND(SUM(Total_Sales), 2)     AS revenue
FROM dbo.ecommerce_clean
WHERE Product_Name IS NOT NULL
GROUP BY Product_Name
ORDER BY revenue DESC;


/* #####################################################################
   DASHBOARD 2  —  CUSTOMER & MARKET INSIGHTS
   Business question: "Who are our customers and where are they?"
   ##################################################################### */

-- 2.1  REVENUE BY COUNTRY  ->  map or bar chart (strongest markets)
SELECT
    Country,
    COUNT(*)                       AS orders,
    ROUND(SUM(Total_Sales), 2)     AS revenue
FROM dbo.ecommerce_clean
WHERE Country IS NOT NULL
GROUP BY Country
ORDER BY revenue DESC;

-- 2.2  TOP 10 CITIES BY REVENUE  ->  bar chart (best-performing cities)
SELECT TOP 10
    City,
    Country,
    ROUND(SUM(Total_Sales), 2)     AS revenue
FROM dbo.ecommerce_clean
WHERE City IS NOT NULL
GROUP BY City, Country
ORDER BY revenue DESC;

-- 2.3  SALES BY GENDER  ->  donut / pie (customer split)
SELECT
    Gender,
    COUNT(*)                       AS orders,
    ROUND(SUM(Total_Sales), 2)     AS revenue
FROM dbo.ecommerce_clean
WHERE Gender IS NOT NULL
GROUP BY Gender
ORDER BY revenue DESC;

-- 2.4  AGE-GROUP ANALYSIS  ->  bar chart (which age ranges spend most?)
SELECT
    CASE
        WHEN Age < 25 THEN '18-24'
        WHEN Age < 35 THEN '25-34'
        WHEN Age < 45 THEN '35-44'
        WHEN Age < 55 THEN '45-54'
        ELSE '55+'
    END                            AS age_group,
    COUNT(*)                       AS orders,
    ROUND(SUM(Total_Sales), 2)     AS revenue
FROM dbo.ecommerce_clean
WHERE Age IS NOT NULL
GROUP BY
    CASE
        WHEN Age < 25 THEN '18-24'
        WHEN Age < 35 THEN '25-34'
        WHEN Age < 45 THEN '35-44'
        WHEN Age < 55 THEN '45-54'
        ELSE '55+'
    END
ORDER BY age_group;

-- 2.5  AVERAGE RATING BY CATEGORY  ->  bar chart (satisfaction per line)
SELECT
    Product_Category,
    ROUND(AVG(Customer_Rating), 2) AS avg_rating,
    COUNT(Customer_Rating)         AS ratings_count
FROM dbo.ecommerce_clean
WHERE Product_Category IS NOT NULL AND Customer_Rating IS NOT NULL
GROUP BY Product_Category
ORDER BY avg_rating DESC;


/* #####################################################################
   DASHBOARD 3  —  PRICING & PROMOTIONS
   Business question: "Are our pricing and discounts working?"
   ##################################################################### */

-- 3.1  DISCOUNT IMPACT  ->  side-by-side bars (do discounts drive volume/revenue?)
SELECT
    CASE WHEN Discount > 0 THEN 'Discounted' ELSE 'Full Price' END AS pricing,
    COUNT(*)                       AS orders,
    ROUND(AVG(Quantity), 2)        AS avg_qty_per_order,
    ROUND(SUM(Total_Sales), 2)     AS revenue,
    ROUND(AVG(Total_Sales), 2)     AS avg_order_value
FROM dbo.ecommerce_clean
WHERE Total_Sales IS NOT NULL
GROUP BY CASE WHEN Discount > 0 THEN 'Discounted' ELSE 'Full Price' END;

-- 3.2  REVENUE BY PAYMENT METHOD  ->  bar chart (how do customers pay?)
SELECT
    Payment_Method,
    COUNT(*)                       AS orders,
    ROUND(SUM(Total_Sales), 2)     AS revenue
FROM dbo.ecommerce_clean
WHERE Payment_Method IS NOT NULL
GROUP BY Payment_Method
ORDER BY revenue DESC;

-- 3.3  AVG DISCOUNT BY CATEGORY  ->  bar chart (which lines get discounted hardest?)
SELECT
    Product_Category,
    ROUND(AVG(Discount) * 100, 1)  AS avg_discount_pct,
    ROUND(SUM(Total_Sales), 2)     AS revenue
FROM dbo.ecommerce_clean
WHERE Product_Category IS NOT NULL
GROUP BY Product_Category
ORDER BY avg_discount_pct DESC;

-- 3.4  DISCOUNT BANDS  ->  bar chart (what discount level sells best?)
SELECT
    CASE
        WHEN Discount = 0            THEN '0% (None)'
        WHEN Discount <= 0.10        THEN '1-10%'
        WHEN Discount <= 0.20        THEN '11-20%'
        WHEN Discount <= 0.30        THEN '21-30%'
        ELSE '30%+'
    END                            AS discount_band,
    COUNT(*)                       AS orders,
    ROUND(SUM(Total_Sales), 2)     AS revenue
FROM dbo.ecommerce_clean
WHERE Total_Sales IS NOT NULL
GROUP BY
    CASE
        WHEN Discount = 0            THEN '0% (None)'
        WHEN Discount <= 0.10        THEN '1-10%'
        WHEN Discount <= 0.20        THEN '11-20%'
        WHEN Discount <= 0.30        THEN '21-30%'
        ELSE '30%+'
    END
ORDER BY discount_band;