# 터미널 창에 입력
# 라이브러리 설치 : pip install streamlit pandas seaborn matplotlib
# Streamlit App 실행 : streamlit run main.py

import streamlit as st

# =============================================================================
# 앱 전체 설정 (st.set_page_config)
# =============================================================================
# [중요] st.set_page_config는 반드시 다른 Streamlit 명령보다 먼저 호출해야 함
# 다중 페이지 앱에서는 main.py(엔트리 포인트)에서 한 번만 설정하는 것을 권장
#
# [주요 파라미터]
# - page_title: 브라우저 탭에 표시되는 제목 (기본값: 파일명)
# - page_icon: 브라우저 탭 아이콘 (이모지, 이미지 URL, 파일 경로)
# - layout: "centered"(기본값) 또는 "wide" (전체 너비)
# - initial_sidebar_state: "auto" (자동), "expanded" (펼침), "collapsed" (접힘)
# - menu_items: 우측 상단 햄버거 메뉴 커스터마이징
# =============================================================================
st.set_page_config(
    page_title="다중 페이지 앱 실습",       # 브라우저 탭 제목
    page_icon="📚",                        # 브라우저 탭 아이콘
    layout="wide",                         # 넓은 레이아웃
    initial_sidebar_state="expanded",      # 사이드바 기본 펼침
    menu_items={
        'Get Help': 'https://docs.streamlit.io',
        'Report a bug': None,              # None으로 설정하면 메뉴에서 숨김
        'About': """
        ## 다중 페이지 앱 실습
        Streamlit의 `st.Page`와 `st.navigation`을 활용한 다중 페이지 앱 튜토리얼입니다.

        **학습 내용**:
        - 다중 페이지 구조 설계
        - Session State를 통한 페이지 간 상태 공유
        - 공통 레이아웃 구성
        """
    }
)

# =============================================================================
# Streamlit 다중 페이지 앱 (Multi-Page App) 실습
# =============================================================================
# 공식 문서: https://docs.streamlit.io/develop/concepts/multipage-apps/overview
#
# [핵심 개념]
# 1. st.Page: 개별 페이지를 정의 (Python 파일 또는 함수)
# 2. st.navigation: 페이지들을 등록하고 네비게이션 메뉴 생성
# 3. pg.run(): 선택된 페이지 실행 (필수!)
#
# [st.Page 주요 파라미터]
# - page: Python 파일 경로 또는 callable 함수
# - title: 네비게이션 메뉴에 표시될 이름
# - icon: 아이콘 (Material Design 아이콘 또는 이모지)
# - default: True면 기본 페이지로 설정
# =============================================================================

# =============================================================================
# 페이지 정의
# =============================================================================
# 방법 1: Python 파일로 페이지 정의
home_page = st.Page(
    page="pages/home.py",
    title="홈",
    icon="🏠",
    default=True  # 기본 페이지로 설정
)

data_page = st.Page(
    page="pages/data_analysis.py",
    title="데이터 분석",
    icon="📊"
)

viz_page = st.Page(
    page="pages/visualization.py",
    title="시각화",
    icon="📈"
)

settings_page = st.Page(
    page="pages/settings.py",
    title="설정",
    icon="⚙️"
)

# =============================================================================
# 네비게이션 구성
# =============================================================================
# 방법 1: 단순 리스트 (섹션 없음)
# pg = st.navigation([home_page, data_page, viz_page, settings_page])
#
# [st.navigation 주요 파라미터]
# - pages: st.Page 객체들의 리스트 또는 딕셔너리
# - position: "sidebar"(기본값), "hidden" (커스텀 네비게이션 시)

# 방법 2: 딕셔너리로 섹션 구분 (권장)
pg = st.navigation({
    "메인": [home_page],
    "분석 도구": [data_page, viz_page],
    "관리": [settings_page]
})

# =============================================================================
# 공통 사이드바 요소 (모든 페이지에서 표시)
# =============================================================================
# [중요] 메인 파일(main.py)에 정의된 위젯은 모든 페이지에서 유지됨
# 이를 활용하면 페이지 간 상태 공유가 쉬워짐
with st.sidebar:
    # [핵심] 페이지별 필터를 위한 placeholder 생성
    # 각 페이지에서 st.session_state.sidebar_placeholder를 통해 필터 삽입 가능
    st.session_state.sidebar_placeholder = st.empty()


    # Session State 현재 상태 표시
    with st.expander("🔄 현재 Session State", expanded=False):
        if len(st.session_state) > 0:
            st.json({k: str(v) for k, v in st.session_state.items()})
        else:
            st.write("저장된 Session State가 없습니다.")

    st.caption("© 2025 Multi Pages App")

# =============================================================================
# 선택된 페이지 실행 (필수!)
# =============================================================================
pg.run()
