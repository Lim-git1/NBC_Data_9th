# 터미널 창에 입력
# 라이브러리 설치 : pip install streamlit pandas
# Streamlit App 실행 : streamlit run .\01_layout_components.py

import streamlit as st
import pandas as pd
import time

st.title("레이아웃 컴포넌트 (Layout Components)")

# =============================================================================
# 1. 컬럼 (Columns) - 화면을 가로로 나누기
# =============================================================================
st.header("1. 컬럼 (Columns)")

# st.columns(): 화면을 가로로 나누는 레이아웃 위젯
# 주요 파라미터:
# - spec: 컬럼 개수(정수) 또는 비율 리스트 (예: [2, 1, 1])
# - gap: 컬럼 간격 ("small", "medium", "large")
# - vertical_alignment: 수직 정렬 ("top", "center", "bottom")
st.write("- `st.columns(spec, gap, vertical_alignment)` : 화면을 가로로 분할")
st.caption("- 용도: 대시보드 지표, 이미지 갤러리, 폼 레이아웃 등 가로 배치 시 사용")

# 파라미터 설명 테이블
params_columns = pd.DataFrame({
    '파라미터': ['spec', 'gap', 'vertical_alignment'],
    '타입': ['int 또는 list', 'str', 'str'],
    '설명': [
        '컬럼 개수(정수) 또는 너비 비율 리스트',
        '컬럼 사이 간격',
        '컬럼 내 요소의 수직 정렬'
    ],
    '예시 값': [
        '3 또는 [2, 1, 1]',
        '"small", "medium", "large"',
        '"top", "center", "bottom"'
    ]
})
st.dataframe(params_columns, width='stretch', hide_index=True)

# -----------------------------------------------------------------------------
st.subheader("(1) 동일 너비 컬럼")
st.caption("정수를 전달하면 동일한 너비의 컬럼이 생성됩니다.")

st.code('''# 3개의 동일한 너비 컬럼 생성
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="매출", value="₩1.2억", delta="+12.5%")

with col2:
    st.metric(label="고객수", value="5,432명", delta="-2.1%"")

with col3:
    st.metric(label="만족도", value="4.8/5.0", delta="+0.3")''', language="python")

st.caption("▼ 실행 결과")

# 3개의 동일한 너비 컬럼 생성
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="매출", value="₩1.2억", delta="+12.5%")

with col2:
    st.metric(label="고객수", value="5,432명", delta="-2.1%")

with col3:
    st.metric(label="만족도", value="4.8/5.0", delta="+0.3")

# -----------------------------------------------------------------------------
st.subheader("(2) 비율로 너비 조절")
st.caption("리스트로 컬럼 너비 비율을 지정할 수 있습니다.")

st.code('''# 비율로 너비 설정 (2:1 비율 = 넓은 영역 : 좁은 영역)
left_col, right_col = st.columns([2, 1])

with left_col:
    st.write("**넓은 영역 (2/3)**")
    chart_data = pd.DataFrame({
        '월': ['1월', '2월', '3월', '4월', '5월'],
        '매출': [100, 150, 130, 180, 200]
    })
    st.line_chart(chart_data.set_index('월'))

with right_col:
    st.write("**좁은 영역 (1/3)**")
    st.info("이 영역은 전체의 1/3입니다")''', language="python")

st.caption("▼ 실행 결과")

# 비율로 너비 설정 (2:1 비율)
left_col, right_col = st.columns([2, 1])

with left_col:
    st.write("**넓은 영역 (2/3)**")
    chart_data = pd.DataFrame({
        '월': ['1월', '2월', '3월', '4월', '5월'],
        '매출': [100, 150, 130, 180, 200]
    })
    st.line_chart(chart_data.set_index('월'))

with right_col:
    st.write("**좁은 영역 (1/3)**")
    st.info("이 영역은 전체의 1/3입니다")

