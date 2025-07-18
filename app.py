import streamlit as st
import google.generativeai as genai
import os

# --- Gemini API를 사용하여 리더십 특성을 요약하는 함수 ---
def summarize_leadership_with_gemini(api_key, strengths_text, weaknesses_text):
    """Gemini AI 모델을 호출하여 리더십 강점/약점 텍스트를 3줄로 요약하는 함수"""
    try:
        # API 키 설정
        genai.configure(api_key=api_key)
        
        # 사용할 모델 선택
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash", # 빠르고 효율적인 모델
            system_instruction="당신은 리더십을 정확하게 분석하고 평가하는 전문가입니다."
        )

        # AI에게 전달할 프롬프트(지시문) 구성
        prompt = f"""
        아래에 제시된 리더의 '강점'과 '약점'에 대한 의견을 바탕으로, 리더십 특성을 3줄로 요약해줘.

        **반드시 지켜야 할 규칙:**
        1.  결과는 반드시 3개의 문장으로만 구성되어야 함.
        2.  각 문장은 12단어 이하로 간결하게 작성해야 함.
        3.  각 문장은 반드시 '~함' 또는 '~임'으로 끝나야 함.
        4.  첫 문장은 강점, 두 번째 문장은 약점, 세 번째 문장은 종합적인 평가를 담아야 함.
        5.  다른 설명 없이, 요약된 3개의 문장만 출력해야 함.

        ---
        [강점 의견]
        {strengths_text}

        [약점 의견]
        {weaknesses_text}
        ---
        """

        # AI 모델로부터 답변 생성 요청
        response = model.generate_content(prompt)
        
        # 결과 텍스트를 줄바꿈 기준으로 분리하여 리스트로 반환
        summary_lines = response.text.strip().split('\n')
        
        # 3줄이 아닐 경우 예외처리
        if len(summary_lines) != 3:
            return ["AI 모델이 형식에 맞게 생성하지 못했습니다. 내용을 조금 더 구체적으로 작성 후 다시 시도해주세요."]

        return summary_lines

    except Exception as e:
        # API 키 오류나 다른 예외 발생 시 사용자에게 알림
        return [f"오류가 발생했습니다: {e}", "API 키가 올바른지 확인해주세요.", "내용을 다시 확인 후 시도해주세요."]


# --- Streamlit UI 구성 ---

# 페이지 기본 설정
st.set_page_config(page_title="AI 리더십 특성 요약기", page_icon="👨‍💼", layout="wide")

# 사이드바에 API 키 입력 필드 추가
with st.sidebar:
    st.header("🔑 API 키 설정")
    gemini_api_key = st.text_input("Gemini API 키를 입력하세요.", type="password")
    st.markdown("[API 키 발급받기](https://aistudio.google.com/app/apikey)")
    st.info("입력하신 API 키는 서버에 저장되지 않으며, 새로고침 시 사라집니다.")

# 메인 화면 구성
st.title("👨‍💼 AI 리더십 특성 3줄 요약")
st.write("리더의 강점과 약점에 대한 의견을 입력하면, Gemini AI가 핵심 특성을 3줄로 요약합니다.")
st.write("")

# 입력 필드 (두 개의 컬럼으로 나누어 배치)
col1, col2 = st.columns(2)
with col1:
    strengths_input = st.text_area("👍 **강점** 또는 **칭찬할 점**을 상세히 입력하세요.", placeholder="예: 팀원들의 의견을 항상 경청하고 존중하며, 명확한 비전과 방향성을 제시해줍니다. 위기 상황에서도 침착하게 팀을 이끌어 신뢰를 줍니다.", height=200)

with col2:
    weaknesses_input = st.text_area("👎 **약점** 또는 **개선점**을 상세히 입력하세요.", placeholder="예: 때로는 업무 위임보다 직접 모든 것을 처리하려는 경향이 있어 팀원들의 성장을 저해할 수 있습니다. 결정된 사항에 대한 피드백이 조금 더 빠르면 좋겠습니다.", height=200)

# 요약 실행 버튼
if st.button("✨ AI로 요약하기", type="primary"):
    # 1. API 키가 있는지 확인
    if not gemini_api_key:
        st.error("❗ 사이드바에 Gemini API 키를 먼저 입력해주세요.")
    # 2. 강점/약점 내용이 모두 있는지 확인
    elif not strengths_input or not weaknesses_input:
        st.error("❗ 강점과 약점 내용을 모두 입력해야 분석할 수 있습니다.")
    # 3. 모든 조건 충족 시 AI 요약 실행
    else:
        with st.spinner('AI가 리더십 특성을 심층 분석 중입니다...'):
            summary_results = summarize_leadership_with_gemini(gemini_api_key, strengths_input, weaknesses_input)
            
            st.write("---")
            st.subheader("📋 리더십 특성 요약 결과")

            # 결과가 3줄일 경우 정상 출력
            if len(summary_results) == 3:
                st.info(f"**강점 기반 특성:** {summary_results[0]}")
                st.warning(f"**보완 필요 특성:** {summary_results[1]}")
                st.success(f"**종합 프로필:** {summary_results[2]}")
            # 오류 발생 시 오류 메시지 출력
            else:
                for line in summary_results:
                    st.error(line)
