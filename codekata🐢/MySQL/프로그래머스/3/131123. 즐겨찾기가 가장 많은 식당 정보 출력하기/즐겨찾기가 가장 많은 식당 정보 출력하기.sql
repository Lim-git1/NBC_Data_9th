-- 코드를 입력하세요
# 첫 제출안
# XX <-- favorites만 비교하여서 최대 즐겨찾기 수와 즐겨찾기 수만 같다면, 다른 타입의 음식도 모두 출력됨
select food_type, rest_id, rest_name, favorites
from rest_info
where favorites in (
    select food_type, max(favorites)
    from REST_INFO
    group by FOOD_TYPE)
GROUP BY REST_ID
ORDER BY FOOD_TYPE desc

# 수정안
select food_type, rest_id, rest_name, favorites
from rest_info
where (food_type, favorites) in (
    select food_type, max(favorites)
    from REST_INFO
    group by FOOD_TYPE)
ORDER BY FOOD_TYPE desc
