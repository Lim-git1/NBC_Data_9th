-- 코드를 입력하세요
select food_type, rest_id, rest_name, favorites
from rest_info
where (food_type, favorites) in (
    select food_type, max(favorites)
    from REST_INFO
    group by FOOD_TYPE)
ORDER BY FOOD_TYPE desc