# -----------------------------------------------------------------------------
st.subheader("(3) 컬럼 간격 조절 (gap)")
st.caption("컬럼 사이의 간격을 조절할 수 있습니다.")

st.code('''# gap 파라미터로 컬럼 간격 설정
gap_option = st.radio(
    "간격 선택",
    options=["small", "medium", "large"],
    index=2,  # 기본값: "large"
    horizontal=True,
    help="컬럼 사이의 간격을 조절합니다"
)

cols = st.columns(4, gap=gap_option)
for i, col in enumerate(cols):
    with col:
        st.button(f"버튼 {i+1}", width="stretch")''', language="python")

st.caption("▼ 실행 결과 (아래에서 간격을 선택해보세요)")

gap_option = st.radio(
    "간격 선택",
    options=["small", "medium", "large"],
    index=2,
    horizontal=True,
    help="컬럼 사이의 간격을 조절합니다"
)

cols = st.columns(4, gap=gap_option)
for i, col in enumerate(cols):
    with col:
        st.button(f"버튼 {i+1}", width="stretch")

# =============================================================================
# 2. 탭 (Tabs) - 콘텐츠 전환하기
# =============================================================================
st.divider()
st.header("2. 탭 (Tabs)")

# st.tabs(): 탭으로 콘텐츠를 전환하는 레이아웃 위젯
st.write("- `st.tabs(tabs)` : 탭으로 콘텐츠 전환")
st.caption("- 용도: 같은 공간에서 여러 콘텐츠를 전환하며 보여줄 때 사용 (예: 데이터/차트/설정 뷰 전환)")

# 파라미터 설명 테이블
params_tabs = pd.DataFrame({
    '파라미터': ['tabs'],
    '타입': ['list[str]'],
    '설명': ['탭 이름 리스트 (이모지 사용 가능)'],
    '예시 값': ['["📊 데이터", "📈 차트", "⚙️ 설정"]']
})
st.dataframe(params_tabs, width='stretch', hide_index=True)

st.code('''# 탭 3개 생성 (이모지로 시각적 구분)
tab1, tab2, tab3 = st.tabs(["📊 데이터", "📈 차트", "⚙️ 설정"])

with tab1:
    st.subheader("데이터 테이블")
    df = pd.DataFrame({
        '제품': ['노트북', '마우스', '키보드'],
        '판매량': [120, 450, 230]
    })
    st.dataframe(df, width='stretch', hide_index=True)

with tab2:
    st.subheader("판매량 차트")
    st.bar_chart(df.set_index('제품'))

with tab3:
    st.subheader("설정")
    dark_mode = st.checkbox("다크 모드")
    font_size = st.slider("글자 크기", 10, 30, 16)
    if st.button("저장"):
        st.success(f"저장 완료! (다크모드: {dark_mode}, 크기: {font_size}px)")''', language="python")

st.caption("▼ 실행 결과")

# 탭 3개 생성 (이모지로 시각적 구분)
tab1, tab2, tab3 = st.tabs(["📊 데이터", "📈 차트", "⚙️ 설정"])

with tab1:
    st.subheader("데이터 테이블")
    df = pd.DataFrame({
        '제품': ['노트북', '마우스', '키보드'],
        '판매량': [120, 450, 230]
    })
    st.dataframe(df, width='stretch', hide_index=True)

with tab2:
    st.subheader("판매량 차트")
    st.bar_chart(df.set_index('제품'))

with tab3:
    st.subheader("설정")
    dark_mode = st.checkbox("다크 모드")
    font_size = st.slider("글자 크기", 10, 30, 16)
    if st.button("저장"):
        st.success(f"저장 완료! (다크모드: {dark_mode}, 크기: {font_size}px)")

# =============================================================================
# 3. 컨테이너 (Container)
# =============================================================================
st.divider()
st.header("3. 컨테이너 (Container)")

st.write("- `st.container(border, height)` : 요소들을 논리적으로 그룹화")
st.caption("- 용도: 관련 요소 묶기, 동적 콘텐츠 영역, 스크롤 가능한 영역 만들기")

