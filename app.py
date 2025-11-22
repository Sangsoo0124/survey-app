import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. 설문 데이터 (파일 없이 바로 실행되도록 내장) ---
# 업로드해주신 파일 내용을 바탕으로 구성했습니다.
QUESTIONS = [
    # [cite_start]Thriving employees [cite: 1, 2, 3]
    {"요인": "Thriving employees", "항목": "업무의 질적 변화와 몰입(Engagement)", "질문": "AI 덕분에 단순 반복 업무가 줄어들어, 더 중요하고 창의적인 업무에 몰입할 수 있게 되었다."},
    {"요인": "Thriving employees", "항목": "주도적으로 성과를 창출(Self-efficacy)하는 느낌", "질문": "나는 AI를 파트너로 활용하여, 이전보다 더 높은 수준의 성과를 창출하고 있다고 느낀다."},
    {"요인": "Thriving employees", "항목": "업무에 대한 통제권(Autonomy)과 유능감", "질문": "나는 AI 도구를 내 업무 맥락에 맞게 자유자재로 응용하고 통제할 수 있는 역량을 갖추고 있다."},
    
    # [cite_start]Motivating culture [cite: 4, 5, 6, 7]
    {"요인": "Motivating culture", "항목": "팀 공유 문화", "질문": "우리 팀은 AI 활용 팁이나 프롬프트 노하우를 서로 적극적으로 공유하는 분위기다."},
    {"요인": "Motivating culture", "항목": "개방적 문화", "질문": "우리 조직은 AI로 산출된 결과물이나 데이터를 부서 간 장벽 없이 개방적으로 공유한다."},
    {"요인": "Motivating culture", "항목": "심리적 안전감이 있는 문화", "질문": "동료들은 AI를 활용하며 겪은 성공 사례뿐만 아니라, 실패 경험(시행착오)도 투명하게 공유한다."},
    {"요인": "Motivating culture", "항목": "도움을 주는 문화", "질문": "나는 동료가 AI 활용에 어려움을 겪을 때, 기꺼이 나의 지식과 시간을 내어 도와준다."},
    
    # [cite_start]Inclusive leadership [cite: 8, 9] 및 파일 내 중간 항목 포함
    {"요인": "Inclusive leadership", "항목": "포용하고 존중해 주는 리더", "질문": "리더는 내가 AI를 활용하는 과정에서 겪는 실수나 시행착오를 질책하기보다 배움의 기회로 존중해준다."},
    {"요인": "Inclusive leadership", "항목": "소통하고 변화를 관리하는 리더", "질문": "리더는 AI 도입으로 인한 업무 방식의 변화에 대해 구성원의 의견을 경청하고, 변화 과정을 세심하게 관리한다."},
    {"요인": "Inclusive leadership", "항목": "고용 불안을 비전 제시로 승화시키는 리더", "질문": "나의 리더는 AI가 내 일자리를 위협하는 것이 아니라, 내 역량을 강화하는 도구임을 명확히 인식시켜 준다."}
]

# 결과 저장 파일명
RESULT_FILE = "survey_results.csv"

# --- 2. UI 및 디자인 설정 ---
st.set_page_config(page_title="AI 조직문화 진단", page_icon="⚡", layout="centered")

