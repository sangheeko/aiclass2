import textwrap
import google.generativeai as genai
import streamlit as st
from datetime import datetime, time
import toml
import pathlib

def to_markdown(text):
    text = text.replace('•', '*')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# secrets.toml 파일 경로
secrets_path = pathlib.Path(__file__).parent.parent / ".streamlit/secrets.toml"

# secrets.toml 파일 읽기
with open(secrets_path, "r") as f:
    secrets = toml.load(f)

# secrets.toml 파일에서 API 키 값 가져오기
api_key = secrets.get("api_key")

# 콘텐츠 생성 함수
def try_generate_content(api_key, prompt):
    # API 키 설정
    genai.configure(api_key=api_key)
   
    try:
        # 콘텐츠 생성
        response = genai.generate(
            model="gemini-1.5-flash",
            prompt=prompt,
            max_tokens=2048,
            temperature=0.9,
            top_p=1,
            top_k=1
        )
        return response[0]['text']  # 예상 생성된 텍스트 반환
    except Exception as e:
        print(f"API 호출 실패: {e}")
        return None

# Streamlit 앱
st.title("지구의 크기 측정 실험")
st.write("에라토스테네스의 방법을 이용하여 지구의 크기를 측정합니다. 실험 시간에 따른 지구본의 측정 위치를 제공합니다.")

# 실험 시간 입력
experiment_time = st.time_input("실험 시간을 입력하세요:", value=time(12, 0))  # 기본 시간 12:00

# 실험 시간에 따른 결과 생성
if st.button("확인"):
    time_str = experiment_time.strftime("%H:%M")
    prompt = f"시간 {time_str}에 지구본에서 그림자가 생기지 않는 곳과 생기는 곳의 경도를 계산해줘."
    response = try_generate_content(api_key, prompt)
    if response:
        st.markdown(to_markdown(response))
    else:
        st.error("정보를 가져오는 데 실패했습니다. API 키와 네트워크 연결을 확인해주세요.")
