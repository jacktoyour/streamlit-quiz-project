import streamlit as st
import time

st.set_page_config(page_title="자기 소개 퀴즈 앱")

# =========================
# 학생 정보 / 로그인 정보
# =========================
STUDENT_ID = "2025404063"
STUDENT_NAME = "진형민"

USER_ID = "2025404063"
USER_PW = "1234"


# =========================
# 캐싱 기능
# =========================
@st.cache_data
def load_quiz_data():
    """
    퀴즈 데이터를 불러오는 함수입니다.
    같은 데이터를 반복해서 새로 만들지 않도록 캐싱을 적용했습니다.
    """
    time.sleep(1)

    questions = [
        {
            "question": "진형민이 제일 좋아하는 음식은?",
            "choices": ["치킨", "라면", "부대찌개", "피자"],
            "answer": "부대찌개"
        },
        {
            "question": "진형민이 제일 좋아하는 노래는",
            "choices": ["wonderwall", "she's electric", "creep", "champgne supernova"],
            "answer": "she's electric"
        },
        {
            "question": "진형민이 속해있는 과는",
            "choices": ["정보융합학과", "전자공학과", "소프트웨어융합과", "로봇학과"],
            "answer": "정보융합학과"
        },
        {
            "question": "진형민이 제일 좋아하는색은",
            "choices": ["초록색", "노랑색", "파란색", "빨간색"],
            "answer": "빨간색"
        },
        {
            "question": "진형민의 생일은",
            "choices": ["5월2일", "6월 12일", "9월 26일", "10월 30일"],
            "answer": "10월 30일"
        }
    ]

    return questions


# =========================
# 세션 상태 초기화
# =========================
if "login" not in st.session_state:
    st.session_state.login = False

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "score" not in st.session_state:
    st.session_state.score = 0


# =========================
# 첫 화면
# =========================
st.title("진형민 소개 퀴즈 앱")

st.info(f"학번: {STUDENT_ID} / 이름: {STUDENT_NAME}")

st.write("""
이 앱은 Python과 Streamlit을 활용하여 만든 형민 소개 퀴즈 앱입니다.  
로그인 후 퀴즈를 풀고 점수를 확인할 수 있습니다.
""")

st.divider()


# =========================
# 로그인 화면
# =========================
if not st.session_state.login:
    st.subheader("로그인")

    input_id = st.text_input("아이디")
    input_pw = st.text_input("비밀번호", type="password")

    if st.button("로그인"):
        if input_id == USER_ID and input_pw == USER_PW:
            st.session_state.login = True
            st.session_state.submitted = False
            st.session_state.score = 0
            st.success("로그인 성공!")
            st.rerun()
        else:
            st.error("아이디 또는 비밀번호가 틀렸습니다.")

    st.caption("테스트용 아이디: 2025404063 / 비밀번호: 1234")


# =========================
# 퀴즈 화면
# =========================
else:
    st.success("로그인 상태입니다.")

    if st.button("로그아웃"):
        st.session_state.login = False
        st.session_state.submitted = False
        st.session_state.score = 0
        st.rerun()

    st.divider()

    st.subheader("자기 소개 퀴즈")

    quiz_data = load_quiz_data()

    st.write("아래 문제를 풀고 제출 버튼을 눌러 결과를 확인하세요.")

    user_answers = []

    with st.form("quiz_form"):
        for i, q in enumerate(quiz_data):
            st.write(f"**문제 {i + 1}. {q['question']}**")

            answer = st.radio(
                "정답을 선택하세요.",
                q["choices"],
                key=f"question_{i}"
            )

            user_answers.append(answer)
            st.write("")

        submitted = st.form_submit_button("제출하기")

    if submitted:
        score = 0

        for i, q in enumerate(quiz_data):
            if user_answers[i] == q["answer"]:
                score += 1

        st.session_state.score = score
        st.session_state.submitted = True

    if st.session_state.submitted:
        st.divider()
        st.subheader("결과")

        score = st.session_state.score
        total = len(quiz_data)

        st.write(f"총 {total}문제 중 **{score}문제**를 맞혔습니다.")
        st.progress(score / total)

        if score == total:
            st.balloons()
            st.success("완벽합니다! 형민 상식이 매우 뛰어납니다.")
        elif score >= total // 2:
            st.info("좋습니다! 형민이를 잘 알고 있습니다.")
        else:
            st.warning("조금 더 친해지려는 노력이 필요합니다.")

