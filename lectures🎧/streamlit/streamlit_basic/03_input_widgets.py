# 터미널 창에 입력
# 라이브러리 설치 : pip install streamlit pandas
# Streamlit App 실행 : streamlit run .\03_input_widgets.py

import streamlit as st
import pandas as pd
import datetime

st.title("입력 위젯 (Input Widgets)")

# =============================================================================
# 1. 텍스트 입력
st.header("1. 텍스트 입력")

# st.text_input(): 한 줄 텍스트 입력 위젯
# 주요 파라미터:
# - label: 입력 필드 위에 표시되는 레이블
# - value: 기본값 (초기 입력값)
# - placeholder: 입력 전 힌트 텍스트 (회색으로 표시)
# - max_chars: 최대 입력 글자 수
# - type: "default" 또는 "password" (비밀번호 입력용)
# - disabled: True면 입력 비활성화
# - label_visibility: "visible", "hidden", "collapsed"
# - help: 도움말 텍스트 (? 아이콘으로 표시)
st.write("(1) **st.text_input(value, placeholder, max_chars, help):** 한 줄 텍스트 입력")
st.write("**용도:** 이름, 이메일, 검색어 등 짧은 텍스트 입력 시 사용")

name = st.text_input(
    label="이름을 입력하세요",
    value="",  # 기본값 (빈 문자열)
    placeholder="홍길동",  # 힌트 텍스트
    max_chars=10,  # 최대 10글자
    help="이름은 최대 10자까지 입력 가능합니다"  # 도움말 (? 아이콘)
)
if name:
    st.write(f"입력한 이름: **{name}**")

st.divider()

# 비밀번호 입력 (type="password")
st.write("(2) **st.text_input(type='password'):** 비밀번호 입력")
st.write("**용도:** 비밀번호, PIN 등 민감한 정보 입력 시 사용 (입력값이 *로 표시)")

password = st.text_input(
    label="비밀번호를 입력하세요",
    type="password",  # 입력 내용이 *로 표시됨
    placeholder="8자 이상 입력",
    max_chars=20,
    help="비밀번호는 8~20자로 설정하세요"
)
st.divider()

# st.text_area(): 여러 줄 텍스트 입력 위젯
# 주요 파라미터:
# - height: 텍스트 영역 높이 (픽셀)
# - max_chars: 최대 입력 글자 수
# - help: 도움말 텍스트 (? 아이콘으로 표시)
st.write("(3) **st.text_area(height, max_chars, placeholder, help):** 여러 줄 텍스트 입력")
st.write("**용도:** 자기소개, 리뷰, 문의사항 등 긴 텍스트 입력 시 사용")

message = st.text_area(
    label="자기소개를 작성하세요",
    value="",  # 기본값
    height=150,  # 높이 150픽셀
    max_chars=200,  # 최대 200자
    placeholder="간단한 자기소개를 입력해주세요...\n여러 줄로 작성 가능합니다.",
    help="최대 200자까지 입력 가능합니다"
)
if message:
    st.write(f"작성한 내용 ({len(message)}자):")
    # st.write()는 줄바꿈(\n)을 무시함 → st.text() 사용하면 줄바꿈 유지
    st.text(message)

# =============================================================================
# 2. 숫자 입력
st.divider()
st.header("2. 숫자 입력")

# st.number_input(): 숫자 전용 입력 위젯 (증감 버튼 제공)
# 주요 파라미터:
# - min_value: 최소값
# - max_value: 최대값
# - value: 기본값
# - step: 증감 단위
# - format: 표시 형식 (예: "%.2f" 소수점 2자리)
# - help: 도움말 텍스트 (? 아이콘으로 표시)
st.write("(1) **st.number_input(min_value, max_value, value, step, help):** 정수 입력")
st.write("**용도:** 나이, 수량, 개수 등 정수 입력 시 사용")

