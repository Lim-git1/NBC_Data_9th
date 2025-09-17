-- 조회수가 가장 높은 중고거래 게시물에 대한 첨부파일 경로를 조회
SELECT concat('/home/grep/src/',f.board_id,'/', f.file_id,f.file_name, f.file_ext) as FILE_PATH
FROM used_goods_board b join used_goods_file f
USING (board_id)
WHERE b.views = (SELECT MAX(views)
                FROM used_goods_board)
ORDER BY f.file_id DESC