# 파라미터 설명 테이블
params_container = pd.DataFrame({
    '파라미터': ['border', 'height'],
    '타입': ['bool', 'int'],
    '설명': [
        '테두리 표시 여부 (Streamlit 1.36.0+)',
        '고정 높이 설정 (픽셀), 넘치면 스크롤'
    ],
    '예시 값': ['True, False', '200, 300, 400']
})
st.dataframe(params_container, width='stretch', hide_index=True)

# -----------------------------------------------------------------------------
st.subheader("(1) 테두리 있는 컨테이너")

st.code('''# 테두리가 있는 컨테이너
with st.container(border=True):
    st.write("📦 **이 안의 모든 요소는 하나의 그룹입니다**")
    col1, col2 = st.columns(2)
    with col1:
        st.button("버튼 A", width="stretch")
    with col2:
        st.button("버튼 B", width="stretch")''', language="python")

st.caption("▼ 실행 결과")

with st.container(border=True):
    st.write("📦 **이 안의 모든 요소는 하나의 그룹입니다**")
    col1, col2 = st.columns(2)
    with col1:
        st.button("버튼 A", width="stretch")
    with col2:
        st.button("버튼 B", width="stretch")

# -----------------------------------------------------------------------------
st.subheader("(2) 스크롤 가능한 컨테이너 (고정 높이)")

st.code('''# 고정 높이 컨테이너 (200px, 넘치면 스크롤)
with st.container(height=200):
    st.write("이 컨테이너는 높이가 200px로 고정되어 있습니다.")
    for i in range(1, 11):
        st.write(f"📝 항목 {i}: 스크롤해서 더 많은 내용을 확인하세요")''', language="python")

st.caption("▼ 실행 결과")

with st.container(height=200):
    st.write("이 컨테이너는 높이가 200px로 고정되어 있습니다.")
    for i in range(1, 11):
        st.write(f"📝 항목 {i}: 스크롤해서 더 많은 내용을 확인하세요")

# =============================================================================
# 4. 확장기 (Expander)
# =============================================================================
st.divider()
st.header("4. 확장기 (Expander)")

st.write("- `st.expander(label, expanded, icon)` : 접었다 펼 수 있는 섹션")
st.caption("- 용도: 상세 정보, FAQ, 추가 옵션 등 선택적으로 표시할 콘텐츠에 사용")

# 파라미터 설명 테이블
params_expander = pd.DataFrame({
    '파라미터': ['label', 'expanded', 'icon'],
    '타입': ['str', 'bool', 'str'],
    '설명': [
        '확장기 제목',
        '기본 펼침 상태 (True면 펼쳐진 상태로 시작)',
        '아이콘 (이모지 또는 Material 아이콘)'
    ],
    '예시 값': ['"상세 정보 보기"', 'True, False (기본값)', '"🔍", ":material/info:"']
})
st.dataframe(params_expander, width='stretch', hide_index=True)

st.code('''# 기본 확장기 (접힌 상태로 시작)
with st.expander("🔍 상세 정보 보기"):
    st.write("여기에 추가 정보를 넣습니다.")
    st.code("print('Hello, World!')", language="python")
    st.info("확장기 안에는 어떤 Streamlit 요소든 넣을 수 있습니다!")

# 펼쳐진 상태로 시작
with st.expander("📋 사용 방법 (기본 펼침)", expanded=True):
    st.write("""
    1. 확장기 제목을 클릭하면 접거나 펼 수 있습니다.
    2. `expanded=True`로 설정하면 기본으로 펼쳐집니다.
    3. 긴 콘텐츠를 숨겨서 화면을 깔끔하게 유지할 수 있습니다.
    """)''', language="python")

st.caption("▼ 실행 결과")

