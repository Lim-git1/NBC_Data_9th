-- 코드를 입력하세요
SELECT cart_id
FROM (
    SELECT id, cart_id, GROUP_CONCAT(name) as name
    FROM CART_PRODUCTS
    GROUP BY cart_id
    ) a
WHERE name like '%Milk%' and name like '%Yogurt%'
ORDER BY cart_id