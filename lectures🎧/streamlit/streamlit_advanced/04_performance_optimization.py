# 터미널 창에 입력
# 라이브러리 설치 : pip install streamlit pandas
# Streamlit App 실행 : streamlit run .\04_performance_optimization.py

import streamlit as st
import pandas as pd
import sqlite3
import time
import os

st.set_page_config(page_title="성능 최적화 실습", layout="wide", page_icon="⚡")
st.title("⚡ Streamlit 성능 최적화")

# =============================================================================
# 데이터 경로 설정
# =============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "chinook.db")

# =============================================================================
# 1. @st.cache_data - 데이터 캐싱
# =============================================================================
st.header("1. @st.cache_data - 데이터 캐싱")
st.write("- `@st.cache_data` : DataFrame, API 응답 등 **데이터**를 캐싱")

# 파라미터 설명 테이블
params_cache_data = pd.DataFrame({
    '파라미터': ['ttl', 'max_entries', 'show_spinner'],
    '타입': ['int/timedelta', 'int', 'bool/str'],
    '설명': [
        '캐시 만료 시간 (초). 지나면 재계산',
        '최대 캐시 수 (함수 인자 조합 기준, 기본 None=무제한). 초과 시 오래된 것부터 삭제',
        '로딩 중 스피너 표시. 문자열 시 메시지 커스텀'
    ],
    '예시 값': ['600', '100', '"로딩 중..."']
})
st.dataframe(params_cache_data, width='stretch', hide_index=True)

# -----------------------------------------------------------------------------
st.subheader("(1) 기본 데이터 캐싱")
st.code('''@st.cache_data
def load_tracks():
    """Chinook DB에서 트랙 데이터 로드"""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("""
        SELECT t.TrackId, t.Name as TrackName, a.Title as Album,
               ar.Name as Artist, g.Name as Genre,
               t.Milliseconds / 1000 as Seconds, t.UnitPrice
        FROM tracks t
        JOIN albums a ON t.AlbumId = a.AlbumId
        JOIN artists ar ON a.ArtistId = ar.ArtistId
        JOIN genres g ON t.GenreId = g.GenreId
    """, conn)
    conn.close()
    return df

tracks_df = load_tracks()''', language="python")

st.caption("▼ 실행 결과")

@st.cache_data
def load_tracks():
    """Chinook DB에서 트랙 데이터 로드"""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("""
        SELECT t.TrackId, t.Name as TrackName, a.Title as Album,
               ar.Name as Artist, g.Name as Genre,
               t.Milliseconds / 1000 as Seconds, t.UnitPrice
        FROM tracks t
        JOIN albums a ON t.AlbumId = a.AlbumId
        JOIN artists ar ON a.ArtistId = ar.ArtistId
        JOIN genres g ON t.GenreId = g.GenreId
    """, conn)
    conn.close()
    return df

tracks_df = load_tracks()
st.success(f"✅ 총 {len(tracks_df):,}개 트랙 로드 완료!")

# -----------------------------------------------------------------------------
st.subheader("(2) TTL 설정 - 주기적 갱신")

st.code('''@st.cache_data(ttl=60)  # 60초마다 캐시 갱신
def get_realtime_stats():
    return {
        'total_tracks': len(tracks_df),
        'avg_price': tracks_df['UnitPrice'].mean(),
        'total_duration': tracks_df['Seconds'].sum() / 3600,
        'updated_at': time.strftime('%H:%M:%S')
    }''', language="python")

st.caption("▼ 실행 결과")

@st.cache_data(ttl=60)
def get_realtime_stats():
    return {
        'total_tracks': len(tracks_df),
        'avg_price': tracks_df['UnitPrice'].mean(),
        'total_duration': tracks_df['Seconds'].sum() / 3600,
        'updated_at': time.strftime('%H:%M:%S')
    }

stats = get_realtime_stats()
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("총 트랙 수", f"{stats['total_tracks']:,}곡")
with col2:
    st.metric("평균 가격", f"${stats['avg_price']:.2f}")
with col3:
    st.metric("총 재생시간", f"{stats['total_duration']:.1f}시간")
with col4:
    st.metric("업데이트", stats['updated_at'])

st.divider()

# =============================================================================
# 2. @st.cache_resource - 리소스 캐싱
# =============================================================================
st.header("2. @st.cache_resource - 리소스 캐싱")
st.write("- `@st.cache_resource` : DB 연결, ML 모델 등 **리소스**를 캐싱 (원본 객체 공유)")

# -----------------------------------------------------------------------------
st.subheader("(1) SQLite 연결 캐싱")

st.code('''@st.cache_resource
def get_database_connection():
    """DB 연결 (리소스 캐싱)"""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn

conn = get_database_connection()''', language="python")

st.caption("▼ 실행 결과")

@st.cache_resource
def get_database_connection():
    """DB 연결 (리소스 캐싱)"""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn

conn = get_database_connection()
st.success("✅ 데이터베이스 연결 성공! (캐싱됨)")

# -----------------------------------------------------------------------------
st.subheader("(2) SQL 쿼리 실행기")

st.code('''query = st.text_area("SQL 쿼리", value="SELECT * FROM artists LIMIT 10")

if st.button("쿼리 실행"):
    result = pd.read_sql(query, conn)
    st.dataframe(result, width='stretch', hide_index=True)''', language="python")

st.caption("▼ 실행 결과")

query = st.text_area("SQL 쿼리", value="SELECT * FROM artists LIMIT 10", height=80, key="sql_query")