# 기본 확장기 (접힌 상태)
with st.expander("🔍 상세 정보 보기"):
    st.write("여기에 추가 정보를 넣습니다.")
    st.code("print('Hello, World!')", language="python")
    st.info("확장기 안에는 어떤 Streamlit 요소든 넣을 수 있습니다!")

# 펼쳐진 상태로 시작하는 확장기
with st.expander("📋 사용 방법 (기본 펼침)", expanded=True):
    st.write("""
    1. 확장기 제목을 클릭하면 접거나 펼 수 있습니다.
    2. `expanded=True`로 설정하면 기본으로 펼쳐집니다.
    3. 긴 콘텐츠를 숨겨서 화면을 깔끔하게 유지할 수 있습니다.
    """)

# =============================================================================
# 5. 빈 컨테이너 (Empty)
# =============================================================================
st.divider()
st.header("5. 빈 컨테이너 (Empty)")

st.write("- `st.empty()` : 동적으로 내용을 교체할 수 있는 플레이스홀더")
st.caption("- 용도: 로딩 상태 표시, 실시간 업데이트, 카운트다운 등 동적 콘텐츠에 사용")

# 파라미터 설명
st.caption("📌 특징: 현재 위치에 빈 자리 확보 → 나중에 내용을 동적으로 교체 가능")

st.code('''countdown_placeholder = st.empty()
st.write("카운트다운 버튼을 클릭하세요")

if st.button("🚀 카운트다운 시작"):
    for i in range(5, 0, -1):
        countdown_placeholder.metric("카운트다운", f"{i}초")
        time.sleep(1)
    countdown_placeholder.success("🎉 완료!")''', language="python")

st.caption("▼ 실행 결과")

countdown_placeholder = st.empty()
st.write("카운트다운 버튼을 클릭하세요")

if st.button("🚀 카운트다운 시작"):
    for i in range(5, 0, -1):
        countdown_placeholder.metric("카운트다운", f"{i}초")
        time.sleep(1)
    countdown_placeholder.success("🎉 완료!")

# =============================================================================
# 6. 간격 조절 (Space) 
# =============================================================================
st.divider()
st.header("6. 간격 조절 (Space)")

st.write("- `st.space(size)` : 요소 사이의 간격을 정밀하게 조절")
st.caption("- 용도: 버튼 정렬, 섹션 구분, 레이아웃 미세 조정에 사용")

# 파라미터 설명 테이블
params_space = pd.DataFrame({
    '파라미터': ['size'],
    '타입': ['str 또는 int'],
    '설명': ['간격 크기 (문자열 프리셋 또는 픽셀 정수)'],
    '예시 값': ['"small", "medium", "large", "stretch", 50, 100']
})
st.dataframe(params_space, width='stretch', hide_index=True)

# 크기 옵션 표
st.subheader("크기 옵션")
size_df = pd.DataFrame({
    '크기': ['"small" (기본)', '"medium"', '"large"', '"stretch"', '정수 (예: 50)'],
    '설명': ['약 12px', '약 40px', '약 68px', '남은 공간 전체', '지정한 픽셀'],
    '용도': ['위젯 라벨 높이만큼의 간격', '버튼 하나 높이만큼의 간격',
             '라벨이 있는 입력 필드 높이', '요소를 양쪽 끝으로 배치', '정확한 크기가 필요할 때']
})
st.dataframe(size_df, width='stretch', hide_index=True)

# -----------------------------------------------------------------------------
st.subheader("수직 간격 비교")

st.code('''col1, col2, col3, col4 = st.columns(4)

with col1:
    st.write("**small**")
    st.button("위")
    st.space("small")  # 약 12px
    st.button("아래")

with col2:
    st.write("**medium**")
    st.button("위")
    st.space("medium")  # 약 40px
    st.button("아래")

with col3:
    st.write("**large**")
    st.button("위")
    st.space("large")  # 약 68px
    st.button("아래")

with col4:
    st.write("**100px**")
    st.button("위")
    st.space(100)  # 정확히 100px
    st.button("아래")''', language="python")

