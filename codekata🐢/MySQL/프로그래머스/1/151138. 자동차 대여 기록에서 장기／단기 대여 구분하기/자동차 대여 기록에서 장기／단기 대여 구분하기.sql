-- 코드를 입력하세요
SELECT history_id
, car_id
, date_format(start_date,'%Y-%m-%d') as start_day
, date_format(end_date,'%Y-%m-%d') as end_day
, CASE WHEN DATEDIFF(end_date,start_date)+1 >= 30 THEN '장기 대여'
ELSE '단기 대여' END AS RENT_TYPE
FROM CAR_RENTAL_COMPANY_RENTAL_HISTORY
WHERE start_date like '2022-09%'
ORDER BY history_id DESC