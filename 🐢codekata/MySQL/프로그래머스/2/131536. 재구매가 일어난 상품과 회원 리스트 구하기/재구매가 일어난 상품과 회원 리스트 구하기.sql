# # -- 코드를 입력하세요
# with sub_table as (
#     SELECT user_id, product_id
#     FROM online_sale
#     GROUP BY user_id
#     HAVING count(user_id) >= 2
# )

# SELECT * #a.user_id, a.product_id
# FROM online_sale a LEFT join sub_table b
# USING (user_id)
# where b.product_id is not null
# ORDER BY 1 ASC, 2 DESC

select user_id,product_id
from (
    select user_id,product_id, count(product_id) OVER (PARTITION BY user_id, product_id) as cnt
    from online_sale
) a
where cnt >= 2
group by product_id, user_id
order by user_id asc, product_id desc
