# 터미널 창에 입력
# 라이브러리 설치 : pip install streamlit pandas seaborn matplotlib
# Streamlit App 실행 : streamlit run .\02_california_housing_dashboard.py

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import platform
import os

# =============================================================================
# 한글 폰트 설정 (운영체제별)
# =============================================================================
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':  # macOS
    plt.rc('font', family='AppleGothic')
else:  # Linux
    plt.rc('font', family='NanumGothic')
plt.rc('axes', unicode_minus=False)  # 마이너스 기호 깨짐 방지

st.set_page_config(page_title="캘리포니아 주택 분석", layout="wide", page_icon="🏠")
st.title("🏠 캘리포니아 주택 데이터 분석")

# =============================================================================
# 데이터 로드
# =============================================================================
# 현재 스크립트 기준 상대 경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "california_housing.csv")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    return df

df = load_data()

# =============================================================================
# 1. 사이드바: 필터 및 설정 (st.sidebar)
# =============================================================================
# 사이드바 사용법 2가지:
# - 방법 1: 객체 표기법 (st.sidebar.title, st.sidebar.selectbox 등)
# - 방법 2: with 구문 (권장 - 더 깔끔함)

with st.sidebar:
    st.title("📊 대시보드 설정")

    # -----------------------------------------------------
    # 필터 설정 섹션
    # -----------------------------------------------------
    st.header("🔍 필터 옵션")

    # 소득 필터
    st.write("**💰 소득 범위 (만 달러)**")
    income_range = st.slider(
        "소득 범위",
        min_value=float(df['MedInc'].min()),
        max_value=float(df['MedInc'].max()),
        value=(float(df['MedInc'].min()), float(df['MedInc'].max())),
        label_visibility="collapsed",
        key="income_filter"
    )

    # 주택 연식 필터
    st.write("**🏠 주택 연식 (년)**")
    age_range = st.slider(
        "주택 연식",
        min_value=int(df['HouseAge'].min()),
        max_value=int(df['HouseAge'].max()),
        value=(int(df['HouseAge'].min()), int(df['HouseAge'].max())),
        label_visibility="collapsed",
        key="age_filter"
    )

    # 인구 필터
    st.write("**👥 인구 수**")
    pop_range = st.slider(
        "인구 수",
        min_value=int(df['Population'].min()),
        max_value=int(df['Population'].max()),
        value=(int(df['Population'].min()), int(df['Population'].max())),
        label_visibility="collapsed",
        key="pop_filter"
    )

    st.divider()

    # -----------------------------------------------------
    # 필터 결과 요약
    # -----------------------------------------------------
    # 필터 적용
    filtered_df = df[
        (df['MedInc'] >= income_range[0]) &
        (df['MedInc'] <= income_range[1]) &
        (df['HouseAge'] >= age_range[0]) &
        (df['HouseAge'] <= age_range[1]) &
        (df['Population'] >= pop_range[0]) &
        (df['Population'] <= pop_range[1])
    ]

    st.metric(label="필터링된 데이터", value=f"{len(filtered_df):,}건")

    # =========================================================================
    # 필터 초기화 버튼
    # =========================================================================
    # [session_state와 key의 관계]
    # 1. 위젯에 key="income_filter" 설정 시, Streamlit이 자동으로
    #    st.session_state["income_filter"]에 위젯 값을 저장함 (별도 초기화 불필요)
    # 2. del st.session_state["key"]로 키를 삭제하면,
    #    다음 rerun 시 위젯이 value 파라미터의 기본값으로 초기화됨
    # 3. st.rerun()은 스크립트를 처음부터 다시 실행함
    # =========================================================================
    if st.button("🔄 필터 초기화", use_container_width=True):
        for key in ["income_filter", "age_filter", "pop_filter"]:
            if key in st.session_state:
                del st.session_state[key]  # 키 삭제 → 위젯이 기본값으로 리셋
        st.rerun()  # 스크립트 재실행

    st.divider()
    st.caption("💡 사이드바는 왼쪽 상단의 > 버튼으로 접을 수 있습니다.")

