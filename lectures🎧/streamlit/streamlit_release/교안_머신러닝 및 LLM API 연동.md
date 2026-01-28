# 📘 Streamlit API 및 머신러닝 연결

## 목차
- 6장: 머신러닝 모델 연동
- 7장: 외부 API 연결 (Gemini)

---

# 6장: 머신러닝 모델 연동

## 💪 이 장을 마치면 할 수 있어요
- 훈련된 ML 모델을 Streamlit에서 불러와 예측할 수 있어요

📚 **공식문서**: [@st.cache_resource](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.cache_resource)

**파일명**: `06_ml_and_api/main.py`

---

## 🚨 핵심 원칙

**Streamlit 앱에서 모델을 훈련하면 안 됩니다!**

```
[올바른 워크플로우]
1. 별도 스크립트에서 모델 훈련
2. 훈련된 모델을 파일로 저장 (.pkl)
3. Streamlit 앱에서 로드하여 예측만 수행
```

**이유**: Streamlit은 인터랙션마다 스크립트가 재실행됨 → 매번 훈련하면 너무 느림

---

## 6.1 모델 훈련 및 저장

**파일: `train_model.py` (별도 실행)**

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import pickle

# 데이터 로드 및 훈련
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 모델 저장
with open("iris_model.pkl", "wb") as f:
    pickle.dump(model, f)
print("저장 완료!")
```

실행: `python train_model.py`

---

## 6.2 Streamlit 앱에서 모델 로드

**파일: `app.py`**

```python
import streamlit as st
import pickle
import numpy as np

# 모델 로드 (캐싱 필수!)
@st.cache_resource
def load_model():
    with open("iris_model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

st.title("🌸 붓꽃 품종 예측")

col1, col2 = st.columns(2)
with col1:
    sepal_length = st.slider("꽃받침 길이", 4.0, 8.0, 5.0)
    sepal_width = st.slider("꽃받침 너비", 2.0, 4.5, 3.0)
with col2:
    petal_length = st.slider("꽃잎 길이", 1.0, 7.0, 4.0)
    petal_width = st.slider("꽃잎 너비", 0.1, 2.5, 1.0)

# 예측
input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
prediction = model.predict(input_data)[0]

species = ["Setosa", "Versicolor", "Virginica"]
st.success(f"예측: **{species[prediction]}**")
```

---

# 7장: 외부 API 연결

## 💪 이 장을 마치면 할 수 있어요
- Gemini API를 연동하여 챗봇을 만들 수 있어요
- secrets.toml로 API 키를 관리할 수 있어요

📚 **공식문서**: [Streamlit Secrets](https://docs.streamlit.io/develop/concepts/connections/secrets-management)

**파일명**: `06_gemini_chat.py`

---

## 7.1 API 키 설정

```toml
# .streamlit/secrets.toml
GEMINI_API_KEY = "your-api-key"
```

⚠️ `secrets.toml`은 `.gitignore`에 추가!

---

## 7.2 Gemini 챗봇 (Multi-turn)

### 설치
```bash
pip install google-genai
```

### 코드

```python
import streamlit as st
from google import genai

# 클라이언트 초기화
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.title("🤖 Gemini 챗봇")

# 세션 상태 초기화
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(model="gemini-2.5-flash-lite")
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 메시지 표시
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 사용자 입력
if prompt := st.chat_input("메시지 입력"):
    # 사용자 메시지 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # AI 응답
    with st.chat_message("assistant"):
        response = st.session_state.chat.send_message(prompt)
        st.write(response.text)

    st.session_state.messages.append({"role": "assistant", "content": response.text})
```

---

# 핵심 요약

| 기능 | 코드 |
|------|------|
| API 키 | `st.secrets["KEY"]` |
| 모델 캐싱 | `@st.cache_resource` |
| 채팅 UI | `st.chat_input()`, `st.chat_message()` |
| 모델 저장 | `pickle.dump(model, file)` |
| 모델 로드 | `pickle.load(file)` |

## 🚨 주의사항
1. API 키는 `secrets.toml`에 저장
2. `secrets.toml`은 `.gitignore`에 추가
3. ML 모델은 **별도 스크립트에서 훈련** 후 저장
4. `@st.cache_resource`로 모델 로드 시 캐싱 필수
