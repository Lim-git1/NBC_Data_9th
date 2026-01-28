import streamlit as st
import pandas as pd
from utils.database import get_connection

st.header("🎤 아티스트 분석")
st.caption("@st.cache_resource로 DB 연결 캐싱 - 모든 페이지에서 동일한 연결 공유")

# 캐싱된 DB 연결
conn = get_connection()
st.success(f"✅ DB 연결 (id: {id(conn)}) - 다른 페이지와 동일한 id 확인!")

st.divider()

# -----------------------------------------------------------------------------
# 아티스트 통계
@st.cache_data
def get_artist_stats():
    return pd.read_sql("""
        SELECT ar.Name as Artist, COUNT(t.TrackId) as TrackCount,
               SUM(t.Milliseconds)/1000/60 as TotalMinutes
        FROM artists ar
        JOIN albums a ON ar.ArtistId = a.ArtistId
        JOIN tracks t ON a.AlbumId = t.AlbumId
        GROUP BY ar.ArtistId
        ORDER BY TrackCount DESC
        LIMIT 20
    """, conn)

artist_stats = get_artist_stats()

col1, col2 = st.columns(2)
with col1:
    st.subheader("트랙 수 Top 10")
    st.bar_chart(artist_stats.set_index('Artist')['TrackCount'].head(10))

with col2:
    st.subheader("총 재생시간 Top 10")
    st.bar_chart(artist_stats.set_index('Artist')['TotalMinutes'].head(10))

st.divider()

# -----------------------------------------------------------------------------
# SQL 쿼리 실행기
st.subheader("🔍 SQL 쿼리 실행")

query = st.text_area("SQL", value="SELECT * FROM artists LIMIT 10", height=80, key="sql")

if st.button("실행"):
    try:
        result = pd.read_sql(query, conn)
        st.dataframe(result, width='stretch', hide_index=True)
    except Exception as e:
        st.error(f"오류: {e}")
