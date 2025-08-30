-- 진료예약번호, 환자이름, 환자번호, 진료과코드, 의사이름, 진료예약일시
SELECT a.apnt_no, p.pt_name, p.pt_no, d.mcdp_cd,d.dr_name, a.apnt_ymd
FROM APPOINTMENT a LEFT JOIN PATIENT p USING (PT_NO)
                LEFT JOIN DOCTOR d ON a.MDDR_ID = d.DR_ID
WHERE a.apnt_ymd like '%2022-04-13%' and d.mcdp_cd = 'CS' and a.apnt_cncl_yn = 'N'
ORDER BY a.apnt_ymd