Select i.name, i.datetime
FROM animal_ins i left join animal_outs o
USING(animal_id)
where o.animal_id is null
order by i.datetime asc
limit 3