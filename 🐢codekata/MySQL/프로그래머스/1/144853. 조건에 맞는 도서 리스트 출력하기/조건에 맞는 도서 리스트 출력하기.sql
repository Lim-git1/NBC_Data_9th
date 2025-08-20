-- 코드를 입력하세요
SELECT book_id, date_format(published_date,"%Y-%m-%d")
from book
where left(published_date,4) = 2021 and category = "인문"
order by published_date