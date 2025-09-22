-- 코드를 입력하세요
SELECT month(start_date) as MONTH, CAR_ID, COUNT(*) as RECORDS
FROM CAR_RENTAL_COMPANY_RENTAL_HISTORY
WHERE car_id in
    (SELECT CAR_ID
    FROM CAR_RENTAL_COMPANY_RENTAL_HISTORY
    where start_date BETWEEN '2022-08-01' AND '2022-10-31'
    GROUP BY car_id
    HAVING COUNT(*) >= 5) and start_date BETWEEN '2022-08-01' AND '2022-10-31'
GROUP BY month(start_date), CAR_ID HAVING COUNT(*) <> 0
ORDER BY month asc, car_id desc