def apply_edgy_style():
    st.markdown("""
    <style>
        /* 다크 모드 배경 및 기본 폰트 색상 */
        .stApp {
            background-color: #111111;
            color: #E0E0E0;
        }
        
        /* 타이틀 그라디언트 효과 */
        .main-title {
            background: linear-gradient(to right, #ff00cc, #333399);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.8rem;
            font-weight: 800;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        .sub-title {
            text-align: center;
            color: #888;
            margin-bottom: 2rem;
            font-size: 1rem;
        }

        /* 카테고리 헤더 스타일 */
        .category-header {
            margin-top: 40px;
            margin-bottom: 20px;
            padding-left: 15px;
            border-left: 4px solid #ff00cc;
            font-size: 1.5rem;
            font-weight: bold;
            color: #fff;
            background: linear-gradient(90deg, rgba(255,0,204,0.1) 0%, rgba(0,0,0,0) 100%);
        }

        /* 질문 카드 디자인 */
        .q-card {
            background-color: #1E1E1E;
            border: 1px solid #333;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            transition: transform 0.2s;
        }
        .q-card:hover {
            border-color: #ff00cc;
        }
        .q-item {
            font-size: 0.85rem;
            color: #ff00cc;
            margin-bottom: 8px;
            font-weight: 600;
            text-transform: uppercase;
        }
        .q-text {
            font-size: 1.1rem;
            line-height: 1.5;
            font-weight: 500;
        }

        /* 버튼 스타일 */
        .stButton > button {
            width: 100%;
            background: linear-gradient(45deg, #ff00cc, #333399);
            color: white;
            font-weight: bold;
            border: none;
            padding: 15px;
            border-radius: 8px;
            font-size: 1.1rem;
        }
        .stButton > button:hover {
            opacity: 0.9;
            transform: scale(1.01);
        }
        
        /* 라디오 버튼 커스텀 */
        div[role="radiogroup"] {
            display: flex;
            justify-content: space-between;
            background: #111;
            padding: 10px;
            border-radius: 8px;
            margin-top: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

apply_edgy_style()

# --- 3. 메인 앱 로직 ---
def main():
    # 사이드바 (관리자 메뉴 숨김 처리 느낌)
    with st.sidebar:
        st.header("⚙️ Menu")
        mode = st.radio("모드 선택", ["설문 참여", "관리자 모드"])
        st.info("모바일/PC 환경 모두 최적화되어 있습니다.")

    # [PAGE 1] 설문 참여 화면
    if mode == "설문 참여":
        st.markdown('<div class="main-title">AI CULTURE<br>SURVEY</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-title">조직의 AI 수용성과 문화를 진단합니다.</div>', unsafe_allow_html=True)

        with st.form("survey_form"):
            responses = {}
            
            # 데이터를 요인별로 그룹화하여 출력
            df = pd.DataFrame(QUESTIONS)
            grouped = df.groupby("요인")
            
            # 출력 순서 지정
            order = ["Motivating culture", "Inclusive leadership", "Thriving employees"]
            
            for factor in order:
                if factor in grouped.groups:
                    st.markdown(f'<div class="category-header">{factor}</div>', unsafe_allow_html=True)
                    group_df = grouped.get_group(factor)
                    
                    for _, row in group_df.iterrows():
                        q_key = f"{factor}_{row['항목']}"
                        
                        st.markdown(f"""
                        <div class="q-card">
                            <div class="q-item">{row['항목']}</div>
                            <div class="q-text">{row['질문']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # 5점 척도 (모바일에서도 찍기 편하도록 설정)
                        val = st.radio(
                            "응답 선택",
                            options=[1, 2, 3, 4, 5],
                            format_func=lambda x: f"{x}",
                            key=q_key,
                            horizontal=True,
                            label_visibility="collapsed"
                        )
                        # 캡션 추가 (1:전혀 아님 ~ 5:매우 그렇다)
                        st.caption("1 (전혀 아님) ↔ 5 (매우 그렇다)")
                        responses[q_key] = val
                        st.write("") # 여백

            st.markdown("---")
            submitted = st.form_submit_button("응답 제출하기")

            if submitted:
                # 타임스탬프 추가
                final_data = responses.copy()
                final_data["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # 데이터프레임 변환
                new_df = pd.DataFrame([final_data])
                
                # CSV 저장 (없으면 생성, 있으면 이어쓰기)
                if not os.path.exists(RESULT_FILE):
                    new_df.to_csv(RESULT_FILE, index=False, encoding="utf-8-sig")
                else:
                    new_df.to_csv(RESULT_FILE, mode='a', header=False, index=False, encoding="utf-8-sig")
                
                st.success("✅ 제출이 완료되었습니다. 감사합니다!")
                st.balloons()

    # [PAGE 2] 관리자 화면
    elif mode == "관리자 모드":
        st.markdown('<div class="main-title">ADMIN DASHBOARD</div>', unsafe_allow_html=True)
        
        pwd = st.text_input("비밀번호를 입력하세요", type="password")
        
        if pwd == "1234":  # 초기 비밀번호
            if os.path.exists(RESULT_FILE):
                data = pd.read_csv(RESULT_FILE)
                
                # 1. 기본 현황
                st.metric(label="총 응답자 수", value=f"{len(data)}명")
                
                # 2. 데이터 미리보기
                st.subheader("📋 응답 데이터 확인")
                st.dataframe(data, use_container_width=True)
                
                # 3. CSV 다운로드
                csv = data.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="📥 데이터 다운로드 (CSV)",
                    data=csv,
                    file_name="survey_results.csv",
                    mime="text/csv"
                )
            else:
                st.warning("아직 제출된 설문 데이터가 없습니다.")
        elif pwd:
            st.error("비밀번호가 틀렸습니다.")

if __name__ == "__main__":
    main()
