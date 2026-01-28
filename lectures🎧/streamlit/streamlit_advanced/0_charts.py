# 터미널 창에 입력
# 라이브러리 설치 : pip install streamlit pandas numpy matplotlib seaborn plotly
# Streamlit App 실행 : streamlit run .\06_charts.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import platform

st.title("차트 시각화 (Charts)")

# =============================================================================
# 운영체제별 한글 폰트 설정
# =============================================================================
def set_korean_font():
    """운영체제에 따라 적절한 한글 폰트 설정"""
    system = platform.system()
    if system == 'Darwin':  # macOS
        plt.rcParams['font.family'] = 'AppleGothic'
    elif system == 'Windows':  # Windows
        plt.rcParams['font.family'] = 'Malgun Gothic'
    else:  # Linux
        plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['axes.unicode_minus'] = False

set_korean_font()

# =============================================================================
# 데이터 로드
# =============================================================================

# @st.cache_data: 데이터 캐싱 데코레이터
# 주요 특징:
# - 동일한 입력에 대해 결과를 메모리에 저장하여 재사용
# - 앱 재실행 시에도 캐시된 데이터 유지 (성능 향상)
@st.cache_data
def load_california_housing():
    """캘리포니아 주택 데이터셋 로드"""
    try:
        df = pd.read_csv('data/california_housing.csv')
        df.columns = ['중위소득', '주택연수', '평균방수', '평균침실수',
                      '인구', '평균거주자수', '위도', '경도', '주택가격']
        df['주택가격'] = df['주택가격'] * 10  # 10만 달러 단위로 표시
        return df
    except FileNotFoundError:
        st.error("데이터 파일을 찾을 수 없습니다. 'data/california_housing.csv' 파일이 있는지 확인하세요.")
        return pd.DataFrame()

df = load_california_housing()
if df.empty:
    st.stop()

# =============================================================================
# 데이터 개요
st.header("데이터 개요")

# 데이터 주요 메트릭 표시
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("총 데이터 수", f"{len(df):,}개")
with col2:
    st.metric("평균 주택가격", f"${df['주택가격'].mean():.1f}만")
with col3:
    st.metric("중위소득 평균", f"${df['중위소득'].mean():.1f}만")
with col4:
    st.metric("평균 주택연수", f"{df['주택연수'].mean():.1f}년")

# 데이터 샘플 보기
st.dataframe(df.head(10), width='stretch')

# =============================================================================
# 1. Streamlit 내장 지도 시각화
st.divider()
st.header("1. Streamlit 내장 지도")

# st.map(): 간단한 지도 시각화
# 주요 파라미터:
# - data: 위도(lat), 경도(lon) 컬럼이 있는 DataFrame
# - zoom: 확대 레벨
st.write("**st.map(data, zoom):** 위도/경도 데이터를 지도에 표시")
st.write("**용도:** 위치 데이터 빠르게 시각화, 매장 분포, GPS 데이터 표시 등")

st.subheader("캘리포니아 주택 위치 분포")

map_df = df[['위도', '경도']].copy()
map_df.columns = ['lat', 'lon']

price_range = st.slider(
    "주택가격 범위 선택 (10만 달러 단위)",
    min_value=float(df['주택가격'].min()),
    max_value=float(df['주택가격'].max()),
    value=(float(df['주택가격'].quantile(0.25)), float(df['주택가격'].quantile(0.75))),
    step=0.5
)

filtered_df = df[(df['주택가격'] >= price_range[0]) & (df['주택가격'] <= price_range[1])].copy()
st.text(f"선택된 가격 범위: ${price_range[0]:.1f}만 ~ ${price_range[1]:.1f}만 (총 {len(filtered_df):,}개)")

if len(filtered_df) > 0:
    map_filtered = filtered_df[['위도', '경도']].copy()
    map_filtered.columns = ['lat', 'lon']
    st.map(map_filtered.sample(min(100, len(map_filtered))), zoom=5)
