import streamlit as st
from konlpy.tag import Okt
from collections import Counter

# --- 핵심 로직 함수 ---
def summarize_leadership(strengths_text, weaknesses_text):
    """리더십 강점/약점 텍스트를 분석하여 3줄로 요약하는 함수"""
    okt = Okt()

    # 1. 강점 분석: 2글자 이상의 명사만 추출
    strength_nouns = [n for n in okt.nouns(strengths_text) if len(n) > 1]
    strength_counts = Counter(strength_nouns)
    # 가장 빈도가 높은 키워드 2개 추출
    top_strengths = [n for n, c in strength_counts.most_common(2)]

    # 2. 약점 분석: 2글자 이상의 명사만 추출
    weakness_nouns = [n for n in okt.nouns(weaknesses_text) if len(n) > 1]
    weakness_counts = Counter(weakness_nouns)
    # 가장 빈도가 높은 키워드 1개 추출
    top_weakness = ""
    if weakness_counts:
        top_weakness = weakness_counts.most_common(1)[0][0]

    # --- 요약 문장 생성 ---
    # 예외 처리: 분석된 키워드가 없는 경우 기본값 설정
    if not top_strengths:
        top_strengths = ["뛰어난", "리더십"] # 기본 강점 키워드
    elif len(top_strengths) == 1:
        top_strengths.append("소통능력") # 키워드가 하나일 경우 기본값 추가

    if not top_weakness:
        top_weakness = "피드백" # 기본 약점 키워드

    # 각 문장은 12단어 이하, ~임/~함 형식으로 생성
    summary_line1 = f"뛰어난 {top_strengths[0]} 및 {top_strengths[1]} 역량을 보유함."
    summary_line2 = f"다만 {top_weakness} 역량은 일부 보완이 필요함."
    summary_line3 = f"종합적으로 {top_strengths[0]} 기반의 소통형 리더임."

    return [summary_line1, summary_line2, summary_line3]

# --- Streamlit UI 구성 ---

# 페이지 기본 설정
st.set_page_config(page_title="리더십 특성 요약기", page_icon="👨‍💼")

# 제목 및 설명
st.title("👨‍💼 리더십 특성 3줄 요약")
st.write("리더의 강점과 약점에 대한 의견을 입력하면, AI가 핵심 특성을 3줄로 요약합니다.")
st.write("") # 여백

# 입력 필드 (두 개의 컬럼으로 나누어 배치)
col1, col2 = st.columns(2)
with col1:
    strengths_input = st.text_area("👍 **강점** 또는 **칭찬할 점**을 입력하세요.", placeholder="예: 항상 팀원들의 의견을 경청하고 명확한 방향성을 제시해줍니다. 소통 능력이 탁월합니다.", height=200)

with col2:
    weaknesses_input = st.text_area("👎 **약점** 또는 **개선점**을 입력하세요.", placeholder="예: 가끔 업무 위임보다는 직접 처리하려는 경향이 있습니다. 빠른 피드백이 조금 아쉽습니다.", height=200)

# 요약 실행 버튼
if st.button("✨ AI로 요약하기"):
    if strengths_input and weaknesses_input:
        # 스피너(로딩 표시)와 함께 분석 함수 실행
        with st.spinner('AI가 리더십 특성을 분석하고 있습니다... 잠시만 기다려주세요.'):
            summary_results = summarize_leadership(strengths_input, weaknesses_input)

            st.write("---")
            st.subheader("📋 리더십 특성 요약 결과")

            # 결과 출력
            st.info(f"**강점 기반 특성:** {summary_results[0]}")
            st.warning(f"**보완 필요 특성:** {summary_results[1]}")
            st.success(f"**종합 프로필:** {summary_results[2]}")
    else:
        # 입력값이 부족할 경우 에러 메시지 표시
        st.error("❗ 강점과 약점 내용을 모두 입력해야 분석할 수 있습니다.")
