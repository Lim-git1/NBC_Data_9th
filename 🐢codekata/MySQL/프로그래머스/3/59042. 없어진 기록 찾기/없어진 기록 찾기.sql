# -- 코드를 입력하세요
SELECT o.animal_id, o.name
FROM ANIMAL_INS i RIGHT JOIN ANIMAL_OUTS o
USING (animal_id)
WHERE i.datetime IS NULL
ORDER BY 1

