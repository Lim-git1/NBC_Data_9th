# utils/database.py - 여러 페이지에서 공통으로 사용하는 함수만 작성

import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path

# 데이터 경로 설정 (현재 파일 기준 상대 경로)
# utils/database.py → ../data/chinook.db
DB_PATH = Path(__file__).parent.parent / "data" / "chinook.db"


@st.cache_resource
def get_connection():
    """
    DB 연결 (싱글톤)
    - 모든 페이지에서 동일한 연결 객체 공유
    - 모든 사용자/세션에서 공유

    [싱글턴(Singleton) 패턴 핵심]
    - 객체를 딱 1개만 생성하고, 어디서든 그 객체를 공유하는 패턴
    - @st.cache_resource가 자동으로 싱글턴 구현
    - 장점: DB 연결 같은 무거운 자원을 매번 새로 만들지 않아 성능 향상
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn


@st.cache_data
def load_tracks():
    """트랙 데이터 로드 (캐싱)
    - 여러 페이지에서 공통으로 사용하는 데이터는 utils에 함수로 분리
    """
    conn = get_connection()
    df = pd.read_sql("""
        SELECT t.TrackId, t.Name as TrackName, a.Title as Album,
               ar.Name as Artist, g.Name as Genre,
               t.Milliseconds / 1000 as Seconds, t.UnitPrice
        FROM tracks t
        JOIN albums a ON t.AlbumId = a.AlbumId
        JOIN artists ar ON a.ArtistId = ar.ArtistId
        JOIN genres g ON t.GenreId = g.GenreId
    """, conn)
    return df
