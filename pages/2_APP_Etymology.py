import streamlit as st
import pandas as pd
import random

# ---------- Page Config ----------
st.set_page_config(
    page_title="APP: Etymology",
    page_icon="🌱",
    layout="wide"
)

# ---------- Sidebar Font ----------
st.markdown("""
<style>

/* Sidebar menu text */
section[data-testid="stSidebar"] a,
section[data-testid="stSidebar"] a span,
section[data-testid="stSidebar"] a p {
    font-size: 18px !important;
    font-weight: 500 !important;
}

</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<h1 style='text-align:center; font-size:36px; margin-bottom:5px;'>
🌱 APP Etymology
</h1>

<p style='text-align:center; font-size:18px; color:#555;'>
어원 · 접두사 · 접미사 · 어근 학습 앱<br>
단어의 뿌리와 의미 관계를 학습하는 앱

</p>
""", unsafe_allow_html=True)

st.title("🌱 APP: Etymology")
st.caption("Daily Test · Review Test · Progress Test")

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
            "Select Test",
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
                "Select Day",
                day_list,
                key=f"day_{i}_{test_type}"
            )
            test_df = test_df[test_df["day"] == selected_day]

        max_questions = len(test_df)

        if max_questions == 0:
            st.warning("No words are available for this test. Please check the selected grade, day, or test type.")
            continue

        question_count = st.slider(
            "Number of Questions",
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

                st.write(f"**Prefix / Root / Suffix:** {row['prefix']}")

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
