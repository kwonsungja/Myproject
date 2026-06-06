import streamlit as st
import pandas as pd
import random

# ---------- Page Config ----------
st.set_page_config(
    page_title="APP: Etymology",
    page_icon="🌱",
    layout="wide"
)

# ---------- Global Font Style ----------
st.markdown("""
<style>

/* Sidebar menu text */
section[data-testid="stSidebar"] a,
section[data-testid="stSidebar"] a span,
section[data-testid="stSidebar"] a p {
    font-size: 18px !important;
    font-weight: 500 !important;
}

/* Grade 1 / Grade 2 / Grade 3 탭 글자 */
button[data-baseweb="tab"] p {
    font-size: 26px !important;
    font-weight: 700 !important;
}

/* selectbox / slider 라벨 */
.stSelectbox label,
.stSlider label {
    font-size: 26px !important;
    font-weight: 700 !important;
}

/* selectbox 내부 글자: 너무 크지 않게 조정 */
div[data-baseweb="select"] > div {
    font-size: 20px !important;
    min-height: 50px !important;
}

/* selectbox 선택된 값 텍스트 */
div[data-baseweb="select"] span {
    font-size: 20px !important;
}

/* slider 숫자 */
.stSlider div {
    font-size: 18px !important;
}

/* 버튼 */
.stButton button {
    font-size: 22px !important;
    font-weight: 600 !important;
    padding: 10px 24px !important;
    border-radius: 12px !important;
}

/* 추가 ↓↓↓ */

/* Select Test / Select Day / Number of Questions */
div[data-testid="stSelectbox"] label p,
div[data-testid="stSlider"] label p {
    font-size: 22px !important;
    font-weight: 700 !important;
}

/* Start Test 버튼 글자 */
div[data-testid="stButton"] button p {
    font-size: 20px !important;
    font-weight: 700 !important;
}

/* 전체 기본 글자 */
html, body, [class*="css"] {
    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<h1 style='text-align:center; font-size:36px; margin-bottom:10px;'>
🌱 APP Etymology (Grade 1)
</h1>

<div style='text-align:center; font-size:18px; color:#555; line-height:1.8;'>

Learn prefixes, suffixes, and roots through meaning, word connections, and review.
<br>
접두사 · 접미사 · 어근을 의미 연결과 반복 학습으로 익히는 고등학교 1학년용 어원 학습 앱입니다.

</div>
""", unsafe_allow_html=True)

st.divider()

@st.cache_data
def load_data():
    return pd.read_csv("data/etymology_final.csv")

df = load_data()

test_map = {
    "접두사 Daily Test": (1, 10),
    "Review Test 1 (Day 1-5)": (1, 5),
    "Review Test 2 (Day 6-10)": (6, 10),
    "Progress Test 1 (Day 1-10)": (1, 10),

    "접미사 Daily Test": (11, 15),
    "Review Test 3 (Day 11-15)": (11, 15),

    "어근 Daily Test 1": (16, 20),
    "Review Test 4 (Day 16-20)": (16, 20),
    "Progress Test 2 (Day 1-20)": (1, 20),

    "Review Test 5 (Day 21-25)": (21, 25),
    "Review Test 6 (Day 26-30)": (26, 30),
    "Progress Test 3 (Day 1-30)": (1, 30),

    "Review Test 7 (Day 31-35)": (31, 35),
    "Review Test 8 (Day 36-40)": (36, 40),
    "Progress Test 4 (Day 1-40)": (1, 40),

    "Review Test 9 (Day 41-45)": (41, 45),
    "Review Test 10 (Day 46-50)": (46, 50),
    "Progress Test 5 (Day 1-50)": (1, 50),
}

grade_tabs = st.tabs(["Grade 1", "Grade 2", "Grade 3"])

