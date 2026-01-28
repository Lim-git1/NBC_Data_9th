import streamlit as st
from utils.database import load_tracks

st.title("⚡ Streamlit 성능 최적화")
st.caption("멀티 페이지 구조에서 캐싱 활용하기")

st.markdown("""
## 폴더 구조

```
05_performance_multipage/
├── main.py                     # 엔트리 포인트 (페이지 설정)
├── utils/
│   └── database.py             # 공유 DB 연결 (@st.cache_resource)
└── pages/
    ├── home.py                 # 홈 (현재 페이지)
    ├── track_analysis.py       # 트랙 분석 (@st.cache_data)
    ├── artist_analysis.py      # 아티스트 분석 (@st.cache_resource)
    └── sales_analysis.py       # 매출 분석 (@st.fragment)
```

## 핵심 포인트

각 페이지에서 **동일한 DB 연결**을 공유합니다:
""")

st.code('''# utils/database.py
@st.cache_resource
def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn

# 어느 페이지에서든 동일한 연결 사용
from utils.database import get_connection
conn = get_connection()  # 항상 같은 객체!''', language="python")

st.info("👈 **왼쪽 사이드바에서 페이지를 선택하세요!** 각 페이지에서 DB 연결 id가 동일한지 확인해보세요.")

st.divider()

# load_tracks() 공유 예시 - 간단한 통계
st.subheader("📊 DB 현황")
st.caption("load_tracks()를 여러 페이지에서 공유하여 캐싱 효과 확인")

tracks_df = load_tracks()
col1, col2, col3 = st.columns(3)
col1.metric("🎵 트랙", f"{len(tracks_df):,}곡")
col2.metric("💿 앨범", f"{tracks_df['Album'].nunique():,}개")
col3.metric("🎤 아티스트", f"{tracks_df['Artist'].nunique():,}명")
