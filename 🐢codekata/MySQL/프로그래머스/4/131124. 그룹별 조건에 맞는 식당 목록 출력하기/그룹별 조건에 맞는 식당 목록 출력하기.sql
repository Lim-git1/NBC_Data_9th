-- 1) 회원별 리뷰 수 집계
WITH review_counts AS (
  SELECT member_id, COUNT(*) AS cnt
  FROM REST_REVIEW
  GROUP BY member_id
),
-- 2) 최다 리뷰 회원(동률 포함) 추리기
top_members AS (
  SELECT member_id
  FROM review_counts
  WHERE cnt = (SELECT MAX(cnt) FROM review_counts)
)
-- 3) 해당 회원들의 리뷰를 회원명과 함께 조회
SELECT
  m.member_name,
  r.review_text,
  DATE_FORMAT(r.review_date, '%Y-%m-%d') AS review_date
FROM REST_REVIEW r JOIN top_members t
USING (member_id)
JOIN MEMBER_PROFILE m
USING (member_id)
ORDER BY r.review_date ASC, r.review_text ASC;