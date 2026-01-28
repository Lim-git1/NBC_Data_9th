-- 코드를 입력하세요
SELECT a.product_code, sum(b.sales_amount*a.price)
FROM product a join offline_sale b on a.product_id = b.product_id
group by 1
order by 2 desc, 1 asc