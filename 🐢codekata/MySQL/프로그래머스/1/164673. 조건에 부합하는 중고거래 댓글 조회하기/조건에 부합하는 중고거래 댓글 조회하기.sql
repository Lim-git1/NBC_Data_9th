-- 코드를 입력하세요
SELECT b.title, board_id, r.reply_id, r.writer_id, r.contents, DATE_FORMAT(r.created_date, '%Y-%m-%d')
FROM used_goods_board b join used_goods_reply r
USING (board_id)
WHERE b.created_date like ('2022-10-%')
ORDER BY r.created_date asc, b.title asc