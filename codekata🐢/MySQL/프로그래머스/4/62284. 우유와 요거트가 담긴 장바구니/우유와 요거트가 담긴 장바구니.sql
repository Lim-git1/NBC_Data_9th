
-- 우유 혹은 요거트 구매한 장바구니 목록
WITH L AS (
    SELECT CART_ID, NAME
    FROM CART_PRODUCTS
    HAVING NAME IN ('Milk','Yogurt')
)
-- 둘다 구매한 장바구니
SELECT CART_ID
FROM L
GROUP BY 1
HAVING COUNT(DISTINCT NAME) >= 2 -- 둘다 구매