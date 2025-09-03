-- 코드를 입력하세요
SELECT YEAR(b.sales_date) AS YEAR, MONTH(b.sales_date) AS MONTH, a.GENDER, COUNT(DISTINCT (a.user_id)) AS USERS
FROM user_info a JOIN online_sale b
USING (user_id)
WHERE a.gender is not null
GROUP BY a.GENDER, MONTH,YEAR
ORDER BY 1, 2, 3