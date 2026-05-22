import streamlit as st
import pandas as pd
import random
from pathlib import Path

# ==========================================
# Grade 1 Collocations App
# Required CSV:
# grade1_common1_common2_collocations.csv
# ==========================================

st.set_page_config(
    page_title="Grade 1 Collocations",
    page_icon="📘",
    layout="wide"
)

# ---------- Style ----------
st.markdown("""
<style>
.main-title {
    font-size: 34px;
    font-weight: 800;
    color: #1565c0;
}

.word-card {
    background-color: #f4f9ff;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #cfe3ff;
    margin-bottom: 14px;
}

.collocation {
    font-size: 28px;
    font-weight: 800;
    color: #0d47a1;
}

.meaning {
    font-size: 19px;
    margin-top: 8px;
}

.example {
    font-size: 16px;
    margin-top: 10px;
    color: #444;
}
</style>
""", unsafe_allow_html=True)

# ---------- Load Data ----------
@st.cache_data
def load_data():

    filename = "grade1_common1_common2_collocations.csv"

    possible_files = [
        filename,
        f"data/{filename}"
    ]

    file_path = None

    for f in possible_files:
        if Path(f).exists():
            file_path = f
            break

    if file_path is None:
        st.error("CSV 파일을 찾을 수 없습니다.")
        st.stop()

    df = pd.read_csv(file_path)

    required_cols = [
        "source_order",
        "section",
        "lesson",
        "collocation",
        "meaning",
        "example_sentence"
    ]

    missing = [c for c in required_cols if c not in df.columns]

    if missing:
        st.error(f"빠진 컬럼: {missing}")
        st.stop()

    df = df.fillna("")
    return df


df = load_data()

# ---------- Header ----------
st.markdown(
    '<div class="main-title">📘 Grade 1 Collocations</div>',
    unsafe_allow_html=True
)

st.write("공통영어1 · 공통영어2 연어 학습 앱")

st.divider()

# ---------- Sidebar ----------
mode = st.sidebar.radio(
    "메뉴 선택",
    [
        "1. Learn",
        "2. Meaning Test",
        "3. Fill-in Test",
        "4. Review Wrong Answers"
    ]
)

section_options = ["전체"] + list(df["section"].unique())

selected_section = st.sidebar.selectbox(
    "교재 선택",
    section_options
)

if selected_section != "전체":
    filtered_df = df[df["section"] == selected_section].copy()
else:
    filtered_df = df.copy()

# ---------- Session ----------
if "wrong_items" not in st.session_state:
    st.session_state.wrong_items = []

# ==========================================
# 1. Learn
# ==========================================
if mode == "1. Learn":

    st.subheader("📖 Learn Collocations")

    for _, row in filtered_df.iterrows():

        st.markdown(f"""
        <div class="word-card">
            <div class="collocation">
                {row['collocation']}
            </div>

            <div class="meaning">
                뜻: {row['korean_meaning']}
            </div>

            <div class="example">
                예문: {row['example_sentence']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 2. Meaning Test
# ==========================================
elif mode == "2. Meaning Test":

    st.subheader("📝 Meaning Test")

    quiz_df = filtered_df.sample(min(10, len(filtered_df)))

    answers = []

    for i, (_, row) in enumerate(quiz_df.iterrows(), start=1):

        correct = row["meaning"]

        wrongs = df[
            df["meaning"] != correct
        ]["meaning"].sample(3).tolist()

        options = wrongs + [correct]

        random.shuffle(options)

        answer = st.radio(
            f"Q{i}. {row['collocation']}",
            options,
            key=f"m_{i}"
        )

        answers.append((row, answer, correct))

    if st.button("제출하기"):

        score = 0

        for row, answer, correct in answers:

            if answer == correct:
                score += 1
                st.success(f"✅ {row['collocation']}")
            else:
                st.error(
                    f"❌ {row['collocation']} → 정답: {correct}"
                )

                st.session_state.wrong_items.append(row)

        st.markdown(f"## 점수: {score} / {len(answers)}")

# ==========================================
# 3. Fill-in Test
# ==========================================
elif mode == "3. Fill-in Test":

    st.subheader("✏️ Fill-in Test")

    quiz_df = filtered_df.sample(min(10, len(filtered_df)))

    user_answers = []

    for i, (_, row) in enumerate(quiz_df.iterrows(), start=1):

        collocation = row["collocation"]

        words = collocation.split()

        if len(words) >= 2:

            blank = "_____ " + " ".join(words[1:])

        else:
            blank = "_____"

        st.write(f"Q{i}. {blank}")

        answer = st.text_input(
            "빈칸에 들어갈 단어 입력",
            key=f"f_{i}"
        )

        user_answers.append((row, answer))

    if st.button("채점하기"):

        score = 0

        for row, answer in user_answers:

            correct = row["collocation"].split()[0]

            if answer.strip().lower() == correct.lower():

                score += 1
                st.success(f"✅ {row['collocation']}")

            else:

                st.error(
                    f"❌ 정답: {row['collocation']}"
                )

                st.session_state.wrong_items.append(row)

        st.markdown(f"## 점수: {score} / {len(user_answers)}")

# ==========================================
# 4. Wrong Answers
# ==========================================
else:

    st.subheader("🔁 Review Wrong Answers")

    if not st.session_state.wrong_items:

        st.info("아직 오답이 없습니다.")

    else:

        for row in st.session_state.wrong_items:

            st.markdown(f"""
            <div class="word-card">

                <div class="collocation">
                    {row['collocation']}
                </div>

                <div class="meaning">
                    뜻: {row['korean_meaning']}
                </div>

                <div class="example">
                    예문: {row['example_sentence']}
                </div>

            </div>
            """, unsafe_allow_html=True)

        if st.button("오답 초기화"):

            st.session_state.wrong_items = []

            st.rerun()