# =============================================================================
# 2. 상단 지표 (st.columns + st.metric) - 전년 대비 KPI
# =============================================================================
st.header("주요 지표 (전년 대비)")

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_price = df['MedHouseVal'].mean() * 100000
    st.metric(label="평균 주택 가격", value=f"${avg_price:,.0f}", delta="12.5%", delta_color="normal")

with col2:
    avg_income = df['MedInc'].mean() * 10000
    st.metric(label="평균 소득", value=f"${avg_income:,.0f}", delta="3.2%", delta_color="normal")

with col3:
    avg_age = df['HouseAge'].mean()
    st.metric(label="평균 주택 연식", value=f"{avg_age:.1f}년", delta="-2.1%", delta_color="inverse")

with col4:
    total_records = len(df)
    st.metric(label="총 데이터 수", value=f"{total_records:,}건", delta="1,240건")

# =============================================================================
# 3. 메인 분석 영역 (st.tabs)
# =============================================================================
tab1, tab2, tab3 = st.tabs(["📋 데이터 테이블", "📈 분포 분석", "📊 통계 요약"])

with tab1:
    st.subheader("데이터 미리보기")
    st.dataframe(filtered_df.head(100), width='stretch', hide_index=True)

with tab2:
    st.subheader("주택 가격 분포")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.histplot(filtered_df['MedHouseVal'], bins=20, kde=True, ax=ax)
    ax.set_xlabel("주택 가격 (10만 달러)")
    ax.set_ylabel("빈도")
    st.pyplot(fig)

    st.subheader("소득별 주택 가격")
    chart_data = filtered_df.groupby(pd.cut(filtered_df['MedInc'], bins=10), observed=False)['MedHouseVal'].mean()
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.plot(range(len(chart_data)), chart_data.values, marker='o', linewidth=2, markersize=6)
    ax2.set_xticks(range(len(chart_data)))
    ax2.set_xticklabels([str(x) for x in chart_data.index], rotation=45, ha='right')
    ax2.set_xlabel("소득 구간 (만 달러)")
    ax2.set_ylabel("평균 주택 가격 (10만 달러)")
    plt.tight_layout()
    st.pyplot(fig2)

with tab3:
    st.subheader("주요 변수 통계")
    stats_df = filtered_df[['MedInc', 'HouseAge', 'AveRooms', 'MedHouseVal']].describe()
    stats_df.columns = ['소득', '주택연식', '평균방수', '주택가격']
    st.dataframe(stats_df, width='stretch')

# =============================================================================
# 4. 상세 분석 (st.expander)
# =============================================================================
st.divider()

with st.expander("📊 심층 분석", expanded=False):
    st.subheader("주택 특성별 가격 분석")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**주택 연식 vs 주택 가격**")
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        sns.scatterplot(data=filtered_df.sample(min(500, len(filtered_df))),
                        x='HouseAge', y='MedHouseVal', alpha=0.5, ax=ax1)
        ax1.set_xlabel("주택 연식 (년)")
        ax1.set_ylabel("주택 가격 (10만 달러)")
        st.pyplot(fig1)

    with col2:
        st.write("**주택 연식별 분포**")
        fig3, ax3 = plt.subplots(figsize=(4, 3))
        # 주택 연식별 구간 설정
        bins = [0, 10, 20, 30, 40, 55]
        labels = ['신축\n(~10년)', '준신축\n(10~20년)', '중간\n(20~30년)', '노후\n(30~40년)', '고령\n(40년+)']
        age_categories = pd.cut(filtered_df['HouseAge'], bins=bins, labels=labels)
        age_counts = age_categories.value_counts().sort_index()

        colors = ['#2ecc71', '#3498db', '#f39c12', '#e67e22', '#e74c3c']
        wedges, texts, autotexts = ax3.pie(
            age_counts.values,
            labels=age_counts.index,
            autopct='%1.1f%%',
            colors=colors,
            explode=[0.02] * len(age_counts),
            startangle=90,
            textprops={'fontsize': 8}
        )
        plt.tight_layout()
        st.pyplot(fig3)

st.divider()
st.caption("© 2025 캘리포니아 주택 데이터 분석 | Streamlit 레이아웃 실습")
