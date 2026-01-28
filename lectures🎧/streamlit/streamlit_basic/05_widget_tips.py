# 터미널 창에 입력
# 라이브러리 설치 : pip install streamlit
# Streamlit App 실행 : streamlit run .\05_widget_tips.py

import streamlit as st

st.title("위젯 활용 팁")

# =============================================================================
# 1. Session State
st.header("1. Session State")

# st.session_state: 페이지 재실행 시에도 값을 유지하는 딕셔너리
# 주요 특징:
# - 위젯 조작 시 페이지가 재실행되어도 값 유지
# - 딕셔너리처럼 키-값 형태로 데이터 저장
# - 브라우저 새로고침(F5) 시에는 초기화됨
st.write("**st.session_state:** 페이지 재실행 시에도 값을 유지하는 상태 저장소")
st.write("**용도:** 퀴즈 점수 누적, 장바구니 상품 담기, 입력 폼의 이전 입력값 유지 등")

col1, col2 = st.columns(2)

# -----------------------------------------------------------------------------
# (1) Session State 없이 - 일반 변수 (값 유지 안됨)
with col1:
    st.subheader("Session State 없이")
    normal_count = 0  # 매번 0으로 초기화됨
    if st.button("+1 증가", key="normal_btn"):
        normal_count += 1  # 버튼 클릭해도 페이지 재실행되면서 다시 0
    st.write(f"일반 변수: **{normal_count}**")
    st.error("버튼 클릭해도 항상 0 (값 유지 안됨)")

# -----------------------------------------------------------------------------
# (2) Session State 사용 - 값 유지됨
with col2:
    st.subheader("Session State 사용")
    if 'count' not in st.session_state:
        st.session_state.count = 0
    if st.button("+1 증가", key="session_btn"):
        st.session_state.count += 1
    st.write(f"Session State: **{st.session_state.count}**")
    st.success("버튼 클릭할 때마다 값 증가 (값 유지됨)")

st.info("Streamlit은 위젯 조작 시마다 전체 코드를 재실행합니다. Session State만 값을 유지할 수 있습니다.")
st.warning("브라우저 새로고침(F5) 시에는 Session State도 초기화됩니다!")

# =============================================================================
# 2. 조건부 위젯
st.divider()
st.header("2. 조건부 위젯")

# 조건부 위젯: 사용자 선택에 따라 다른 위젯을 동적으로 표시
# 주요 특징:
# - if문으로 특정 조건에서만 위젯 표시
# - 사용자 경험(UX) 향상에 유용
st.write("조건부 위젯: 사용자 선택에 따라 추가 옵션을 동적으로 표시")
st.write("**용도:** 연관 옵션 표시, 단계별 입력 폼, 맞춤형 UI 구성 시 사용")

drink = st.selectbox("음료 선택", ["아메리카노", "라떼"])

if drink == "라떼":
    milk = st.radio("우유 종류", ["일반 우유", "두유"], horizontal=True)
    st.write(f"선택: **{milk} {drink}**")
else:
    st.write(f"선택: **{drink}**")

# =============================================================================
# 3. 입력값 검증 (유효성 검사)
st.divider()
st.header("3. 입력값 검증 (유효성 검사)")

# 입력값 검증: 사용자 입력을 실시간으로 검사하여 피드백 제공
# 주요 기법:
# - len(): 문자열 길이 검사
# - isalnum(): 영문자+숫자만 포함 여부 검사
# - 정규표현식(re): 복잡한 패턴 검사
st.write("입력값 검증 (유효성 검사): 사용자 입력을 실시간으로 검사하여 즉각적인 피드백 제공")
st.write("**용도:** 회원가입 폼, 결제 정보 입력 등 유효성 검사가 필요한 경우 사용")

user_id = st.text_input("사용자 ID 입력", placeholder="4자 이상 영문자+숫자")

if user_id:
    if len(user_id) >= 4 and user_id.isalnum():
        st.success("사용 가능한 ID입니다")
    elif len(user_id) < 4:
        st.error("4자 이상 입력해주세요")
    else:
        st.error("영문자와 숫자만 사용 가능합니다")

# =============================================================================
# 4. Form - 여러 입력 일괄 처리
st.divider()
st.header("4. Form - 여러 입력 일괄 처리")

# st.form(): 여러 입력을 한 번에 제출하는 폼 컨테이너
# 주요 파라미터:
# - key: 폼의 고유 식별자
# - clear_on_submit: 제출 후 입력값 초기화 여부
# st.form_submit_button(): 폼 전용 제출 버튼
# - type: "primary" (강조) 또는 "secondary" (기본)
st.write("**st.form(key):** 여러 입력을 한 번에 제출하는 폼 컨테이너")
st.write("**용도:** 회원가입, 설문조사, 주문서 등 여러 입력을 모아서 처리할 때 사용")

# Form 사용 이유 설명
st.subheader("Form을 사용하는 이유")
st.write("**Form 없이:** 위젯 하나 조작할 때마다 전체 코드 재실행 → 입력 5개면 최대 5번 재실행")
st.write("**Form 사용:** Submit 버튼 누를 때만 1번 재실행 → 빠르고 부드러운 입력 경험")

with st.form(key="signup_form"):
    st.subheader("회원가입")

    name = st.text_input("이름")
    email = st.text_input("이메일")
    age = st.slider("나이", 0, 100, 25)
    agree = st.checkbox("약관에 동의합니다")

    # Form 안에서만 사용 가능한 제출 버튼
    submitted = st.form_submit_button("가입하기", type="primary")

    if submitted:
        if name and email and agree:
            st.success(f"{name}님, 환영합니다!")
            st.balloons()
        else:
            st.error("모든 필수 정보를 입력하고 약관에 동의해주세요")

