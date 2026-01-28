-- 코드를 입력하세요
SELECT a.product_id, a.product_name, sum(a.price*b.amount) AS TOTAL_SALES
FROM food_product a join food_order b
USING (product_id)
WHERE b.produce_date like '2022-05%'
GROUP BY a.product_id
ORDER BY 3 DESC, 1 ASC