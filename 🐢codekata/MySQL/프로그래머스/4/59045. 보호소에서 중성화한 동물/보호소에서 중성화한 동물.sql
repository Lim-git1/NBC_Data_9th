-- 코드를 입력하세요
SELECT i.animal_id, i.animal_type, i.name
from animal_ins i inner join animal_outs o
on i.animal_id = o.animal_id
where i.sex_upon_intake like '%intact%' and o.SEX_UPON_OUTCOME not like '%intact%'
 