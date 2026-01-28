# =============================================================================
# 데이터 분석 페이지 (Data Analysis Page)
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(page_title="데이터 분석 | 다중 페이지 앱", layout="wide", page_icon="📊")
st.title("📊 데이터 분석")

# =============================================================================
# 데이터 로드
# =============================================================================
# 현재 스크립트의 상위 폴더 기준으로 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "california_housing.csv")

@st.cache_data  # 데이터 캐싱: 함수 인자가 동일하면 재실행 없이 캐시된 결과 반환
                # 모든 페이지에서 공유됨, 새로고침(F5) 시 캐시 초기화
def load_data():
    """캘리포니아 주택 데이터 로드"""
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    else:
        # 데이터가 없으면 샘플 데이터 생성
        np.random.seed(42)
        n = 1000
        return pd.DataFrame({
            'MedInc': np.random.uniform(0.5, 15, n),
            'HouseAge': np.random.randint(1, 52, n),
            'AveRooms': np.random.uniform(1, 10, n),
            'AveBedrms': np.random.uniform(0.5, 5, n),
            'Population': np.random.randint(100, 10000, n),
            'AveOccup': np.random.uniform(1, 10, n),
            'Latitude': np.random.uniform(32, 42, n),
            'Longitude': np.random.uniform(-124, -114, n),
            'MedHouseVal': np.random.uniform(0.5, 5, n)
        })

df = load_data()

# =============================================================================
# Session State 초기화 (페이지 간 상태 공유)
# =============================================================================
# [중요] 다중 페이지 앱에서 위젯 상태 관리
# 방법 1: 메인 파일(main.py)에서 위젯 정의 (가장 권장)
# 방법 2: Session State 중간 키 사용 (현재 방법)
# 방법 3: 위젯 클린업 방지

# Session State 기본값 설정
if "income_min" not in st.session_state:
    st.session_state.income_min = float(df['MedInc'].min())
if "income_max" not in st.session_state:
    st.session_state.income_max = float(df['MedInc'].max())

# =============================================================================
# 사이드바: 필터 설정 (main.py의 placeholder 활용)
# =============================================================================
# [Session State 활용법]
#
# [문제] 위젯과 연결된 key는 페이지 이동 시 자동 삭제됨
#   - st.session_state.xxx = 값       → 직접 저장 → 영구 유지 ✅
#   - st.slider(..., key="yyy")       → 위젯과 연결 → st.session_state.yyy 자동 생성
#     └─ 페이지 이동 → 위젯 사라짐 → st.session_state.yyy 자동 삭제 ❌
#
# [해결] 임시 키(_접두사) + on_change 콜백으로 영구 키에 복사
#   - key="_income_range"             → 임시 키 (삭제되어도 OK)
#   - on_change=update_income         → 값 변경 시 영구 키에 복사
#   - value=(income_min, income_max)  → 영구 키 값으로 위젯 초기화
def update_income():
    """소득 필터 값을 Session State에 저장"""
    st.session_state.income_min = st.session_state._income_range[0]
    st.session_state.income_max = st.session_state._income_range[1]

# main.py에서 생성한 placeholder에 필터 삽입
with st.session_state.sidebar_placeholder.container():
    st.header("🔍 데이터 필터")
    st.write("**💰 소득 범위 (만 달러)**")
    st.slider(
        "소득 범위 선택",
        min_value=float(df['MedInc'].min()),
        max_value=float(df['MedInc'].max()),
        value=(st.session_state.income_min, st.session_state.income_max),
        key="_income_range",  # 임시 키 (언더스코어 접두사)
        on_change=update_income,  # 값 변경 시 콜백 실행
        label_visibility="collapsed"
    )

# =============================================================================
# 데이터 필터링
# =============================================================================
filtered_df = df[
    (df['MedInc'] >= st.session_state.income_min) &
    (df['MedInc'] <= st.session_state.income_max)
].copy()  # 원본 데이터 보호를 위해 복사본 사용

# =============================================================================
# 메인 콘텐츠
# =============================================================================
# 필터 결과 요약
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="전체 데이터",
        value=f"{len(df):,}건"
    )

with col2:
    st.metric(
        label="필터링된 데이터",
        value=f"{len(filtered_df):,}건",
        delta=f"{len(filtered_df) - len(df):,}건"
    )

with col3:
    st.metric(
        label="필터링 비율",
        value=f"{len(filtered_df)/len(df)*100:.1f}%"
    )

st.divider()

# =============================================================================
# 데이터 테이블
# =============================================================================
st.subheader("📋 데이터 테이블")

# 컬럼 선택
all_columns = df.columns.tolist()

# Session State로 선택된 컬럼 유지
if "selected_columns" not in st.session_state:
    st.session_state.selected_columns = all_columns[:5]

selected_cols = st.multiselect(
    "표시할 컬럼 선택",
    options=all_columns,
    default=st.session_state.selected_columns,
    key="selected_columns"
)

if selected_cols:
    # 설정 페이지에서 지정한 표시 행 수 사용
    display_rows = st.session_state.get("display_rows", 100)
    st.dataframe(
        filtered_df[selected_cols].head(display_rows),
        width='stretch',
        hide_index=True
    )
else:
    st.warning("최소 하나의 컬럼을 선택해주세요.")

st.divider()

# =============================================================================
# 기술 통계
# =============================================================================
st.subheader("📈 기술 통계")

tab1, tab2 = st.tabs(["요약 통계", "상관관계"])

with tab1:
    st.write("**필터링된 데이터의 기술 통계량**")
    stats_df = filtered_df.describe()
    st.dataframe(stats_df, width='stretch')

with tab2:
    st.write("**변수 간 상관관계**")
    numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns
    corr_matrix = filtered_df[numeric_cols].corr()
    st.dataframe(
        corr_matrix.style.background_gradient(cmap='RdYlBu', vmin=-1, vmax=1),
        width='stretch'
    )

# =============================================================================
# 페이지 하단 안내
# =============================================================================
st.divider()
st.info("💡 **Tip**: 필터 설정은 Session State에 저장되어 다른 페이지로 이동해도 유지됩니다.")
