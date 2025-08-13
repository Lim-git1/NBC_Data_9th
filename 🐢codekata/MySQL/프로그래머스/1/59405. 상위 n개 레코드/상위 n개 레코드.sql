-- 코드를 입력하세요
SELECT name
from animal_ins
where datetime = (
    select min(datetime)
    from animal_ins
);

-- 코드를 입력하세요
SELECT name
from animal_ins
order by datetime
limit 1;