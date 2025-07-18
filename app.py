import streamlit as st
import google.generativeai as genai

# --- 1. 페이지 설정 및 제목 ---
st.set_page_config(
    page_title="AI 리더십 특성 3줄 요약기",
    page_icon="👨‍💼",
    layout="wide",
)
st.title("👨‍💼 AI 리더십 특성 3줄 요약")
st.caption("리더의 강점과 약점에 대한 의견을 입력하면, Gemini AI가 핵심 특성을 3줄로 요약합니다.")


# --- 2. Gemini API 설정 ---
# 경고: 실제 운영 환경에서는 보안을 위해 API 키를 코드에 직접 노출하지 마세요.
# Streamlit의 secrets management 기능을 사용하는 것이 가장 안전합니다.
API_KEY = "AIzaSyAUQxQMUcE1GKMoQTF1Qfm9s7_2mxeK5c8" # 제공된 예시 키

try:
    # API 키 설정
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"API 키 설정 중 오류가 발생했습니다: {e}")
    st.stop() # API 키 설정 실패 시 앱 실행 중지

# --- 3. 모델 및 프롬프트 설정 ---
# API 요청에 사용할 설정값 (제공된 예시와 동일하게)
generation_config = genai.GenerationConfig(
    temperature=0.7,
)

# AI의 역할을 정의하는 시스템 명령어
SYSTEM_INSTRUCTION = """
당신은 리더십을 정확하고 간결하게 분석하는 전문가입니다.
사용자가 리더의 강점과 약점에 대한 의견을 전달하면, 아래의 규칙에 따라 리더십 특성을 3줄로 요약해야 합니다.

**[요약 규칙]**
1.  결과는 반드시 3개의 문장으로만 구성해야 합니다.
2.  각 문장은 12단어 이하의 간결한 문장이어야 합니다.
3.  각 문장의 끝은 반드시 '~함' 또는 '~임'으로 끝나야 합니다.
4.  첫 번째 문장은 강점, 두 번째 문장은 약점, 세 번째 문장은 종합 평가를 담아야 합니다.
5.  규칙 설명이나 다른 불필요한 말 없이, 요약된 3줄의 문장만 출력해야 합니다.
"""

try:
    # GenerativeModel 객체 생성 (제공된 예시와 동일한 파라미터 사용)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_INSTRUCTION,
        generation_config=generation_config,
    )
except Exception as e:
    st.error(f"Gemini 모델 초기화 중 오류가 발생했습니다: {e}")
    st.stop() # 모델 초기화 실패 시 앱 실행 중지


# --- 4. 웹 UI 및 사용자 입력 ---
st.write("") # 여백
col1, col2 = st.columns(2)
with col1:
    strengths_input = st.text_area("👍 **강점** 또는 **칭찬할 점**을 상세히 입력하세요.", placeholder="예: 팀원들의 의견을 항상 경청하고 존중하며, 명확한 비전과 방향성을 제시해줍니다. 위기 상황에서도 침착하게 팀을 이끌어 신뢰를 줍니다.", height=200)

with col2:
    weaknesses_input = st.text_area("👎 **약점** 또는 **개선점**을 상세히 입력하세요.", placeholder="예: 때로는 업무 위임보다 직접 모든 것을 처리하려는 경향이 있어 팀원들의 성장을 저해할 수 있습니다. 결정된 사항에 대한 피드백이 조금 더 빠르면 좋겠습니다.", height=200)


# --- 5. 요약 생성 버튼 및 API 호출 ---
if st.button("✨ AI로 요약 생성하기", type="primary"):
    # 입력 값 검증
    if not strengths_input.strip() or not weaknesses_input.strip():
        st.warning("❗ 강점과 약점 내용을 모두 입력해야 분석할 수 있습니다.")
    else:
        # AI에게 전달할 최종 프롬프트 구성
        user_prompt = f"""
        [강점 의견]
        {strengths_input}

        [약점 의견]
        {weaknesses_input}
        """
        
        with st.spinner("Gemini가 리더십 특성을 분석하고 있습니다..."):
            try:
                # 스트리밍 방식으로 API 호출 (제공된 예시와 동일한 메소드 사용)
                response_stream = model.generate_content(
                    user_prompt,
                    stream=True,
                )

                st.write("---")
                st.subheader("🤖 Gemini 요약 결과")
                
                # 스트림으로 들어오는 결과를 실시간으로 화면에 출력
                st.write_stream(chunk.text for chunk in response_stream)

            except Exception as e:
                st.error(f"API 호출 중 오류가 발생했습니다. API 키가 유효한지 또는 모델 이름('gemini-1.5-flash')이 올바른지 확인해 주세요.\n\n오류 상세: {e}")

# --- 6. 앱 정보 ---
st.markdown("---")
st.info("이 앱은 Google Gemini API를 사용하여 텍스트를 요약합니다. 제공된 API 키는 예시이며, 실제 환경에서는 Streamlit Secrets 등 안전한 방법을 통해 관리해야 합니다.")
