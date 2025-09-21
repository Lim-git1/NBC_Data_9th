-- 코드를 입력하세요
SELECT a.author_id, a.author_name, b.category, sum(s.sales*b.price) as TOTAL_SALES
FROM BOOK b JOIN BOOK_SALES s USING(BOOK_ID)
            JOIN AUTHOR a USING(AUTHOR_ID)
WHERE LEFT(s.sales_date,7) like '2022-01%'
GROUP BY a.author_id, b.category
ORDER BY a.author_id asc, b.category desc