age = st.number_input(
    label="나이를 입력하세요",
    min_value=0,  # 최소값
    max_value=150,  # 최대값
    value=25,  # 기본값
    step=1,  # 증감 단위
    help="0~150 사이의 정수를 입력하세요"
)
st.write(f"입력한 나이: **{age}세**")

st.divider()

# 소수점 입력 예제
st.write("(2) **st.number_input(min_value, max_value, value, step, format):** 소수점 입력")
st.write("**용도:** 체중, 가격, 비율 등 소수점이 필요한 숫자 입력 시 사용")

weight = st.number_input(
    label="체중을 입력하세요 (kg)",
    min_value=0.0,  # 소수점 사용
    max_value=300.0,
    value=65.5,  # 기본값
    step=0.1,  # 0.1kg 단위
    format="%.1f",  # 소수점 1자리까지 표시
    help="소수점 첫째자리까지 입력 가능합니다"
)
st.write(f"입력한 체중: **{weight:.1f}kg**")

# =============================================================================
# 3. 슬라이더
st.divider()
st.header("3. 슬라이더")

# st.slider(): 슬라이더로 값 선택
# 주요 파라미터:
# - min_value: 최소값
# - max_value: 최대값
# - value: 기본값 (튜플로 지정하면 범위 슬라이더)
# - step: 증감 단위
# - format: 표시 형식
# - help: 도움말 텍스트
# 단일값 슬라이더
st.subheader("단일값 슬라이더")
st.write("(1) **st.slider(min_value, max_value, value, step, format):** 슬라이더로 값 선택")
st.write("**용도:** 온도, 볼륨, 밝기 등 범위 내 단일값 선택 시 사용")
temperature = st.slider(
    label="온도 설정",
    min_value=-10,
    max_value=40,
    value=20,  # 기본값
    step=1,
    format="%d°C",  # 표시 형식
    help="에어컨 온도를 설정하세요"
)
st.write(f"설정 온도: **{temperature}°C**")

st.divider()

# 범위 슬라이더 (value에 튜플 지정)
st.subheader("범위 슬라이더")
st.write("(2) **st.slider(value=(min, max)):** 범위 슬라이더 (튜플로 지정)")
st.write("**용도:** 가격 범위, 날짜 범위 등 최소/최대값을 동시에 선택 시 사용")
price_range = st.slider(
    label="가격 범위 선택",
    min_value=0,
    max_value=1000000,
    value=(100000, 500000),  # 튜플로 지정하면 범위 선택 가능
    step=10000,
    format="₩%d",  # 표시 형식
    help="최소/최대 가격을 드래그하여 설정하세요"
)
st.write(f"선택된 가격 범위: **₩{price_range[0]:,} ~ ₩{price_range[1]:,}**")

st.divider()

# st.select_slider(): 이산형 값 슬라이더
st.subheader("선택 슬라이더")
st.write("(3) **st.select_slider(options, value, help):** 정해진 옵션 중 선택")
st.write("**용도:** 사이즈, 등급, 레벨 등 불연속적인 값 선택 시 사용")

size = st.select_slider(
    label="티셔츠 사이즈 선택",
    options=["XS", "S", "M", "L", "XL", "XXL"],
    value="M",  # 기본값
    help="원하는 사이즈를 선택하세요"
)
st.write(f"선택한 사이즈: **{size}**")

# =============================================================================
# 4. 선택 상자
st.divider()
st.header("4. 선택 상자")

# st.selectbox(): 드롭다운 메뉴로 단일 항목 선택
# 주요 파라미터:
# - options: 선택 가능한 항목 리스트
# - index: 기본 선택 인덱스 (0부터 시작), None이면 placeholder 표시
# - placeholder: 선택 전 힌트 텍스트
# - disabled: True면 선택 비활성화
# - help: 도움말 텍스트 (? 아이콘으로 표시)
st.write("**st.selectbox(options, index, placeholder, help):** 드롭다운 단일 선택")
st.write("**용도:** 도시, 국가, 카테고리 등 여러 옵션 중 하나만 선택 시 사용")

