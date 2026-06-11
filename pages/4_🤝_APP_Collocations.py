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

# ---------- Style ----------
st.markdown("""
<style>

/* 전체 기본 글자 */
html, body, [class*="css"] {
    font-size: 17px;
}

/* Sidebar menu text */
section[data-testid="stSidebar"] a,
section[data-testid="stSidebar"] a span,
section[data-testid="stSidebar"] a p {
    font-size: 18px !important;
    font-weight: 500 !important;
}

/* 메뉴 선택 라벨 */
div[data-testid="stRadio"] > label {
    font-size: 24px !important;
    font-weight: 700 !important;
}

/* 라디오 선택지 글자 */
div[role="radiogroup"] label p {
    font-size: 22px !important;
    font-weight: 500 !important;
}

/* selectbox, slider 라벨 */
label p {
    font-size: 19px !important;
    font-weight: 600 !important;
}

.word-card {
    background-color: #fff7f0;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #ffd2b8;
    margin-bottom: 14px;
}

.guided-card {
    background-color: #f3f8ff;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #cfe3ff;
    margin-bottom: 14px;
}

.review-card {
    background-color: #f7fff4;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #cdebc3;
    margin-bottom: 14px;
}

.collocation-word {
    font-size: 26px;
    font-weight: 800;
    color: #1565c0;
}

.meaning-text {
    font-size: 19px;
    color: #222;
    margin-top: 6px;
}

.example-text {
    font-size: 17px;
    color: #444;
    margin-top: 8px;
}

.tip-text {
    font-size: 16px;
    color: #666;
    margin-top: 6px;
}

</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<h1 style='text-align:center; font-size:36px; margin-bottom:10px;'>
📘 APP Collocations (Grade 1)
</h1>

<div style='text-align:center; font-size:18px; color:#555; line-height:1.8;'>

Learn collocations through meaning, context, guided practice, and review.
<br>
공통영어1 · 공통영어2 · 자연스러운 연어 표현을 문맥 속에서 학습하는 고등학교 1학년용 연어 앱입니다.

</div>
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

# ---------- Session ----------
if "collocation_wrong_items" not in st.session_state:
    st.session_state.collocation_wrong_items = []

if "collocation_guided_items" not in st.session_state:
    st.session_state.collocation_guided_items = []

if "collocation_check_items" not in st.session_state:
    st.session_state.collocation_check_items = []

# ---------- Learning Settings ----------
st.header("⚙️ 학습 설정")

mode = st.radio(
    "메뉴 선택",
    [
        "📘 Learn",
        "🧩 Guided Practice",
        "✅ Practice Check",
        "🔁 Review"
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

# ==========================================
# 1. Learn
# ==========================================
if mode == "📘 Learn":

    st.subheader("📘 Learn")
    st.info("목표: 연어의 의미와 자연스러운 사용을 먼저 이해합니다.")

    for _, row in filtered_df.iterrows():

        st.markdown(
            f"""
            <div class="word-card">

            <div class="collocation-word">
            {row['collocation']}
            </div>

            <div class="meaning-text">
            뜻: {row['meaning_ko']}
            </div>

            <div class="example-text">
            예문: {row['example_sentence']}
            </div>

            <div class="tip-text">
            <p>💡 학습 팁: {row['learning_tip']}</p>
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

# ==========================================
# 2. Guided Practice
# ==========================================
elif mode == "🧩 Guided Practice":

    st.subheader("🧩 Guided Practice")
    st.info("목표: 예문과 힌트를 보면서 자연스러운 연어 표현을 익힙니다.")

    practice_size = st.selectbox(
        "연습 문항 수",
        [5, 10, 15],
        index=0
    )

    if st.button("새 Guided Practice 시작"):

        guided_items = filtered_df.sample(
            min(practice_size, len(filtered_df)),
            random_state=random.randint(1, 100000)
        ).to_dict("records")

        for item in guided_items:

            correct = item["meaning_ko"]

            wrongs = df[
                df["meaning_ko"] != correct
            ]["meaning_ko"].dropna().unique().tolist()

            wrongs = random.sample(
                wrongs,
                min(2, len(wrongs))
            )

            options = wrongs + [correct]
            random.shuffle(options)

            item["options"] = options

        st.session_state.collocation_guided_items = guided_items

    if st.session_state.collocation_guided_items:

        answers = []

        for i, item in enumerate(
            st.session_state.collocation_guided_items,
            start=1
        ):

            st.markdown(
                f"""
                <div class="guided-card">

                <div class="collocation-word">
                Q{i}. {item['collocation']}
                </div>

                <div class="example-text">
                예문: {item['example_sentence']}
                </div>

                <div class="tip-text">
                💡 Hint: Think about words that naturally go together.
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            answer = st.radio(
                "💡 뜻을 고르세요.",
                item["options"],
                index=None,
                key=f"guided_{i}"
            )

            answers.append((item, answer))

# ==========================================
# 3. Practice Check
# ==========================================
elif mode == "✅ Practice Check":

    st.subheader("✅ Practice Check")
    st.info("목표: 힌트 없이 연어 표현을 스스로 확인합니다.")

    quiz_size = st.selectbox(
        "문항 수",
        [5, 10, 15, 20],
        index=1
    )

    if st.button("새 Practice Check 시작"):

        quiz_df = filtered_df.sample(
            min(quiz_size, len(filtered_df))
        )

        quiz_items = []

        for _, row in quiz_df.iterrows():

            correct = row["meaning_ko"]

            wrongs = df[
                df["meaning_ko"] != correct
            ]["meaning_ko"].dropna().unique().tolist()

            wrongs = random.sample(
                wrongs,
                min(3, len(wrongs))
            )

            options = wrongs + [correct]
            random.shuffle(options)

            item = row.to_dict()
            item["options"] = options

            quiz_items.append(item)

        st.session_state.collocation_check_items = quiz_items

    if st.session_state.collocation_check_items:

        answers = []

        for i, item in enumerate(
            st.session_state.collocation_check_items,
            start=1
        ):

            st.markdown(f"### Q{i}. {item['collocation']}")

            answer = st.radio(
                "💡 뜻을 고르세요.",
                item["options"],
                index=None,
                key=f"check_{i}"
            )

            answers.append((item, answer))

        if st.button("Practice Check 제출"):

            score = 0

            for item, answer in answers:

                correct = item["meaning_ko"]

                if answer == correct:

                    score += 1

                    st.success(
                        f"✅ {item['collocation']}"
                    )

                else:

                    st.error(
                        f"❌ {item['collocation']} → 정답: {correct}"
                    )

                    st.write(f"예문: {item['example_sentence']}")

                    if item not in st.session_state.collocation_wrong_items:
                        st.session_state.collocation_wrong_items.append(item)

            st.markdown(
                f"## 점수: {score} / {len(answers)}"
            )

            if score == len(answers):
                st.success("🎉 Perfect Score!")
                st.balloons()
# ==========================================
# 4. Review
# ==========================================
else:

    st.subheader("🔁 Review")
    st.info("목표: 틀린 연어 표현을 다시 복습하며 장기 기억으로 연결합니다.")

    if not st.session_state.collocation_wrong_items:

        st.success("아직 오답이 없습니다. Practice Check를 먼저 풀어 보세요.")

    else:

        for row in st.session_state.collocation_wrong_items:

            st.markdown(
                f"""
                <div class="review-card">

                <div class="collocation-word">
                {row['collocation']}
                </div>

                <div class="meaning-text">
                뜻: {row['meaning_ko']}
                </div>

                <div class="example-text">
                예문: {row['example_sentence']}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        if st.button("오답 초기화"):

            st.session_state.collocation_wrong_items = []

            st.rerun()

# ---------- Footer ----------
st.divider()
st.caption("Designed for Grade 1 Common English collocation learning.")