if st.button("🔍 쿼리 실행", key="run_query"):
    try:
        result = pd.read_sql(query, conn)
        st.dataframe(result, width='stretch', hide_index=True)
        st.caption(f"결과: {len(result)}행")
    except Exception as e:
        st.error(f"쿼리 오류: {e}")

st.divider()

# =============================================================================
# 3. @st.fragment - 부분 재실행
# =============================================================================
st.header("3. @st.fragment - 부분 재실행")
st.write("- `@st.fragment` : 위젯 변경 시 **해당 영역만** 재실행 (Fragment 내 위젯에는 `key` 필수)")

# -----------------------------------------------------------------------------
st.subheader("(1) 필터링 Fragment")

st.code('''@st.fragment
def filter_section():
    genres = tracks_df['Genre'].unique().tolist()
    selected_genre = st.selectbox("장르 선택", genres, key="filter_genre")
    max_price = st.slider("최대 가격", 0.0, 2.0, 1.0, key="filter_price")

    filtered = tracks_df[
        (tracks_df['Genre'] == selected_genre) &
        (tracks_df['UnitPrice'] <= max_price)
    ]
    st.write(f"**필터링 결과:** {len(filtered):,}곡")
    st.dataframe(filtered.head(10), width='stretch', hide_index=True)

filter_section()''', language="python")

st.caption("▼ 실행 결과")

@st.fragment
def filter_section():
    col1, col2 = st.columns(2)
    with col1:
        genres = tracks_df['Genre'].unique().tolist()
        selected_genre = st.selectbox("장르 선택", genres, key="filter_genre")
    with col2:
        max_price = st.slider("최대 가격", 0.0, 2.0, 1.0, step=0.1, key="filter_price")

    filtered = tracks_df[
        (tracks_df['Genre'] == selected_genre) &
        (tracks_df['UnitPrice'] <= max_price)
    ]
    st.write(f"**필터링 결과:** {len(filtered):,}곡")
    st.dataframe(filtered.head(10), width='stretch', hide_index=True)

filter_section()

# -----------------------------------------------------------------------------
st.subheader("(2) 차트 Fragment")

st.code('''@st.fragment
def chart_section():
    chart_type = st.radio(
        "차트 유형",
        ["장르별 트랙 수", "아티스트별 앨범 수", "가격 분포"],
        horizontal=True,
        key="chart_type"
    )

    if chart_type == "장르별 트랙 수":
        chart_data = tracks_df['Genre'].value_counts().head(10)
        st.bar_chart(chart_data)
    elif chart_type == "아티스트별 앨범 수":
        chart_data = tracks_df.groupby('Artist')['Album'].nunique().nlargest(10)
        st.bar_chart(chart_data)
    else:
        chart_data = tracks_df['UnitPrice'].value_counts().sort_index()
        st.bar_chart(chart_data)

chart_section()''', language="python")

st.caption("▼ 실행 결과")

@st.fragment
def chart_section():
    chart_type = st.radio(
        "차트 유형",
        ["장르별 트랙 수", "아티스트별 앨범 수", "가격 분포"],
        horizontal=True,
        key="chart_type"
    )

    if chart_type == "장르별 트랙 수":
        chart_data = tracks_df['Genre'].value_counts().head(10)
        st.bar_chart(chart_data)
    elif chart_type == "아티스트별 앨범 수":
        chart_data = tracks_df.groupby('Artist')['Album'].nunique().nlargest(10)
        st.bar_chart(chart_data)
    else:
        chart_data = tracks_df['UnitPrice'].value_counts().sort_index()
        st.bar_chart(chart_data)

chart_section()

st.divider()

# =============================================================================
# 4. 캐싱 + Fragment 조합
# =============================================================================
st.header("4. 캐싱 + Fragment 조합")

st.code('''@st.cache_data
def expensive_aggregation(genre):
    time.sleep(1)  # 복잡한 계산 시뮬레이션
    genre_data = tracks_df[tracks_df['Genre'] == genre]
    return {
        'count': len(genre_data),
        'avg_duration': genre_data['Seconds'].mean(),
        'total_value': (genre_data['UnitPrice'] * 100).sum()
    }

@st.fragment
def aggregation_fragment():
    genre = st.selectbox("장르 선택", tracks_df['Genre'].unique(), key="agg_genre")

    with st.spinner("계산 중..."):
        result = expensive_aggregation(genre)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("트랙 수", f"{result['count']}곡")
    with col2:
        st.metric("평균 길이", f"{result['avg_duration']:.0f}초")
    with col3:
        st.metric("총 가치", f"${result['total_value']:.0f}")

aggregation_fragment()''', language="python")

st.caption("▼ 실행 결과")

@st.cache_data
def expensive_aggregation(genre):
    time.sleep(1)
    genre_data = tracks_df[tracks_df['Genre'] == genre]
    return {
        'count': len(genre_data),
        'avg_duration': genre_data['Seconds'].mean(),
        'total_value': (genre_data['UnitPrice'] * 100).sum()
    }

@st.fragment
def aggregation_fragment():
    genre = st.selectbox("장르 선택", tracks_df['Genre'].unique(), key="agg_genre")

    with st.spinner("계산 중..."):
        result = expensive_aggregation(genre)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("트랙 수", f"{result['count']}곡")
    with col2:
        st.metric("평균 길이", f"{result['avg_duration']:.0f}초")
    with col3:
        st.metric("총 가치", f"${result['total_value']:.0f}")

aggregation_fragment()

st.caption("© 2025 Streamlit 성능 최적화")
