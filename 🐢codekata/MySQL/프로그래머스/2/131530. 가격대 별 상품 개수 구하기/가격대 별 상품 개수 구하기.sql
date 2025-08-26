-- 코드를 입력하세요
SELECT truncate(price,-4) AS PRICE_GROUP, count(product_id) AS PRODUCTS
from product
group by 1
order by 1