else:
    st.warning("선택된 가격 범위에 해당하는 주택이 없습니다.")

# =============================================================================
# 2. 정적 차트 (Matplotlib, Seaborn)
# =============================================================================
st.divider()
st.header("2. 정적 차트 (Static Charts)")
st.write("**st.pyplot(fig):** Matplotlib/Seaborn 차트를 Streamlit에 표시")
st.write("**정적 차트란?** 이미지로 렌더링되어 확대/축소, 마우스 오버 등 상호작용이 불가능한 차트")
st.write("**언제 사용?** 논문/보고서 출력, PDF 저장, 빠른 렌더링이 필요할 때")

st.subheader("2-1. Matplotlib")
st.write("**Matplotlib:** Python 시각화의 기본 라이브러리, 모든 세부 설정을 직접 제어 가능")
st.write("**용도:** 논문/보고서용 고품질 그래프, 완벽한 커스터마이징이 필요할 때 사용")

col1, col2 = st.columns(2)

with col1:
    st.subheader("(1) 히스토그램")
    st.write("**plt.hist():** 데이터 분포를 구간별 빈도로 표시")

    plt.figure(figsize=(8, 5))
    plt.hist(df['주택가격'], bins=30, alpha=0.7, color='lightcoral', edgecolor='black')
    plt.xlabel('주택가격 (10만 달러)', fontsize=12)
    plt.ylabel('주택 수', fontsize=12)
    plt.title('캘리포니아 주택가격 분포', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)

    mean_price = df['주택가격'].mean()
    plt.axvline(mean_price, color='red', linestyle='--', label=f'평균: ${mean_price:.1f}만')
    plt.legend()

    st.pyplot(plt.gcf())
    plt.clf()

with col2:
    st.subheader("(2) 산점도")
    st.write("**plt.scatter():** 두 변수의 관계를 점으로 표시")

    plt.figure(figsize=(8, 5))
    sample_df = df.sample(n=1000, random_state=42)

    scatter = plt.scatter(sample_df['중위소득'], sample_df['주택가격'],
                         c=sample_df['주택연수'], cmap='viridis', alpha=0.6, s=30)
    plt.xlabel('중위소득 (만 달러)', fontsize=12)
    plt.ylabel('주택가격 (10만 달러)', fontsize=12)
    plt.title('소득 vs 주택가격 (색상: 주택연수)', fontsize=14, fontweight='bold')

    cbar = plt.colorbar(scatter)
    cbar.set_label('주택연수 (년)', rotation=270, labelpad=15)
    plt.grid(True, alpha=0.3)

    st.pyplot(plt.gcf())
    plt.clf()

# =============================================================================
# 2-2. Seaborn - 통계 시각화
st.subheader("2-2. Seaborn")

st.write("**Seaborn:** Matplotlib 기반의 고수준 통계 시각화 라이브러리")
st.write("**특징:** 적은 코드로 예쁜 통계 차트 생성, 기본 스타일이 깔끔함, pandas DataFrame과 자연스럽게 연동")

col1, col2 = st.columns(2)

with col1:
    st.subheader("(1) 박스플롯")
    st.write("**sns.boxplot():** 그룹별 데이터 분포를 상자그림으로 표시")

    df_age = df.copy()
    df_age['연수구간'] = pd.cut(df_age['주택연수'],
                             bins=[0, 10, 25, 40, 100],
                             labels=['신축(0-10년)', '보통(11-25년)',
                                   '오래됨(26-40년)', '매우오래됨(40년+)'])

    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df_age, x='연수구간', y='주택가격', hue='연수구간', palette='Set2', legend=False)
    plt.title('주택연수별 가격 분포', fontsize=14, fontweight='bold')
    plt.ylabel('주택가격 (10만 달러)')
    plt.xlabel('주택연수 구간')
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(plt.gcf())
    plt.clf()

