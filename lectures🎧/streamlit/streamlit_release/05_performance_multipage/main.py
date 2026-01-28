# 터미널 창에 입력
# Streamlit App 실행 : streamlit run .\05_performance_multipage\main.py

import streamlit as st

# =============================================================================
# 앱 전체 설정
# =============================================================================
st.set_page_config(
    page_title="성능 최적화 (멀티페이지)",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# 페이지 정의 (st.Page)
# =============================================================================
home_page = st.Page(
    page="pages/home.py",
    title="홈",
    icon="🏠",
    default=True
)

track_page = st.Page(
    page="pages/track_analysis.py",
    title="트랙 분석",
    icon="🎵"
)

artist_page = st.Page(
    page="pages/artist_analysis.py",
    title="아티스트 분석",
    icon="🎤"
)

sales_page = st.Page(
    page="pages/sales_analysis.py",
    title="매출 분석",
    icon="💰"
)

# =============================================================================
# 네비게이션 구성 (st.navigation)
# =============================================================================
pg = st.navigation({
    "메인": [home_page],
    "분석": [track_page, artist_page, sales_page]
})

# =============================================================================
# 공통 사이드바
# =============================================================================
with st.sidebar:
    st.caption("© 2025 Streamlit 심화")

# =============================================================================
# 페이지 실행
# =============================================================================
pg.run()
