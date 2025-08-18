-- 코드를 입력하세요
SELECT PT_NAME, PT_NO, GEND_CD, AGE, 
if (TLNO is null, 'NONE',TLNO)
from patient
where age <= 12 and gend_cd ='W'
order by 4 desc, 1 asc