st.caption("▼ 실행 결과")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.write("**small**")
    st.button("위 s")
    st.space("small")
    st.button("아래 s")

with col2:
    st.write("**medium**")
    st.button("위 m")
    st.space("medium")
    st.button("아래 m")

with col3:
    st.write("**large**")
    st.button("위 l")
    st.space("large")
    st.button("아래 l")

with col4:
    st.write("**100px**")
    st.button("위 p")
    st.space(100)
    st.button("아래 p")

# =============================================================================
# 7. 다이얼로그 (Dialog) - 모달 팝업 창
# =============================================================================
st.divider()
st.header("7. 다이얼로그 (Dialog)")

# @st.dialog: 모달 팝업 창을 생성하는 데코레이터
# 주요 파라미터:
# - title: 다이얼로그 창 제목 (필수)
# - width: 다이얼로그 너비 ("small", "large")
st.write("- `@st.dialog(title, width)` : 모달 팝업 창 생성 데코레이터")
st.caption("- 용도: 사용자 입력 폼, 확인 대화상자, 상세 정보 표시 등 집중이 필요한 작업에 사용")

# 파라미터 설명 테이블
params_dialog = pd.DataFrame({
    '파라미터': ['title', 'width'],
    '타입': ['str', 'str'],
    '설명': [
        '다이얼로그 창 상단에 표시될 제목',
        '다이얼로그 너비 설정'
    ],
    '예시 값': [
        '"사용자 정보 입력"',
        '"small" (기본), "large"'
    ]
})
st.dataframe(params_dialog, width='stretch', hide_index=True)

# 주요 특징 설명
st.subheader("주요 특징")
st.markdown("""
- `@st.dialog` 데코레이터로 함수를 다이얼로그로 변환
- 함수를 호출하면 다이얼로그가 열림
- `st.rerun()`을 호출하면 다이얼로그가 닫힘
- 다이얼로그 내부에서 모든 Streamlit 위젯 사용 가능
""")

# -----------------------------------------------------------------------------
st.subheader("(1) 기본 다이얼로그")
st.caption("버튼을 클릭하면 다이얼로그가 열리고, 내부 버튼으로 닫을 수 있습니다.")

st.code('''@st.dialog("📝 메시지 입력")
def message_dialog():
    """기본 다이얼로그 예제"""
    message = st.text_input("메시지를 입력하세요")

    if st.button("확인", type="primary"):
        if message:
            st.session_state.last_message = message
            st.rerun()  # 다이얼로그 닫기
        else:
            st.warning("메시지를 입력해주세요!")

# 다이얼로그 열기 버튼
if st.button("💬 메시지 입력하기"):
    message_dialog()

# 입력된 메시지 표시
if "last_message" in st.session_state:
    st.success(f"입력된 메시지: {st.session_state.last_message}")''', language="python")

st.caption("▼ 실행 결과")

@st.dialog("📝 메시지 입력")
def message_dialog():
    """기본 다이얼로그 예제"""
    message = st.text_input("메시지를 입력하세요")

    if st.button("확인", type="primary"):
        if message:
            st.session_state.last_message = message
            st.rerun()
        else:
            st.warning("메시지를 입력해주세요!")

if st.button("💬 메시지 입력하기"):
    message_dialog()

if "last_message" in st.session_state:
    st.success(f"입력된 메시지: {st.session_state.last_message}")

# -----------------------------------------------------------------------------
st.subheader("(2) 넓은 다이얼로그 (width='large')")
st.caption("더 많은 콘텐츠를 표시할 때는 넓은 다이얼로그를 사용합니다.")

