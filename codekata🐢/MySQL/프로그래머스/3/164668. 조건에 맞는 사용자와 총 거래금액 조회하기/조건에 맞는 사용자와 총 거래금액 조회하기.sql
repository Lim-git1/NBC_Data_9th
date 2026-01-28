-- 코드를 입력하세요
SELECT b.writer_id, u.nickname, b.TOTAL_PRICE
from (
select writer_id, sum(PRICE) TOTAL_PRICE
from used_goods_board
where status = 'DONE'
group by writer_id
) b INNER JOIN used_goods_user u
on b.writer_id = u.user_id
where b.TOTAL_PRICE>=700000
order by b.TOTAL_PRICE