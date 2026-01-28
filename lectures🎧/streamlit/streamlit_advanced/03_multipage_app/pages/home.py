# =============================================================================
# 홈 페이지 (Home Page)
# =============================================================================

import streamlit as st

st.set_page_config(page_title="홈 | 다중 페이지 앱", layout="wide", page_icon="🏠")
st.title("🏠 다중 페이지 앱 실습")

# =============================================================================
# 사이드바: 환영 메시지 (main.py의 placeholder 활용)
# =============================================================================
with st.session_state.sidebar_placeholder.container():
    st.header("👋 환영합니다!")
    st.write("사이드바에서 페이지를 선택하세요.")

# =============================================================================
# 앱 소개
# =============================================================================
st.header("Streamlit 다중 페이지 앱 구조 학습")

st.markdown("""
이 앱은 **Streamlit의 다중 페이지 기능**을 학습하기 위한 실습 자료입니다.

### 학습 내용
- `st.Page`와 `st.navigation`을 활용한 페이지 구성
- 페이지 간 상태(Session State) 공유
- 공통 레이아웃과 개별 페이지 레이아웃 구성
""")

# =============================================================================
# 앱 구조 설명
# =============================================================================
st.divider()
st.header("📁 앱 구조")

col1, col2 = st.columns(2)

with col1:
    st.subheader("파일 구조")
    st.code("""
03_multipage_app/
├── main.py              # 엔트리 포인트 (진입점)
└── pages/
    ├── home.py          # 홈 페이지 (현재)
    ├── data_analysis.py # 데이터 분석 페이지
    ├── visualization.py # 시각화 페이지
    └── settings.py      # 설정 페이지
    """, language="text")

with col2:
    st.subheader("핵심 코드 (main.py)")
    st.code("""
import streamlit as st

# 페이지 정의
home_page = st.Page("pages/home.py", title="홈", icon="🏠", default=True)
data_page = st.Page("pages/data_analysis.py", title="데이터 분석", icon="📊")
viz_page = st.Page("pages/visualization.py", title="시각화", icon="📈")
settings_page = st.Page("pages/settings.py", title="설정", icon="⚙️")

# 네비게이션 구성 (딕셔너리로 섹션 구분)
pg = st.navigation({
    "메인": [home_page],
    "분석 도구": [data_page, viz_page],
    "관리": [settings_page]
})

# 공통 사이드바 요소
with st.sidebar:
    st.caption("© 2025 다중 페이지 앱 실습")

# 선택된 페이지 실행 (필수!)
pg.run()
    """, language="python")

# =============================================================================
# 페이지 소개 카드
# =============================================================================
st.divider()
st.header("📑 페이지 소개")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True, height=280):
        st.subheader("📊 데이터 분석")
        st.write("데이터프레임 조작과 필터링을 학습합니다.")
        st.write("- 캘리포니아 주택 데이터 활용")
        st.write("- 인터랙티브 필터 구현")
        st.write("- Session State 활용")

with col2:
    with st.container(border=True, height=280):
        st.subheader("📈 시각화")
        st.write("다양한 차트 생성 방법을 학습합니다.")
        st.write("- Matplotlib/Seaborn 연동")
        st.write("- Streamlit 내장 차트")
        st.write("- 인터랙티브 차트")

with col3:
    with st.container(border=True, height=280):
        st.subheader("⚙️ 설정")
        st.write("앱 전역 설정을 관리합니다.")
        st.write("- Session State 관리")
        st.write("- 페이지 간 상태 공유")
        st.write("- 설정 초기화")

# =============================================================================
# Session State 소개
# =============================================================================
st.divider()
st.header("🔄 Session State 개요")

st.info("""
**Session State**는 페이지 간 데이터를 공유하는 핵심 메커니즘입니다.

- `st.session_state["key"]`로 값을 저장/조회
- 브라우저 세션이 유지되는 동안 값이 보존됨
- 위젯의 `key` 파라미터로 자동 연동 가능
- 👈 **사이드바에서 현재 Session State를 확인할 수 있습니다!**
""")

# =============================================================================
# 시작하기
# =============================================================================
st.divider()
st.success("👈 왼쪽 사이드바에서 페이지를 선택하여 시작하세요!")
