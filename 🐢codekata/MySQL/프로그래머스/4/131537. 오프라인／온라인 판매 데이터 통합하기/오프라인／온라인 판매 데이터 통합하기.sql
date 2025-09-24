-- 코드를 입력하세요
(SELECT date_format(SALES_DATE, '%Y-%m-%d') SALES_DATE
        , PRODUCT_ID
        , USER_ID
        , SALES_AMOUNT
FROM online_sale
WHERE sales_date like '2022-03%')
UNION ALL
(SELECT date_format(SALES_DATE, '%Y-%m-%d') SALES_DATE
        , PRODUCT_ID
        , NULL 'USER_ID'
        , SALES_AMOUNT
FROM offline_sale
WHERE sales_date like '2022-03%')
ORDER BY sales_date asc, product_id asc, user_id asc