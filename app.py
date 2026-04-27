import streamlit as st
import time

st.set_page_config(page_title="전공 상식 퀴즈 앱")

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
            "question": "Python에서 리스트를 만드는 기호는?",
            "choices": ["()", "[]", "{}", "<>"],
            "answer": "[]"
        },
        {
            "question": "Streamlit에서 화면에 제목을 출력하는 함수는?",
            "choices": ["st.title()", "st.print()", "st.header_title()", "st.show()"],
            "answer": "st.title()"
        },
        {
            "question": "GitHub에서 프로젝트를 저장하는 공간을 무엇이라고 하는가?",
            "choices": ["Repository", "Folder", "Cloud", "Commit"],
            "answer": "Repository"
        },
        {
            "question": "Streamlit에서 버튼을 만드는 함수는?",
            "choices": ["st.input()", "st.button()", "st.click()", "st.submit()"],
            "answer": "st.button()"
        },
        {
            "question": "Streamlit에서 데이터 캐싱에 사용하는 데코레이터는?",
            "choices": ["@st.cache_data", "@st.save_data", "@st.memory", "@st.data_save"],
            "answer": "@st.cache_data"
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
st.title("전공 상식 퀴즈 앱")

st.info(f"학번: {STUDENT_ID} / 이름: {STUDENT_NAME}")

st.write("""
이 앱은 Python과 Streamlit을 활용하여 만든 전공 상식 퀴즈 앱입니다.  
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

    st.subheader("전공 상식 퀴즈")

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
            st.success("완벽합니다! 전공 상식이 매우 뛰어납니다.")
        elif score >= total // 2:
            st.info("좋습니다! 기본 개념을 잘 알고 있습니다.")
        else:
            st.warning("조금 더 복습이 필요합니다.")

    st.divider()

    with st.expander("캐싱 기능 설명 보기"):
        st.write("""
        이 앱에서는 `@st.cache_data`를 사용했습니다.

        `load_quiz_data()` 함수는 퀴즈 문제 데이터를 불러오는 함수입니다.
        Streamlit은 버튼을 누르거나 입력값이 바뀌면 앱 코드를 다시 실행하는데,
        캐싱을 사용하면 같은 퀴즈 데이터를 매번 새로 만들지 않고
        저장된 데이터를 다시 사용합니다.

        따라서 중복 실행을 줄이고 앱 실행 속도를 높일 수 있습니다.
        """)
