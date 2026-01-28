-- 코드를 입력하세요
SELECT distinct a.car_id AS CAR_ID
from CAR_RENTAL_COMPANY_CAR a join CAR_RENTAL_COMPANY_RENTAL_HISTORY b 
using (car_id)
where a.car_type = '세단' and month(b.start_date) = 10
order by 1 desc