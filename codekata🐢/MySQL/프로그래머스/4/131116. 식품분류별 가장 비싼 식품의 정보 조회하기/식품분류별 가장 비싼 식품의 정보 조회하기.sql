-- 코드를 입력하세요
SELECT category, price, product_name
FROM FOOD_PRODUCT
WHERE category in ("과자", "국", "김치", "식용유") 
AND price in (
    SELECT max(price)
    FROM FOOD_PRODUCT
    GROUP BY CATEGORY)
GROUP BY category
ORDER BY price DESC