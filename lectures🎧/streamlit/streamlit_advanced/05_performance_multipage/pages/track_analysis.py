import streamlit as st
import pandas as pd
from utils.database import load_tracks, get_connection

st.header("🎵 트랙 분석")
st.caption("@st.cache_data로 데이터 캐싱 - 다른 페이지와 동일한 데이터 공유")

# DB 연결 id 확인
conn = get_connection()
st.success(f"✅ DB 연결 (id: {id(conn)})")

# 캐싱된 데이터 로드
tracks_df = load_tracks()
st.write(f"**{len(tracks_df):,}개 트랙 로드됨**")

st.divider()

# -----------------------------------------------------------------------------
# Fragment로 필터링
@st.fragment
def track_filter():
    col1, col2 = st.columns(2)
    with col1:
        genres = tracks_df['Genre'].unique().tolist()
        selected_genre = st.selectbox("장르 선택", genres, key="genre")
    with col2:
        max_price = st.slider("최대 가격", 0.0, 2.0, 1.0, key="price")

    filtered = tracks_df[
        (tracks_df['Genre'] == selected_genre) &
        (tracks_df['UnitPrice'] <= max_price)
    ]

    st.write(f"**필터링 결과:** {len(filtered):,}곡")
    st.dataframe(filtered.head(20), width='stretch', hide_index=True)

track_filter()

st.divider()

# -----------------------------------------------------------------------------
# 차트
@st.fragment
def track_chart():
    chart_type = st.radio("차트", ["장르별 트랙 수", "가격 분포"], horizontal=True, key="chart")

    if chart_type == "장르별 트랙 수":
        st.bar_chart(tracks_df['Genre'].value_counts().head(10))
    else:
        st.bar_chart(tracks_df['UnitPrice'].value_counts().sort_index())

track_chart()