city = st.selectbox(
    label="거주 도시를 선택하세요",
    options=["서울", "부산", "대구", "인천", "광주", "대전", "울산"],
    index=None,  # None이면 placeholder 표시
    placeholder="도시를 선택하세요...",  # 선택 전 표시
    help="현재 거주하고 있는 도시를 선택해주세요"
)
if city:
    st.write(f"선택한 도시: **{city}**")
else:
    st.info("도시를 선택해주세요")

# =============================================================================
# 5. 다중 선택
st.divider()
st.header("5. 다중 선택")

# st.multiselect(): 여러 항목을 동시에 선택 가능한 위젯
# 주요 파라미터:
# - options: 선택 가능한 항목 리스트
# - default: 기본 선택 항목 리스트
# - max_selections: 최대 선택 가능 개수
# - placeholder: 선택 전 힌트 텍스트
# - help: 도움말 텍스트 (? 아이콘으로 표시)
st.write("**st.multiselect(options, default, max_selections, placeholder, help):** 복수 항목 선택")
st.write("**용도:** 취미, 관심분야, 태그 등 여러 항목을 동시에 선택 시 사용")

hobbies = st.multiselect(
    label="취미를 선택하세요",
    options=["영화 감상", "독서", "운동", "음악 감상", "여행", "요리", "게임", "사진촬영"],
    default=["독서"],  # 기본 선택값
    max_selections=3,  # 최대 3개까지만 선택 가능
    placeholder="취미를 선택하세요 (최대 3개)",
    help="관심있는 취미를 최대 3개까지 선택할 수 있습니다"
)

if hobbies:
    st.write(f"선택한 취미 ({len(hobbies)}개): **{', '.join(hobbies)}**")
else:
    st.info("취미를 선택해주세요")

# =============================================================================
# 6. 라디오 버튼
st.divider()
st.header("6. 라디오 버튼")

# st.radio(): 단일 선택 라디오 버튼 (모든 옵션이 화면에 표시됨)
# 주요 파라미터:
# - options: 선택 가능한 항목 리스트
# - index: 기본 선택 인덱스 (None이면 선택 안함)
# - horizontal: True면 가로 배열, False면 세로 배열
# - captions: 각 옵션에 대한 설명 리스트
# - help: 도움말 텍스트 (? 아이콘으로 표시)
st.write("(1) **st.radio(options, index, captions, help):** 라디오 버튼 단일 선택")
st.write("**용도:** 성별, 결제방법 등 모든 옵션을 보여주고 하나만 선택 시 사용")

# 세로 배열 + captions 사용
gender = st.radio(
    label="성별을 선택하세요",
    options=["남성", "여성", "기타"],
    index=0,  # 기본값: 첫 번째 항목
    captions=["Male", "Female", "Other"],  # 각 항목 아래 작은 설명
    help="해당하는 성별을 선택해주세요"
)
st.write(f"선택한 성별: **{gender}**")

st.divider()

# 가로 배열 + index=None (선택 안함)
st.write("(2) **st.radio(horizontal=True):** 가로 배열")
st.write("**용도:** 만족도, 평점 등 가로로 나열해서 보여줄 때 사용")

satisfaction = st.radio(
    label="서비스 만족도를 선택하세요",
    options=["매우 불만족", "불만족", "보통", "만족", "매우 만족"],
    index=None,  # 기본 선택 없음
    horizontal=True,  # 가로 배열
    help="서비스에 대한 만족도를 평가해주세요"
)
if satisfaction:
    st.write(f"선택한 만족도: **{satisfaction}**")
else:
    st.info("만족도를 선택해주세요")

# =============================================================================
# 7. 체크박스
st.divider()
st.header("7. 체크박스")

