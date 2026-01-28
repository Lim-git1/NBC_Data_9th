# utils/database.py - 여러 페이지에서 공통으로 사용하는 함수만 작성

import streamlit as st
import sqlite3
import pandas as pd
import os

# 데이터 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "..", "data", "chinook.db")


@st.cache_resource
def get_connection():
    """
    DB 연결 (싱글톤)
    - 모든 페이지에서 동일한 연결 객체 공유
    - 모든 사용자/세션에서 공유
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn


@st.cache_data
def load_tracks():
    """트랙 데이터 로드 (캐싱)"""
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
