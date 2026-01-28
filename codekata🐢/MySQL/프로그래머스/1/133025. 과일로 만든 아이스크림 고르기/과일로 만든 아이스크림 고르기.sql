-- 코드를 입력하세요
SELECT flavor
FROM first_half h join icecream_info i
USING (flavor)
WHERE i.ingredient_type like 'fruit%' and h.total_order >= 3000
ORDER BY h.total_order DESC