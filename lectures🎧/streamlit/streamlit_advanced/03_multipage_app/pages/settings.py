# =============================================================================
# 설정 페이지 (Settings Page)
# =============================================================================
# 앱 전역 설정을 관리하는 페이지
# 여기서 변경한 설정값은 Session State에 저장되어 다른 페이지에서도 사용됨
# 예: chart_style → visualization.py에서 차트 스타일로 적용
#     display_rows → data_analysis.py에서 테이블 표시 행 수로 적용
# =============================================================================

import streamlit as st

st.set_page_config(page_title="설정 | 다중 페이지 앱", layout="wide", page_icon="⚙️")
st.title("⚙️ 설정")

# =============================================================================
# 사이드바: 설정 안내 (main.py의 placeholder 활용)
# =============================================================================
with st.session_state.sidebar_placeholder.container():
    st.header("⚙️ 설정 페이지")
    st.write("앱 전역 설정을 관리합니다.")

st.markdown("""
이 페이지에서는 앱 전역 설정을 관리합니다.
설정값은 **Session State**에 저장되어 모든 페이지에서 공유됩니다.
""")

st.divider()

# =============================================================================
# 차트 설정
# =============================================================================
# [패턴] 임시 키(_접두사) + on_change 콜백으로 영구 키에 복사
# - key="_chart_style"        → 임시 키 (페이지 이동 시 삭제되어도 OK)
# - on_change=update_...      → 값 변경 시 영구 키(chart_style)에 복사
# - value/index 초기화        → 영구 키 값으로 위젯 초기화
# =============================================================================
st.header("🎨 차트 설정")

col1, col2 = st.columns(2)

with col1:
    # 차트 스타일 - visualization.py의 sns.set_style()에서 사용
    if "chart_style" not in st.session_state:
        st.session_state.chart_style = "darkgrid"

    def update_chart_style():
        st.session_state.chart_style = st.session_state._chart_style

    chart_styles = ["darkgrid", "whitegrid", "dark", "white", "ticks"]

    current_index = chart_styles.index(st.session_state.chart_style)

    st.selectbox(
        "차트 스타일 (Seaborn)",
        options=chart_styles,
        index=current_index,  # 영구 키 값으로 초기 선택 설정
        key="_chart_style",   # 임시 키 (언더스코어 접두사)
        on_change=update_chart_style,  # 값 변경 시 영구 키에 복사
        help="시각화 페이지의 차트 스타일을 변경합니다."
    )

with col2:
    # 차트 높이 - visualization.py의 figsize 계산에 사용
    if "chart_height" not in st.session_state:
        st.session_state.chart_height = 400

    def update_chart_height():
        st.session_state.chart_height = st.session_state._chart_height

    st.slider(
        "차트 기본 높이 (px)",
        min_value=200,
        max_value=600,
        value=st.session_state.chart_height,  # 영구 키 값으로 초기화
        step=50,
        key="_chart_height",   # 임시 키
        on_change=update_chart_height  # 영구 키에 복사
    )

# =============================================================================
# 데이터 표시 설정
# =============================================================================
# data_analysis.py에서 사용되는 테이블 관련 설정
# =============================================================================
st.header("📋 데이터 표시 설정")

# 표시 행 수 - data_analysis.py의 head(display_rows)에서 사용
if "display_rows" not in st.session_state:
    st.session_state.display_rows = 100

def update_display_rows():
    st.session_state.display_rows = st.session_state._display_rows

st.number_input(
    "테이블 기본 표시 행 수",
    min_value=10,
    max_value=500,
    value=st.session_state.display_rows,
    step=10,
    key="_display_rows",
    on_change=update_display_rows
)

# =============================================================================
# 전체 초기화
# =============================================================================
# [주의] 모든 Session State를 삭제하면 앱이 초기 상태로 돌아감
# list()로 복사본을 만들어 순회해야 함 (순회 중 삭제 시 오류 방지)
# =============================================================================
st.divider()

st.warning("아래 버튼을 누르면 모든 설정이 초기화됩니다.")
if st.button("🗑️ 모든 설정 초기화", type="primary", use_container_width=True):
    # [전체 삭제] list()로 키 목록 복사 후 순회하며 삭제
    # 직접 st.session_state.keys()를 순회하면 런타임 오류 발생
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.success("모든 설정이 초기화되었습니다!")
    st.rerun()  # 앱 전체 재실행

# =============================================================================
# 페이지 하단 안내
# =============================================================================
st.divider()
