-- 코드를 입력하세요
#SELECT animal_type , if (name is not null,name,'no name') 'name', sex_upon_intake
SELECT ANIMAL_TYPE, IFNULL(NAME,'No name') AS NAME, SEX_UPON_INTAKE
FROM ANIMAL_INS
ORDER BY ANIMAL_ID ASC