with col2:
    st.subheader("(2) 히트맵")
    st.write("**sns.heatmap():** 상관관계를 색상으로 표시")

    correlation_cols = ['중위소득', '주택연수', '평균방수', '주택가격']
    correlation_data = df[correlation_cols].corr()

    plt.figure(figsize=(6, 5))
    sns.heatmap(correlation_data, annot=True, cmap='coolwarm', center=0,
                square=True, linewidths=0.5, fmt='.2f', annot_kws={'size': 10})
    plt.title('주요 변수 상관관계', fontsize=14, fontweight='bold')
    plt.tight_layout()

    st.pyplot(plt.gcf())
    plt.clf()

# =============================================================================
# 3. 동적 차트 (Plotly)
# =============================================================================
st.divider()
st.header("3. 동적 차트 (Interactive Charts)")
st.write("**동적 차트란?** 마우스 오버, 확대/축소, 범례 클릭 등 사용자 상호작용이 가능한 차트")
st.write("**언제 사용?** 대시보드, 데이터 탐색, 프레젠테이션, 웹 앱에서 사용자 경험이 중요할 때")

st.subheader("Plotly")

# st.plotly_chart(): Plotly 차트를 Streamlit에 표시
# 주요 파라미터:
# - figure_or_data: Plotly Figure 객체
# - width: 'stretch'로 컨테이너 너비에 맞춤
st.write("**st.plotly_chart(fig):** Plotly 차트를 Streamlit에 표시")
st.write("**Plotly:** 웹 기반 인터랙티브 시각화 라이브러리, JavaScript로 렌더링")
st.write("**특징:** 확대/축소, 마우스 오버 정보, 범례 토글, PNG/SVG 다운로드 버튼 내장")

col1, col2 = st.columns(2)

# (1) 인터랙티브 산점도
with col1:
    st.subheader("(1) 인터랙티브 산점도")
    st.write("**px.scatter():** 마우스 오버, 확대/축소가 가능한 산점도")

    sample_df = df.sample(n=1000, random_state=42)

    fig = px.scatter(sample_df,
                    x='중위소득', y='주택가격',
                    color='주택연수',
                    hover_data=['평균방수', '인구'],
                    title='중위소득 vs 주택가격',
                    labels={'중위소득': '중위소득 (만$)', '주택가격': '주택가격 (10만$)'},
                    color_continuous_scale='Viridis')
    fig.update_layout(height=400)
    st.plotly_chart(fig, width='stretch')

# (2) 꺾은선 + 막대 복합 차트
with col2:
    st.subheader("(2) 꺾은선 + 막대 복합 차트")
    st.write("**go.Bar() + go.Scatter():** 두 가지 차트 유형을 하나로 결합")

    # 주택연수 구간별 집계 데이터
    df_grouped = df.groupby(pd.cut(df['주택연수'], bins=range(0, 55, 5)), observed=False).agg({
        '주택가격': 'mean',
        '중위소득': 'count'
    }).reset_index()
    df_grouped.columns = ['연수구간', '평균가격', '주택수']
    df_grouped['연수구간'] = df_grouped['연수구간'].astype(str)

    fig = go.Figure()
    # 막대 그래프: 주택 수
    fig.add_trace(go.Bar(
        x=df_grouped['연수구간'], y=df_grouped['주택수'],
        name='주택 수', marker_color='lightblue', yaxis='y'
    ))
    # 꺾은선 그래프: 평균 가격
    fig.add_trace(go.Scatter(
        x=df_grouped['연수구간'], y=df_grouped['평균가격'],
        name='평균 가격', mode='lines+markers',
        marker=dict(color='red', size=8), line=dict(width=2), yaxis='y2'
    ))
    fig.update_layout(
        title='주택연수별 분포 및 평균가격',
        xaxis_title='주택연수 구간',
        yaxis=dict(title='주택 수', side='left'),
        yaxis2=dict(title='평균가격 (10만$)', side='right', overlaying='y'),
        legend=dict(x=0.01, y=0.99), height=400
    )
    st.plotly_chart(fig, width='stretch')
