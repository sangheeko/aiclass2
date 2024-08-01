import textwrap
import google.generativeai as genai
import streamlit as st

def to_markdown(text):
    text = text.replace('•', '*')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

api_key = "AIzaSyDl8qvlDLVhF0WbRldoMaaidKPEZmTXrH0"

# 콘텐츠 생성 함수
def try_generate_content(api_key, prompt):
    genai.configure(api_key=api_key)
   
    try:
        response = genai.generate(
            model="gemini-1.5-flash",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            top_p=1,
            top_k=1,
            max_tokens=2048,
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            ]
        )
        # 응답에서 텍스트 추출
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"API 호출 실패: {e}")
        return None

# Streamlit 앱
st.title("지진대와 국가의 거리 확인")
st.write("국가 이름을 입력하면 해당 국가와 주요 지진대(불의 고리) 간의 거리를 확인할 수 있습니다.")

country_name = st.text_input("국가 이름을 입력하세요:")

if st.button("확인"):
    if country_name:
        # 지진대와의 거리 계산을 위한 프롬프트 생성
        prompt = f"{country_name}는 주요 지진대와 얼마나 가까운가요?"
        response = try_generate_content(api_key, prompt)
        if response:
            st.markdown(to_markdown(response))
        else:
            st.error("정보를 가져오는 데 실패했습니다.")
    else:
        st.warning("국가 이름을 입력해주세요.")
