import streamlit as st
import pandas as pd
import random
from pathlib import Path

# ==========================================
# Grade 1 Collocations App
# ==========================================

# ---------- Page Config ----------
st.set_page_config(
    page_title="Grade 1 Collocations",
    page_icon="📘",
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
📘 APP Collocations
</h1>

<p style='text-align:center; font-size:18px; color:#555;'>
공통영어1 · 공통영어2 연어 학습 앱<br>
자주 함께 쓰이는 자연스러운 단어 표현을 학습하는 앱
</p>
""", unsafe_allow_html=True)

# ---------- Style ----------
st.markdown("""
<style>

.main-title {
    font-size: 40px;
    font-weight: 800;
    color: #1565c0;
}

.word-card {
    background-color: #f4f9ff;
    padding: 24px;
    border-radius: 18px;
    border: 1px solid #cfe3ff;
    margin-bottom: 18px;
}

.collocation {
    font-size: 34px;
    font-weight: 800;
    color: #0d47a1;
}

.meaning {
    font-size: 26px;
    margin-top: 12px;
}

.example {
    font-size: 22px;
    margin-top: 14px;
    color: #444;
}

.question-text {
    font-size: 32px !important;
    font-weight: 700 !important;
    margin-top: 24px;
    margin-bottom: 10px;
}

/* 선택지 글자 */
div[role="radiogroup"] label {
    font-size: 28px !important;
    font-weight: 500 !important;
}

/* 라디오 버튼 간격 */
div[role="radiogroup"] > label {
    margin-bottom: 12px !important;
}

/* 슬라이더 숫자 */
.stSlider label {
    font-size: 22px !important;
}

/* selectbox */
.stSelectbox label {
    font-size: 24px !important;
    font-weight: 600 !important;
}

/* radio menu */
.stRadio label {
    font-size: 24px !important;
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
        "meaning_ko",
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

# ---------- Learning Settings ----------

st.header("⚙️ 학습 설정")

mode = st.radio(
    "메뉴 선택",
    [
        "1. Learn",
        "2. Meaning Test",
        "3. Fill-in Test",
        "4. Review Wrong Answers"
    ],
    index=0
)

section_options = ["전체"] + list(df["section"].dropna().unique())

selected_section = st.selectbox(
    "학습 자료 선택",
    section_options
)

if selected_section != "전체":
    filtered_df = df[df["section"] == selected_section].copy()
else:
    filtered_df = df.copy()

lesson_options = ["전체"] + list(filtered_df["lesson"].dropna().unique())

selected_lesson = st.selectbox(
    "Lesson 선택",
    lesson_options
)

if selected_lesson != "전체":
    filtered_df = filtered_df[
        filtered_df["lesson"] == selected_lesson
    ].copy()

items_per_page = st.slider(
    "한 번에 볼 표현 수",
    5,
    20,
    10
)

# ---------- Session ----------
if "wrong_items" not in st.session_state:
    st.session_state.wrong_items = []

# ==========================================
# 1. Learn
# ==========================================
if mode == "1. Learn":

    st.subheader("📖 Learn Collocations")

    for _, row in filtered_df.iterrows():

        st.markdown(
            f"""
<div style='background-color:#fff7ef; padding:28px; border-radius:18px; border:1px solid #ffd2b3; margin-bottom:24px;'>
<div style='color:#e85d04; font-size:24px; font-weight:800; margin-bottom:18px;'>{row['collocation']}</div>
<div style='font-size:18px; margin-bottom:12px;'><b>뜻:</b> {row['meaning_ko']}</div>
<div style='font-size:17px;'><b>예문:</b> {row['example_sentence']}</div>
</div>
            """,
            unsafe_allow_html=True
        )
        
elif mode == "2. Meaning Test":

    st.subheader("📝 Meaning Test")

    if "meaning_quiz_items" not in st.session_state:
        st.session_state.meaning_quiz_items = []

    if st.button("새 Meaning Test 시작"):
        quiz_df = filtered_df.sample(min(items_per_page, len(filtered_df)))

        quiz_items = []

        for _, row in quiz_df.iterrows():
            correct = row["meaning_ko"]

            wrongs = df[df["meaning_ko"] != correct]["meaning_ko"].dropna().unique().tolist()
            wrongs = random.sample(wrongs, min(3, len(wrongs)))

            options = wrongs + [correct]
            random.shuffle(options)

            item = row.to_dict()
            item["options"] = options
            quiz_items.append(item)

        st.session_state.meaning_quiz_items = quiz_items

    if not st.session_state.meaning_quiz_items:
        st.warning("먼저 '새 Meaning Test 시작' 버튼을 눌러 주세요.")
        st.stop()

    answers = []
for i, item in enumerate(st.session_state.meaning_quiz_items, start=1):

    correct = item["meaning_ko"]
    options = item["options"]

    st.markdown(
        f"<div class='question-text'>Q{i}. {item['collocation']}</div>",
        unsafe_allow_html=True
    )

    answer = st.radio(
        "",
        options,
        index=None,
        key=f"m_{i}"
    )

    answers.append((item, answer, correct))
    "",
    options,
    index=None,
    key=f"m_{i}"
)

    answers.append((item, answer, correct))

    if st.button("제출하기"):
        score = 0

        for item, answer, correct in answers:
            if answer == correct:
                score += 1
                st.success(f"✅ {item['collocation']}")
            else:
                st.error(f"❌ {item['collocation']} → 정답: {correct}")
                st.session_state.wrong_items.append(item)

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
elif mode == "4. Review Wrong Answers":

    st.subheader("🔁 Review Wrong Answers")

    if not st.session_state.wrong_items:
        st.info("아직 오답이 없습니다.")

    else:
        for row in st.session_state.wrong_items:

            with st.container():
                st.markdown(f"### {row['collocation']}")
                st.write(f"**뜻:** {row['meaning_ko']}")
                st.write(f"**예문:** {row['example_sentence']}")
                st.divider()

        if st.button("오답 초기화"):
            st.session_state.wrong_items = []
            st.rerun()
