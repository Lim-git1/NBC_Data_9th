-- 코드를 입력하세요
SELECT i.INGREDIENT_TYPE, sum(total_order) AS TOTAL_ORDER
from first_half f join icecream_info i
using (flavor)
group by i.INGREDIENT_TYPE
order by sum(total_order) asc