# 0부터 23까지의 시간(h)을 생성하는 재귀 CTE 
WITH RECURSIVE hours AS (
     SELECT 0 AS hour 
     UNION ALL 
     SELECT hour + 1 
     FROM hours 
     WHERE hour < 23 )

SELECT h.hour, count(a.datetime) COUNT
FROM hours h LEFT JOIN animal_outs a
ON hour(a.datetime) = h.hour
GROUP BY HOUR
ORDER BY HOUR