# st.checkbox(): True/False 값을 반환하는 체크박스
# 주요 파라미터:
# - label: 체크박스 옆에 표시되는 텍스트
# - value: 기본값 (True=체크됨, False=해제)
# - disabled: True면 체크 비활성화
# - help: 도움말 텍스트
st.write("**st.checkbox(value, help):** 체크박스 (True/False 반환)")
st.write("**용도:** 약관 동의, 옵션 선택 등 예/아니오 선택 시 사용")

agree = st.checkbox(
    label="개인정보 처리방침에 동의합니다 (필수)",
    value=False,  # 기본값: 체크 안됨
    help="서비스 이용을 위해 필수로 동의해야 합니다"
)

marketing = st.checkbox(
    label="마케팅 정보 수신에 동의합니다 (선택)",
    value=False,
    help="이벤트, 할인 정보 등을 받아보실 수 있습니다"
)

newsletter = st.checkbox(
    label="뉴스레터 수신에 동의합니다 (선택)",
    value=True,  # 기본값: 체크됨
    help="주간 뉴스레터를 이메일로 받아보실 수 있습니다"
)

# 조건부 메시지 표시
st.write("**동의 현황:**")
col1, col2, col3 = st.columns(3)
with col1:
    if agree:
        st.success("개인정보: 동의")
    else:
        st.error("개인정보: 미동의")
with col2:
    if marketing:
        st.success("마케팅: 동의")
    else:
        st.warning("마케팅: 미동의")
with col3:
    if newsletter:
        st.success("뉴스레터: 동의")
    else:
        st.warning("뉴스레터: 미동의")

# =============================================================================
# 8. 토글 스위치
st.divider()
st.header("8. 토글 스위치")

# st.toggle(): 온/오프 토글 스위치
# 주요 파라미터:
# - label: 토글 옆에 표시되는 텍스트
# - value: 기본값 (True=켜짐, False=꺼짐)
# - disabled: True면 토글 비활성화
# - help: 도움말 텍스트
st.write("**st.toggle(value, help):** 토글 스위치 (On/Off)")
st.write("**용도:** 다크모드, 알림 설정 등 켜기/끄기 선택 시 사용")

col1, col2 = st.columns(2)

with col1:
    dark_mode = st.toggle(
        label="다크 모드",
        value=False,
        help="화면을 어두운 테마로 변경합니다"
    )
    st.write(f"상태: **{'켜짐' if dark_mode else '꺼짐'}**")

with col2:
    notifications = st.toggle(
        label="알림 설정",
        value=True,
        help="푸시 알림을 받을지 설정합니다"
    )
    st.write(f"상태: **{'켜짐' if notifications else '꺼짐'}**")

# =============================================================================
# 9. 버튼
st.divider()
st.header("9. 버튼")

# st.button(): 클릭 버튼 (클릭 시 True 반환)
# 주요 파라미터:
# - label: 버튼에 표시되는 텍스트
# - type: "primary" (강조) 또는 "secondary" (기본)
# - disabled: True면 버튼 비활성화
# - icon: 버튼 아이콘 (이모지 또는 :material/아이콘명:)
# - help: 도움말 텍스트
st.write("**st.button(type, icon, disabled, help):** 클릭 버튼")
st.write("**용도:** 폼 제출, 실행, 저장 등 사용자 액션 트리거 시 사용")

# 버튼 타입 비교
col1, col2 = st.columns(2)

with col1:
    if st.button(
        label="기본 버튼",
        type="secondary",  # 기본 스타일
        icon="📌",  # 아이콘 추가
        help="기본 스타일의 버튼입니다"
    ):
        st.info("기본 버튼 클릭!")

with col2:
    if st.button(
        label="강조 버튼",
        type="primary",  # 강조 스타일 (파란색)
        icon=":material/star:",  # Material 아이콘
        help="강조 스타일의 버튼입니다"
    ):
        st.success("Primary 버튼 클릭!")

