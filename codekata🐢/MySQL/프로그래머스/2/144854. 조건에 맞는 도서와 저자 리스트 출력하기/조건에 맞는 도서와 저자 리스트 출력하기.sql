-- 코드를 입력하세요
SELECT b.book_id, a.author_name, date_format(b.published_date,"%Y-%m-%d")
from book b join author a
using (author_id)
where category ='경제'
order by published_date asc