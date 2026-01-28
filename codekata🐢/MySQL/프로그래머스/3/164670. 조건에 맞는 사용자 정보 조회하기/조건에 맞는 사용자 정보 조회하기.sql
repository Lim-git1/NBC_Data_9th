-- 코드를 입력하세요
SELECT a.writer_id
, b.nickname
, concat(b.city," ",b.street_address1," ",b.street_address2) as "전체주소"
, concat(left(b.tlno,3),'-',mid(b.tlno,4,4),'-',right(b.tlno,4)) as "전화번호"
FROM used_goods_board a join used_goods_user b
on a.writer_id = b.user_id
group by a.writer_id
having count(a.writer_id) >= 3
order by b.user_id desc