st.divider()

# 전체 너비 버튼 + 이름 연동
if st.button(
    label="인사하기",
    type="primary",
    icon="👋",
    disabled=not name,  # 이름이 없으면 비활성화
    help="위에서 이름을 입력하면 활성화됩니다"
):
    st.balloons()
    st.success(f"안녕하세요, {name}님!")

if not name:
    st.caption("버튼을 활성화하려면 위에서 이름을 먼저 입력하세요")

# =============================================================================
# 10. 날짜/시간 입력
st.divider()
st.header("10. 날짜/시간 입력")

# st.date_input(): 날짜 선택기
# 주요 파라미터:
# - value: 기본 날짜 (datetime.date 객체) 또는 튜플 (범위 선택)
# - min_value: 선택 가능한 최소 날짜
# - max_value: 선택 가능한 최대 날짜
# - format: 날짜 표시 형식 (예: "YYYY-MM-DD", "DD/MM/YYYY")
# - help: 도움말 텍스트 (? 아이콘으로 표시)
st.write("(1) **st.date_input(value, min_value, max_value, format):** 날짜 선택")
st.write("**용도:** 생년월일, 예약일 등 날짜 선택 시 사용")

birthday = st.date_input(
    label="생일을 선택하세요",
    value=datetime.date(2000, 1, 1),  # 기본값
    min_value=datetime.date(1900, 1, 1),  # 최소 날짜
    max_value=datetime.date.today(),  # 최대 날짜 (오늘)
    format="YYYY-MM-DD",  # 표시 형식
    help="생년월일을 선택해주세요"
)
st.write(f"선택한 생일: **{birthday}** ({datetime.date.today().year - birthday.year}세)")

st.divider()

# 날짜 범위 선택
st.write("(2) **st.date_input(value=(시작일, 종료일)):** 날짜 범위 선택")
st.write("**용도:** 휴가 기간, 예약 기간 등 시작일~종료일 선택 시 사용")

date_range = st.date_input(
    label="휴가 기간을 선택하세요",
    value=(datetime.date.today(), datetime.date.today() + datetime.timedelta(days=7)),  # 기본 범위
    min_value=datetime.date.today(),  # 오늘부터
    max_value=datetime.date.today() + datetime.timedelta(days=365),  # 1년 이내
    format="YYYY-MM-DD",
    help="시작일과 종료일을 선택하세요"
)
if len(date_range) == 2:
    days = (date_range[1] - date_range[0]).days
    st.write(f"휴가 기간: **{date_range[0]} ~ {date_range[1]}** ({days}일)")

st.divider()

# st.time_input(): 시간 선택기
# 주요 파라미터:
# - value: 기본 시간 (datetime.time 객체)
# - step: 시간 선택 간격 (timedelta, 초 단위 정수도 가능)
# - help: 도움말 텍스트 (? 아이콘으로 표시)
st.write("(3) **st.time_input(value, step, help):** 시간 선택")
st.write("**용도:** 약속 시간, 알람 시간 등 시간 선택 시 사용")

appointment_time = st.time_input(
    label="약속 시간을 선택하세요",
    value=datetime.time(14, 30),  # 기본값: 오후 2시 30분
    step=datetime.timedelta(minutes=15),  # 15분 단위로 선택
    help="15분 단위로 시간을 선택할 수 있습니다"
)
st.write(f"선택한 시간: **{appointment_time.strftime('%H:%M')}** ({appointment_time.strftime('%p')})")

# =============================================================================
# 11. 색상 선택
st.divider()
st.header("11. 색상 선택")

# st.color_picker(): 색상 선택기
# 주요 파라미터:
# - value: 기본 색상 (HEX 코드)
# - label_visibility: "visible", "hidden", "collapsed"
# - help: 도움말 텍스트 (? 아이콘으로 표시)
st.write("**st.color_picker(value, help):** 색상 선택")
st.write("**용도:** 테마 색상, 배경색 등 색상 선택 시 사용")

