# -*- coding: utf-8 -*-

# # app.py

# import streamlit as st
# import pandas as pd

# # 프로젝트 구성 요소 임포트
# from clients.llm_client import LLMClient
# from clients.backtester_client import BacktesterClient
# from agents.idea_agent import IdeaAgent
# from agents.factor_agent import FactorAgent
# from agents.eval_agent import EvalAgent
# from agents.advice_agent import InvestmentAdviceAgent
# from core.optimizer import HyperparameterOptimizer

# def main():
#     """
#     AlphaAgent 투자 조언 웹서비스의 메인 실행 함수.
#     """
#     st.set_page_config(page_title="AlphaAgent: LLM-Driven Alpha Mining", layout="wide")

#     # --- UI 구성 ---
#     st.title("🤖 AlphaAgent: LLM 기반 알파 탐색 및 투자 조언")
#     st.markdown("""
#     'AlphaAgent' 논문을 기반으로 구현된 이 서비스는 LLM 에이전트를 활용하여 새로운 투자 아이디어(알파 팩터)를 발굴하고,
#     백테스팅을 통해 검증한 뒤, 최종적으로 개인 투자자를 위한 조언 리포트를 생성합니다.
#     """)

#     st.sidebar.header("조정 패널")
#     initial_insight = st.sidebar.text_area(
#         "초기 투자 아이디어를 입력하세요",
#         height=150,
#         placeholder="예시: 거래량이 급증하는 소형주는 단기적으로 가격이 상승하는 경향이 있다."
#     )
#     num_rounds = st.sidebar.slider("탐색 반복 횟수 (Rounds)", 1, 5, 2)
#     start_button = st.sidebar.button("알파 탐색 시작", type="primary")

#     # --- 워크플로우 실행 ---
#     if start_button:
#         if not initial_insight.strip():
#             st.sidebar.error("초기 투자 아이디어를 입력해주세요.")
#             return

#         try:
#             # 1. 에이전트 및 클라이언트 초기화
#             with st.status("에이전트 및 클라이언트 초기화 중...", expanded=True) as status:
#                 llm_client = LLMClient()
#                 backtester_client = BacktesterClient()
#                 idea_agent = IdeaAgent(llm_client)
#                 factor_agent = FactorAgent(llm_client)
#                 eval_agent = EvalAgent(backtester_client)
#                 advice_agent = InvestmentAdviceAgent(llm_client)
#                 # optimizer = HyperparameterOptimizer() # 최적화는 현재 워크플로우에 미포함
#                 status.update(label="초기화 완료!", state="complete", expanded=False)

#         # except ValueError as e:
#         #     st.error(f"설정 오류: {e}")
#         #     st.stop()
#         # except Exception as e:
#         #     st.error(f"오류가 발생했습니다: {e}")
#         #     st.exception(e) # 모든 예외에 대해 스택 트레이스 표시
#         #     st.stop()
#             # 2. 메인 순환 로직 (Hypothesis -> Factor -> Evaluation)
#             current_hypothesis = {}
#             feedback_summary = {}
#             all_evaluated_factors = []

#             for i in range(num_rounds):
#                 round_num = i + 1
#                 st.subheader(f"🔄 Round {round_num}")

#                 with st.expander(f"Round {round_num}: 전체 과정 보기", expanded=True):
#                     # --- 가설 생성 단계 ---
#                     st.info(f"**단계 1: 가설 생성**")
#                     with st.spinner("LLM이 새로운 투자 가설을 생성 중입니다..."):
#                         if i == 0:
#                             current_hypothesis = idea_agent.generate_initial_hypothesis(initial_insight)
#                         else:
#                             current_hypothesis = idea_agent.refine_hypothesis(feedback_summary)

#                     if not current_hypothesis:
#                         st.error("가설 생성에 실패했습니다. 워크플로우를 중단합니다.")
#                         return
#                     st.write("✨ **생성된 가설:**")
#                     st.json(current_hypothesis)

#                     # --- 팩터 생성 단계 ---
#                     st.info(f"**단계 2: 팩터 변환**")
#                     with st.spinner("LLM이 가설을 바탕으로 알파 팩터 수식을 생성 중입니다..."):
#                         generated_factors = factor_agent.create_factors(current_hypothesis, num_factors=3)

#                     if not generated_factors:
#                         st.error("팩터 생성에 실패했습니다. 워크플로우를 중단합니다.")
#                         return
#                     st.write("📝 **생성된 팩터 후보:**")
#                     st.json(generated_factors)

