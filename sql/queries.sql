-- Q1: Total customers
SELECT COUNT(*) AS total_customers
FROM customers;
 
-- Q2: Order status distribution
SELECT status, COUNT(*) AS total_orders
FROM orders
GROUP BY status;
 
-- Q3: Completed order revenue
SELECT ROUND(SUM(order_amount), 2) AS completed_revenue
FROM orders
WHERE LOWER(status) = 'completed';
 
-- Q4: Customer-wise order count
SELECT customer_id, COUNT(*) AS total_orders
FROM orders
GROUP BY customer_id
ORDER BY total_orders DESC;
 
-- Q5: Customers with more than 5 orders
SELECT customer_id, COUNT(*) AS order_count
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 5;
 
-- Q6: Average order amount by product category
WITH category_orders AS (
    SELECT p.category, o.order_amount
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    WHERE LOWER(o.status) = 'completed'
)
SELECT category, ROUND(AVG(order_amount), 2) AS average_order_amount
FROM category_orders
GROUP BY category;
 
-- Q7: Rank customers by spending
SELECT
    customer_id,
    SUM(order_amount) AS total_spending,
    RANK() OVER (ORDER BY SUM(order_amount) DESC) AS spending_rank
FROM orders
WHERE LOWER(status) = 'completed'
GROUP BY customer_id;
 