col1, col2 = st.columns(2)

with col1:
    text_color = st.color_picker(
        label="텍스트 색상",
        value="#FFFFFF",  # 기본값: 흰색
        help="텍스트 색상을 선택하세요"
    )
    st.write(f"선택: **{text_color}**")

with col2:
    bg_color = st.color_picker(
        label="배경 색상",
        value="#FF5733",  # 기본값: 주황색
        help="배경 색상을 선택하세요"
    )
    st.write(f"선택: **{bg_color}**")

# 선택한 색상으로 미리보기
# st.markdown(): 마크다운 텍스트 렌더링 (HTML도 지원)
# 주요 파라미터:
# - body: 마크다운 또는 HTML 문자열
# - unsafe_allow_html: True면 HTML 태그 허용 (기본값 False)
st.write("**st.markdown(body, unsafe_allow_html):** HTML로 커스텀 요소 생성")
st.write("**용도:** 마크다운으로 표현 불가능한 커스텀 스타일링, CSS 적용 시 사용")
st.write("**색상 미리보기:**")
st.markdown(
    f'<div style="background-color: {bg_color}; padding: 30px; border-radius: 10px; text-align: center;">'
    f'<span style="color: {text_color}; font-weight: bold; font-size: 20px;">Hello, Streamlit!</span>'
    f'</div>',
    unsafe_allow_html=True
)

# =============================================================================
# 12. 파일 업로드
st.divider()
st.header("12. 파일 업로드")

# st.file_uploader(): 파일 업로드 위젯
# 주요 파라미터:
# - type: 허용할 파일 확장자 리스트
# - accept_multiple_files: True면 여러 파일 업로드 가능
# - label_visibility: 레이블 표시 설정
# - help: 도움말 텍스트 (? 아이콘으로 표시)
st.write("**st.file_uploader(type, accept_multiple_files, help):** 파일 업로드")
st.write("**용도:** 이미지, 문서 등 파일 업로드 시 사용")

uploaded_file = st.file_uploader(
    label="이미지 파일을 업로드하세요",
    type=["png", "jpg", "jpeg", "gif"],  # 허용 확장자
    accept_multiple_files=False,  # 단일 파일만
    help="PNG, JPG, JPEG, GIF 파일만 업로드 가능합니다"
)

if uploaded_file is not None:
    st.write(f"**파일명:** {uploaded_file.name}")
    st.write(f"**파일 크기:** {uploaded_file.size / 1024:.1f} KB")
    st.write(f"**파일 타입:** {uploaded_file.type}")
    st.image(uploaded_file, caption="업로드된 이미지", width='stretch')

# =============================================================================
# 13. 파일 다운로드
st.divider()
st.header("13. 파일 다운로드")

# st.download_button(): 파일 다운로드 버튼
# 주요 파라미터:
# - label: 버튼 텍스트
# - data: 다운로드할 데이터 (문자열, 바이트)
# - file_name: 다운로드될 파일명
# - mime: 파일 MIME 타입 (text/csv, application/json, text/plain 등)
st.write("**st.download_button(label, data, file_name, mime):** 파일 다운로드 버튼")
st.write("**용도:** 분석 결과, 보고서, 설정 파일 등을 사용자가 다운로드할 수 있게 할 때 사용")

# CSV 파일 다운로드
st.subheader("CSV 파일 다운로드")

download_df = pd.DataFrame({
    '이름': ['김철수', '이영희', '박민수'],
    '점수': [85, 92, 78]
})
st.dataframe(download_df)

csv = download_df.to_csv(index=False).encode('utf-8-sig')  # 한글 깨짐 방지

st.download_button(
    label="CSV 파일 다운로드",
    data=csv,
    file_name="scores.csv",
    mime="text/csv"
)
