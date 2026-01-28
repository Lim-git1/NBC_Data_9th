-- 코드를 입력하세요
SELECT i.animal_id, i.name
from animal_ins i right join animal_outs o on i.animal_id = o.animal_id
where i.animal_id is not null
order by (o.datetime - i.datetime) desc
limit 2