for i, tab in enumerate(grade_tabs, start=1):
    with tab:
        st.subheader(f"Grade {i} Etymology Test")

        grade_df = df[df["grade"].astype(str) == str(i)]
     
        if i == 1:
            available_tests = [
                "접두사 Daily Test",
                "Review Test 1 (Day 1-5)",
                "Review Test 2 (Day 6-10)",
                "Progress Test 1 (Day 1-10)",
                "접미사 Daily Test",
                "Review Test 3 (Day 11-15)"
            ]

        elif i == 2:
            available_tests = [
                "어근 Daily Test 1",
                "Review Test 4 (Day 16-20)",
                "Progress Test 2 (Day 1-20)",
                "Review Test 5 (Day 21-25)",
                "Review Test 6 (Day 26-30)",
                "Progress Test 3 (Day 1-30)"
            ]

        else:
            available_tests = [
                "Review Test 7 (Day 31-35)",
                "Review Test 8 (Day 36-40)",
                "Progress Test 4 (Day 1-40)",
                "Review Test 9 (Day 41-45)",
                "Review Test 10 (Day 46-50)",
                "Progress Test 5 (Day 1-50)"
            ]

        test_type = st.selectbox(
            "📝 Select Test",
            available_tests,
            key=f"test_type_{i}"
        )
        start_day, end_day = test_map[test_type]
        test_df = grade_df[
            (grade_df["day"] >= start_day) &
            (grade_df["day"] <= end_day)
        ]

        if "Daily Test" in test_type:
            day_list = sorted(test_df["day"].unique())
            selected_day = st.selectbox(
                "📅 Select Day",
                day_list,
                key=f"day_{i}_{test_type}"
            )
            test_df = test_df[test_df["day"] == selected_day]

        max_questions = len(test_df)

        if max_questions == 0:
            st.warning("No words are available for this test. Please check the selected grade, day, or test type.")
            continue

        question_count = st.slider(
            "❓ Number of Questions",
            min_value=1,
            max_value=min(30, max_questions),
            value=min(10, max_questions),
            key=f"q_count_{i}_{test_type}"
        )

        if st.button("Start Test", key=f"start_{i}_{test_type}"):
            st.session_state[f"quiz_{i}"] = test_df.sample(
                question_count,
                random_state=random.randint(1, 10000)
            ).reset_index(drop=True)
            st.session_state[f"answers_{i}"] = {}

        if f"quiz_{i}" in st.session_state:
            quiz_df = st.session_state[f"quiz_{i}"]

            st.markdown("---")
            st.markdown("## 📝 Test Questions")

for idx, row in quiz_df.iterrows():
    st.markdown(f"### Q{idx+1}. {row['word']}")

    etymology_note = str(row.get("etymology_note", ""))

    if etymology_note != "nan" and etymology_note.strip() != "":
        st.markdown(f"""
        <div style="
            font-size:20px;
            line-height:1.8;
            background-color:#f8fbff;
            padding:12px 18px;
            border-radius:10px;
            border-left:5px solid #4a90e2;
            margin:12px 0 18px 0;
        ">
            <b>Etymology:</b> {etymology_note}
        </div>
        """, unsafe_allow_html=True)
    example_sentence = str(row['example_sentence'])
                example_sentence = str(row['example_sentence'])
                target_word = str(row['word'])

                if example_sentence == "nan":
                    example_sentence = ""

                highlighted_sentence = example_sentence.replace(
                    target_word,
                    f"**{target_word}**"
                )

                st.markdown(f"**Example:** {highlighted_sentence}")

                user_answer = st.text_input(
                    "Translate the sentence into Korean",
                    key=f"answer_{i}_{idx}"
                )

                st.caption("Focus on the highlighted word when translating.")

                st.session_state[f"answers_{i}"][idx] = user_answer

            if st.button("Submit Answers", key=f"submit_{i}_{test_type}"):
                score = 0

                st.markdown("---")
                st.markdown("## ✅ Result")

                for idx, row in quiz_df.iterrows():
                    user_answer = st.session_state[f"answers_{i}"].get(idx, "")
                    correct_answer = str(row["example_korean"])

                    if user_answer.strip() in correct_answer:
                        score += 1
                        st.success(f"Q{idx+1}. Correct! / {row['word']} = {correct_answer}")
                    else:
                        st.error(f"Q{idx+1}. Incorrect")
                        st.write(f"Your answer: {user_answer}")
                        st.write(f"Correct answer: {correct_answer}")

                st.markdown(f"## Final Score: {score} / {len(quiz_df)}")

                result_df = quiz_df[[
                    "day", "prefix", "meaning", "word", "word_meaning",
                    "example_sentence", "example_korean", "etymology_note"
                ]]

                st.markdown("### Review Table")
                st.dataframe(result_df, use_container_width=True)
