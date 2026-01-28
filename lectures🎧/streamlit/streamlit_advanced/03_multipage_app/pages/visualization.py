# =============================================================================
# 시각화 페이지 (Visualization Page)
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import platform
import os

st.set_page_config(page_title="시각화 | 다중 페이지 앱", layout="wide", page_icon="📈")
st.title("📈 데이터 시각화")

# =============================================================================
# 데이터 로드 (data_analysis.py와 동일한 로직)
# =============================================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "california_housing.csv")

@st.cache_data  # 데이터 캐싱: 함수 인자가 동일하면 재실행 없이 캐시된 결과 반환
                # 모든 페이지에서 공유됨, 새로고침(F5) 시 캐시 초기화
def load_data():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    else:
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
# Session State에서 필터 값 가져오기
# =============================================================================
# [핵심] 데이터 분석 페이지에서 설정한 필터가 여기서도 적용됨!
income_min = st.session_state.get("income_min", float(df['MedInc'].min()))
income_max = st.session_state.get("income_max", float(df['MedInc'].max()))

filtered_df = df[
    (df['MedInc'] >= income_min) &
    (df['MedInc'] <= income_max)
].copy()  # 원본 데이터 보호를 위해 복사본 사용

# =============================================================================
# 사이드바: 현재 필터 상태 표시 (main.py의 placeholder 활용)
# =============================================================================
with st.session_state.sidebar_placeholder.container():
    st.header("📊 현재 필터 상태")
    st.write(f"**소득 범위**: {income_min:.1f} ~ {income_max:.1f}")
    st.write(f"**데이터 건수**: {len(filtered_df):,}건")
    st.caption("💡 데이터 분석 페이지에서 필터 변경 가능")

# =============================================================================
# 차트 스타일 및 한글 폰트 설정
# =============================================================================
# [중요] sns.set_style() 이후에 한글 폰트를 설정해야 덮어쓰기 방지
chart_style = st.session_state.get("chart_style", "darkgrid")
sns.set_style(chart_style)

# 한글 폰트 설정 (운영체제별) - sns.set_style 이후에 적용
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':  # macOS
    plt.rc('font', family='AppleGothic')
else:  # Linux
    plt.rc('font', family='NanumGothic')
plt.rc('axes', unicode_minus=False)  # 마이너스 기호 깨짐 방지

# 차트 높이 기본값 설정
if "chart_height" not in st.session_state:
    st.session_state.chart_height = 400

# =============================================================================
# 메인 콘텐츠: 차트 탭
# =============================================================================
tab1, tab2, tab3 = st.tabs(["📊 분포", "📈 관계", "📉 시계열"])

# -----------------------------------------------------------------------------
# Tab 1: 분포 차트
# -----------------------------------------------------------------------------
with tab1:
    st.subheader("변수 분포 분석")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**주택 가격 분포**")
        fig1, ax1 = plt.subplots(figsize=(8, st.session_state.chart_height/100))
        sns.histplot(data=filtered_df, x='MedHouseVal', kde=True, ax=ax1)
        ax1.set_xlabel("주택 가격 (10만 달러)")
        ax1.set_ylabel("빈도")
        ax1.set_title("주택 가격 히스토그램")
        plt.tight_layout()
        st.pyplot(fig1)
        plt.close(fig1)

    with col2:
        st.write("**소득 분포**")
        fig2, ax2 = plt.subplots(figsize=(8, st.session_state.chart_height/100))
        sns.histplot(data=filtered_df, x='MedInc', kde=True, color='green', ax=ax2)
        ax2.set_xlabel("소득 (만 달러)")
        ax2.set_ylabel("빈도")
        ax2.set_title("소득 히스토그램")
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close(fig2)

    # 박스플롯
    st.write("**주요 변수 박스플롯**")
    fig3, axes = plt.subplots(1, 4, figsize=(16, st.session_state.chart_height/100))

    variables = ['MedInc', 'HouseAge', 'AveRooms', 'MedHouseVal']
    titles = ['소득', '주택 연식', '평균 방 수', '주택 가격']
    colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c']

    for ax, var, title, color in zip(axes, variables, titles, colors):
        sns.boxplot(data=filtered_df, y=var, ax=ax, color=color)
        ax.set_title(title)
        ax.set_ylabel("")

    plt.tight_layout()
    st.pyplot(fig3)
    plt.close(fig3)

# -----------------------------------------------------------------------------
# Tab 2: 관계 차트
# -----------------------------------------------------------------------------
with tab2:
    st.subheader("변수 간 관계 분석")

    col1, col2 = st.columns(2)

    with col1:
        x_var = st.selectbox(
            "X축 변수",
            options=['MedInc', 'HouseAge', 'AveRooms', 'Population'],
            index=0
        )

    with col2:
        y_var = st.selectbox(
            "Y축 변수",
            options=['MedHouseVal', 'MedInc', 'HouseAge', 'AveRooms'],
            index=0
        )

    # 산점도
    st.write(f"**{x_var} vs {y_var}**")

    # 샘플링 (너무 많은 점은 성능 저하)
    sample_size = min(1000, len(filtered_df))
    sample_df = filtered_df.sample(sample_size, random_state=42)

    fig4, ax4 = plt.subplots(figsize=(10, st.session_state.chart_height/100))
    scatter = ax4.scatter(
        sample_df[x_var],
        sample_df[y_var],
        c=sample_df['MedHouseVal'],
        cmap='viridis',
        alpha=0.6,
        s=20
    )
    ax4.set_xlabel(x_var)
    ax4.set_ylabel(y_var)
    plt.colorbar(scatter, label='주택 가격')
    plt.tight_layout()
    st.pyplot(fig4)
    plt.close(fig4)

# -----------------------------------------------------------------------------
# Tab 3: 시계열/트렌드 차트
# -----------------------------------------------------------------------------
with tab3:
    st.subheader("주택 연식별 분석")

    # 주택 연식별 평균 가격
    age_price = filtered_df.groupby('HouseAge')['MedHouseVal'].mean().reset_index()

    st.write("**주택 연식별 평균 가격**")
    fig6, ax6 = plt.subplots(figsize=(12, st.session_state.chart_height/100))
    ax6.plot(age_price['HouseAge'], age_price['MedHouseVal'], marker='o', linewidth=2, markersize=4)
    ax6.fill_between(age_price['HouseAge'], age_price['MedHouseVal'], alpha=0.3)
    ax6.set_xlabel("주택 연식 (년)")
    ax6.set_ylabel("평균 주택 가격 (10만 달러)")
    ax6.set_title("주택 연식에 따른 평균 가격 변화")
    ax6.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig6)
    plt.close(fig6)

    # 연식 구간별 통계
    st.write("**연식 구간별 통계**")
    bins = [0, 10, 20, 30, 40, 52]
    labels = ['신축(~10년)', '준신축(10~20년)', '중간(20~30년)', '노후(30~40년)', '고령(40년+)']
    filtered_df['AgeGroup'] = pd.cut(filtered_df['HouseAge'], bins=bins, labels=labels)

    age_stats = filtered_df.groupby('AgeGroup', observed=False).agg({
        'MedHouseVal': ['mean', 'std', 'count'],
        'MedInc': 'mean'
    }).round(2)
    age_stats.columns = ['평균가격', '가격표준편차', '데이터수', '평균소득']
    st.dataframe(age_stats, width='stretch')

# =============================================================================
# 페이지 하단 안내
# =============================================================================
st.divider()
st.info("💡 **Tip**: 데이터 분석 페이지에서 설정한 필터가 여기서도 적용됩니다. Session State를 통해 페이지 간 상태가 공유됩니다!")
