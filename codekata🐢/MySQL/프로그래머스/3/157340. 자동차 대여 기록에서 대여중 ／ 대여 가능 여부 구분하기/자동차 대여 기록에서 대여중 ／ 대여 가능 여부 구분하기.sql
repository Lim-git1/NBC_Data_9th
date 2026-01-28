-- 코드를 입력하세요
-- 1. case-when 구문을 사용해서 availability 컬럼 생성
# SELECT DISTINCT CAR_ID
#         #, start_date,end_date
#         , CASE WHEN car_id in (SELECT car_id
#                     FROM car_rental_company_rental_history
#                     WHERE '2022-10-16' BETWEEN start_date AND end_date) THEN '대여중'
#         ELSE '대여가능' END AS AVAILABILITY
# FROM CAR_RENTAL_COMPANY_RENTAL_HISTORY
# #GROUP BY car_id
# ORDER BY car_id DESC

# '2022-10-16' BETWEEN start_date AND end_date
# start_date < '2022-10-16' AND end_date >= '2022-10-16'
#, CASE WHEN LEFT(max(start_date),10) < '2022-10-16' and LEFT(max(end_date),10) >= '2022-10-16' THEN '대여중'

select distinct CAR_ID, 
    case 
        when CAR_ID in (
            select CAR_ID
            from CAR_RENTAL_COMPANY_RENTAL_HISTORY
            where '2022-10-16' between START_DATE and END_DATE
        ) then '대여중'
        else '대여 가능'
        end as AVAILABILITY
from CAR_RENTAL_COMPANY_RENTAL_HISTORY
order by CAR_ID desc;