st.code('''@st.dialog("📊 상세 정보", width="large")
def detail_dialog(item_name, item_data):
    """파라미터를 받는 넓은 다이얼로그"""
    st.write(f"**{item_name}** 상세 정보")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("판매량", f"{item_data['sales']:,}개")
        st.metric("재고", f"{item_data['stock']:,}개")
    with col2:
        st.metric("가격", f"₩{item_data['price']:,}")
        st.metric("평점", f"{item_data['rating']}/5.0")

    st.divider()
    new_price = st.number_input("가격 수정", value=item_data['price'], step=1000)

    if st.button("저장하고 닫기", type="primary"):
        st.session_state.updated_price = new_price
        st.rerun()

# 다이얼로그에 데이터 전달
sample_item = {"sales": 1250, "stock": 89, "price": 59000, "rating": 4.5}

if st.button("📦 상품 상세보기"):
    detail_dialog("무선 키보드", sample_item)

if "updated_price" in st.session_state:
    st.info(f"수정된 가격: ₩{st.session_state.updated_price:,}")''', language="python")

st.caption("▼ 실행 결과")

@st.dialog("📊 상세 정보", width="large")
def detail_dialog(item_name, item_data):
    """파라미터를 받는 넓은 다이얼로그"""
    st.write(f"**{item_name}** 상세 정보")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("판매량", f"{item_data['sales']:,}개")
        st.metric("재고", f"{item_data['stock']:,}개")
    with col2:
        st.metric("가격", f"₩{item_data['price']:,}")
        st.metric("평점", f"{item_data['rating']}/5.0")

    st.divider()
    new_price = st.number_input("가격 수정", value=item_data['price'], step=1000)

    if st.button("저장하고 닫기", type="primary"):
        st.session_state.updated_price = new_price
        st.rerun()

sample_item = {"sales": 1250, "stock": 89, "price": 59000, "rating": 4.5}

if st.button("📦 상품 상세보기"):
    detail_dialog("무선 키보드", sample_item)

if "updated_price" in st.session_state:
    st.info(f"수정된 가격: ₩{st.session_state.updated_price:,}")

# -----------------------------------------------------------------------------
st.subheader("(3) 확인/취소 다이얼로그")
st.caption("삭제 등 위험한 작업 전 사용자 확인을 받을 때 유용합니다.")

st.code('''@st.dialog("⚠️ 삭제 확인")
def confirm_delete_dialog(item_name):
    """확인/취소 버튼이 있는 다이얼로그"""
    st.warning(f"**{item_name}**을(를) 정말 삭제하시겠습니까?")
    st.caption("이 작업은 되돌릴 수 없습니다.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("취소", use_container_width=True):
            st.session_state.delete_result = "취소됨"
            st.rerun()
    with col2:
        if st.button("삭제", type="primary", use_container_width=True):
            st.session_state.delete_result = f"{item_name} 삭제 완료"
            st.rerun()

if st.button("🗑️ 항목 삭제"):
    confirm_delete_dialog("중요한 파일.txt")

if "delete_result" in st.session_state:
    if "삭제 완료" in st.session_state.delete_result:
        st.error(st.session_state.delete_result)
    else:
        st.info(st.session_state.delete_result)''', language="python")

st.caption("▼ 실행 결과")

@st.dialog("⚠️ 삭제 확인")
def confirm_delete_dialog(item_name):
    """확인/취소 버튼이 있는 다이얼로그"""
    st.warning(f"**{item_name}**을(를) 정말 삭제하시겠습니까?")
    st.caption("이 작업은 되돌릴 수 없습니다.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("취소", use_container_width=True):
            st.session_state.delete_result = "취소됨"
            st.rerun()
    with col2:
        if st.button("삭제", type="primary", use_container_width=True):
            st.session_state.delete_result = f"{item_name} 삭제 완료"
            st.rerun()

if st.button("🗑️ 항목 삭제"):
    confirm_delete_dialog("중요한 파일.txt")

if "delete_result" in st.session_state:
    if "삭제 완료" in st.session_state.delete_result:
        st.error(st.session_state.delete_result)
    else:
        st.info(st.session_state.delete_result)

st.divider()
st.caption("© 2025 Streamlit 레이아웃 실습 | 4장 레이아웃 구성")