#                     # --- 팩터 평가 단계 ---
#                     st.info(f"**단계 3: 팩터 평가**")
#                     with st.spinner(f"{len(generated_factors)}개 팩터에 대한 백테스팅을 실행합니다... (시간이 소요될 수 있습니다)"):
#                         evaluated_factors = eval_agent.evaluate_factors(generated_factors)

#                     st.write("📊 **팩터 평가 결과 (IC 기준 내림차순):**")
#                     st.dataframe(pd.DataFrame(evaluated_factors))
#                     all_evaluated_factors.extend(evaluated_factors)

#                     # --- 피드백 요약 ---
#                     feedback_summary = eval_agent.summarize_for_feedback(evaluated_factors)
#                     st.write("📈 **이번 라운드 요약:**")
#                     st.json(feedback_summary)

#             # 3. 최종 분석 및 투자 조언 생성
#             st.success("모든 알파 탐색 라운드가 완료되었습니다.")
#             st.header("🏆 최종 결과 분석")

#             if not all_evaluated_factors:
#                 st.warning("유효한 팩터가 발굴되지 않았습니다.")
#                 return

#             # 전체 라운드에서 IC가 가장 높은 팩터 선정
#             overall_best_factor = max([f for f in all_evaluated_factors if f.get('ic') is not None], key=lambda x: x['ic'])

#             st.write("전체 라운드에서 발굴된 최고의 알파 팩터는 다음과 같습니다:")
#             st.json(overall_best_factor)

#             # --- 투자 조언 리포트 생성 ---
#             st.header("📜 최종 투자 조언 리포트")
#             with st.spinner("LLM이 최종 리포트를 작성 중입니다..."):
#                 final_report = advice_agent.generate_advice_report(overall_best_factor)

#             st.markdown(final_report)

#         except Exception as e:
#             st.error(f"오류가 발생했습니다: {e}")

# if __name__ == "__main__":
#     main()

# app.py

import streamlit as st
import pandas as pd

# 프로젝트 구성 요소 임포트
from clients.llm_client import LLMClient
from clients.backtester_client import BacktesterClient
from agents.idea_agent import IdeaAgent
from agents.factor_agent import FactorAgent
from agents.eval_agent import EvalAgent
from agents.advice_agent import InvestmentAdviceAgent
# from core.optimizer import HyperparameterOptimizer # 현재 미사용

def initialize_workflow(initial_insight):
    """워크플로우 상태를 초기화하는 함수"""
    st.session_state.processing = True
    st.session_state.round_num = 0
    st.session_state.initial_insight = initial_insight
    st.session_state.current_hypothesis = {}
    st.session_state.feedback_summary = {}
    st.session_state.all_evaluated_factors = []

