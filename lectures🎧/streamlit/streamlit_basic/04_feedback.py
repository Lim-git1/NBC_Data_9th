# 터미널 창에 입력
# 라이브러리 설치 : pip install streamlit
# Streamlit App 실행 : streamlit run .\03_feedback.py

import streamlit as st
import time

# =============================================================================
# 1. 토스트 알림 (Status elements)
# =============================================================================
st.header("1. 토스트 알림 (Status Elements)")

# st.toast(): 화면 우측 하단에 잠시 나타났다 사라지는 알림
# 주요 파라미터:
# - body: 알림 메시지 텍스트
# - icon: 아이콘 (이모지 또는 :material/아이콘명: 형식)
st.write("**st.toast(body, icon):** 잠시 나타났다 사라지는 팝업 알림")
st.write("**용도:** 저장 완료, 설정 변경 등 사용자에게 간단한 피드백 제공 시 사용")

if st.button("성공 알림"):
    st.toast("파일이 저장되었습니다!", icon="✅")


# =============================================================================
# 2. 스피너 (Status elements > Show progress)
# =============================================================================
st.divider()
st.header("2. 스피너 (Show Progress)")

# st.spinner(): 작업 진행 중임을 나타내는 로딩 애니메이션
# 주요 파라미터:
# - text: 로딩 중 표시할 메시지 (기본값: "In progress...")
# - cache: 캐싱 데코레이터와 함께 사용 시 로딩 상태 표시
st.write("**st.spinner(text):** 작업 진행 중 로딩 애니메이션 표시")
st.write("**용도:** API 호출, 데이터 처리 등 시간이 걸리는 작업 대기 시 사용")

if st.button("데이터 로딩"):
    with st.spinner("데이터를 불러오는 중..."):
        time.sleep(3)  # 실제 작업 시간 시뮬레이션
    st.success("데이터 로딩 완료!")

# =============================================================================
# 3. 진행률 표시 (Status elements > Show progress)
# =============================================================================
st.divider()
st.header("3. 진행률 표시 (Show Progress)")

# st.progress(): 진행률을 시각적으로 보여주는 프로그레스 바
# 주요 파라미터:
# - value: 진행률 (0~100 정수 또는 0.0~1.0 실수)
# - text: 프로그레스 바 위에 표시할 텍스트
st.write("**st.progress(value, text):** 작업 진행률을 나타내는 프로그레스 바")
st.write("**용도:** 파일 업로드/다운로드, 대량 데이터 처리 등 진행 상황 표시 시 사용")

if st.button("파일 업로드"):
    progress_bar = st.progress(0, text="업로드 준비 중...")
    for i in range(100):
        time.sleep(0.01)  # 실제 업로드 시간 시뮬레이션
        progress_bar.progress(i + 1, text=f"업로드 중... {i + 1}%")
    progress_bar.progress(100, text="업로드 완료!")
    st.success("파일 업로드 완료!")

# =============================================================================
# 4. 상태 컨테이너 (Status elements > Show progress)
# =============================================================================
st.divider()
st.header("4. 상태 컨테이너 (Show Progress)")

# st.status(): 단계별 진행 상황을 보여주는 확장 가능한 컨테이너
# 주요 파라미터:
# - label: 상태 컨테이너의 제목
# - expanded: 초기 확장 상태 (True/False)
# - state: 상태 ("running", "complete", "error")
st.write("**st.status(label, expanded, state):** 단계별 진행 상황을 보여주는 상태 컨테이너")
st.write("**용도:** 배포, 설치, 다단계 처리 등 여러 단계의 진행 상황 표시 시 사용")

if st.button("배포 프로세스"):
    with st.status("애플리케이션 배포 중...", expanded=True) as status:
        st.write("1️⃣ 코드 검사 중...")
        time.sleep(1)
        st.write("2️⃣ 빌드 중...")
        time.sleep(1)
        st.write("3️⃣ 테스트 실행 중...")
        time.sleep(1)
        st.write("4️⃣ 서버에 배포 중...")
        time.sleep(1)
        # status.update(): 상태 컨테이너의 라벨, 상태, 확장 여부를 업데이트
        status.update(label="배포 완료!", state="complete", expanded=False)

# =============================================================================
# 5. 축하 애니메이션 (Status elements > Celebrate)
# =============================================================================
st.divider()
st.header("5. 축하 애니메이션 (Celebrate)")

# st.balloons(): 풍선 애니메이션 표시 (성공, 완료 등 축하 상황에 사용)
# st.snow(): 눈 내리는 애니메이션 표시 (겨울 테마, 특별 이벤트 등에 사용)
st.write("**st.balloons() / st.snow():** 화면 전체에 애니메이션 효과 표시")
st.write("**용도:** 목표 달성, 회원가입 완료, 이벤트 등 축하 상황에서 사용")

# 화면을 2개의 열로 분할하여 버튼 배치
col1, col2 = st.columns(2)

with col1:
    if st.button("🎈 풍선 날리기"):
        st.balloons()

with col2:
    if st.button("❄️ 눈 내리기"):
        st.snow()

# =============================================================================
# 6. 예외 처리 출력 (Status elements)
# =============================================================================
st.divider()
st.header("6. 예외 처리 출력 (Status Elements)")

# st.exception(): 예외(Exception) 정보를 보기 좋게 출력
# 주요 파라미터:
# - exception: 출력할 Exception 객체
st.write("**st.exception(exception):** 예외 정보를 디버깅하기 쉽게 출력")
st.write("**용도:** 개발/디버깅 시 에러 추적, 사용자에게 상세한 오류 정보 제공 시 사용")

try:
    # 일부러 에러 발생시키기
    result = 1 / 0
except Exception as e:
    st.exception(e)
