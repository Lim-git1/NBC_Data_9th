# 터미널 창에 입력
# 라이브러리 설치 : pip install streamlit
# Streamlit App 실행 : streamlit run .\01_hello.py

import streamlit as st
import datetime

# 페이지 제목
st.title("나의 첫 번째 Streamlit 앱")

# 간단한 텍스트 작성
st.write("데이터 분석 9기")

# 현재 시간 표시
st.write(f"현재 시간: {datetime.datetime.now()}")

# 이미지 작성
st.image(
    "https://i.imgur.com/f8JIo8f.jpeg",
    caption="데이터 분석 중인 귀여운 고양이",
)