def main():
    """
    AlphaAgent 투자 조언 웹서비스의 메인 실행 함수.
    """
    st.set_page_config(page_title="AlphaAgent: LLM-Driven Alpha Mining", layout="wide")

    # --- UI 구성 ---
    st.title("🤖 AlphaAgent: LLM 기반 알파 탐색 및 투자 조언")
    st.markdown("""
    'AlphaAgent' 논문을 기반으로 구현된 이 서비스는 LLM 에이전트를 활용하여 새로운 투자 아이디어(알파 팩터)를 발굴하고,
    백테스팅을 통해 검증한 뒤, 최종적으로 개인 투자자를 위한 조언 리포트를 생성합니다.
    """)

    st.sidebar.header("조정 패널")
    initial_insight_input = st.sidebar.text_area(
        "초기 투자 아이디어를 입력하세요",
        height=150,
        placeholder="예시: 거래량이 급증하는 소형주는 단기적으로 가격이 상승하는 경향이 있다."
    )
    num_rounds = st.sidebar.slider("탐색 반복 횟수 (Rounds)", 1, 5, 2)
    
    # 두 개의 컬럼을 만들어 버튼을 나란히 배치
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_button = st.button("알파 탐색 시작", type="primary")
    with col2:
        reset_button = st.button("초기화")

    # --- 상태 관리 및 워크플로우 실행 ---

    # 시작 버튼 클릭 시 상태 초기화
    if start_button:
        if not initial_insight_input.strip():
            st.sidebar.error("초기 투자 아이디어를 입력해주세요.")
        else:
            initialize_workflow(initial_insight_input)
            st.rerun() # 초기화 후 즉시 재실행하여 루프 시작

    # 리셋 버튼 클릭 시 상태 초기화
    if reset_button:
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    # 'processing' 상태가 True일 때만 워크플로우 로직 실행
    if st.session_state.get('processing', False):
        
        # 1. 에이전트 및 클라이언트 초기화 (매 실행마다 초기화)
        # 참고: LLMClient나 BacktesterClient가 무거운 리소스를 로드한다면
        # @st.cache_resource를 사용하여 캐싱하는 것이 효율적입니다.
        llm_client = LLMClient()
        backtester_client = BacktesterClient()
        idea_agent = IdeaAgent(llm_client)
        factor_agent = FactorAgent(llm_client)
        eval_agent = EvalAgent(backtester_client)
        advice_agent = InvestmentAdviceAgent(llm_client)
        
        # 2. 메인 순환 로직: num_rounds에 도달할 때까지 한 라운드씩 실행
        if st.session_state.round_num < num_rounds:
            round_num_display = st.session_state.round_num + 1
            st.subheader(f"🔄 Round {round_num_display} / {num_rounds}")

            with st.expander(f"Round {round_num_display}: 전체 과정 보기", expanded=True):
                # --- 가설 생성 단계 ---
                st.info(f"**단계 1: 가설 생성**")
                with st.spinner("LLM이 새로운 투자 가설을 생성 중입니다..."):
                    if st.session_state.round_num == 0:
                        st.session_state.current_hypothesis = idea_agent.generate_initial_hypothesis(st.session_state.initial_insight)
                    else:
                        st.session_state.current_hypothesis = idea_agent.refine_hypothesis(st.session_state.feedback_summary)

                if not st.session_state.current_hypothesis:
                    st.error("가설 생성에 실패했습니다. 워크플로우를 중단합니다.")
                    st.session_state.processing = False # 처리 중단
                    return
                st.write("✨ **생성된 가설:**")
                st.json(st.session_state.current_hypothesis)

                # --- 팩터 생성 단계 ---
                st.info(f"**단계 2: 팩터 변환**")
                with st.spinner("LLM이 가설을 바탕으로 알파 팩터 수식을 생성 중입니다..."):
                    generated_factors = factor_agent.create_factors(st.session_state.current_hypothesis, num_factors=3)

                if not generated_factors:
                    st.error("팩터 생성에 실패했습니다. 워크플로우를 중단합니다.")
                    st.session_state.processing = False # 처리 중단
                    return
                st.write("📝 **생성된 팩터 후보:**")
                st.json(generated_factors)

                # --- 팩터 평가 단계 ---
                st.info(f"**단계 3: 팩터 평가**")
                with st.spinner(f"{len(generated_factors)}개 팩터에 대한 백테스팅을 실행합니다..."):
                    evaluated_factors = eval_agent.evaluate_factors(generated_factors)

                st.write("📊 **팩터 평가 결과 (IC 기준 내림차순):**")
                st.dataframe(pd.DataFrame(evaluated_factors))
                st.session_state.all_evaluated_factors.extend(evaluated_factors)

                # --- 피드백 요약 ---
                st.session_state.feedback_summary = eval_agent.summarize_for_feedback(evaluated_factors)
                st.write("📈 **이번 라운드 요약:**")
                st.json(st.session_state.feedback_summary)

            # 다음 라운드를 위해 라운드 카운터 증가 및 재실행
            st.session_state.round_num += 1
            st.rerun()

        # 3. 모든 라운드 완료 후 최종 분석 및 조언 생성
        else:
            st.success("모든 알파 탐색 라운드가 완료되었습니다.")
            st.header("🏆 최종 결과 분석")

            if not st.session_state.all_evaluated_factors:
                st.warning("유효한 팩터가 발굴되지 않았습니다.")
            else:
                overall_best_factor = max([f for f in st.session_state.all_evaluated_factors if f.get('ic') is not None], key=lambda x: x['ic'])
                st.write("전체 라운드에서 발굴된 최고의 알파 팩터는 다음과 같습니다:")
                st.json(overall_best_factor)

                st.header("📜 최종 투자 조언 리포트")
                with st.spinner("LLM이 최종 리포트를 작성 중입니다..."):
                    final_report = advice_agent.generate_advice_report(overall_best_factor)
                st.markdown(final_report)
            
            # 워크플로우 완료 후 처리 상태 종료
            st.session_state.processing = False

if __name__ == "__main__":
    main()
