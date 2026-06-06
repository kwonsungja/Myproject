import streamlit as st
import pandas as pd
import random
from pathlib import Path

# ==========================================
# Grade 1 Common English Phrasal Verbs App
# ==========================================

st.set_page_config(
    page_title="Grade 1 Phrasal Verbs",
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

.main-title {
    font-size: 34px;
    font-weight: 800;
    color: #ff6b35;
}

.sub-text {
    font-size: 17px;
    color: #555;
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

.phrasal-word {
    font-size: 26px;
    font-weight: 800;
    color: #e85d04;
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

# ---------- Data Loading ----------
@st.cache_data
def load_data():
    filename = "grade1_common1_common2_book_phrasal_verbs.csv"
    possible_files = [filename, f"data/{filename}"]

    file_path = None
    for f in possible_files:
        if Path(f).exists():
            file_path = f
            break

    if file_path is None:
        st.error(
            "CSV 파일을 찾을 수 없습니다. "
            "grade1_common1_common2_book_phrasal_verbs.csv 파일을 app.py와 같은 폴더 또는 data 폴더에 넣어 주세요."
        )
        st.stop()

    df = pd.read_csv(file_path)

    required_cols = [
        "source_order", "section", "grade", "textbook", "lesson",
        "phrasal_verb", "korean_meaning", "example_sentence",
        "chunk_type", "difficulty", "learning_tip", "source_note"
    ]

    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        st.error(f"CSV 컬럼명이 맞지 않습니다. 빠진 컬럼: {missing}")
        st.stop()

    for col in required_cols:
        df[col] = df[col].fillna("")

    df = df.sort_values("source_order").reset_index(drop=True)
    return df


df = load_data()

# ---------- Session State ----------
if "phrasal_quiz_items" not in st.session_state:
    st.session_state.phrasal_quiz_items = []

if "phrasal_wrong_items" not in st.session_state:
    st.session_state.phrasal_wrong_items = []

if "guided_items" not in st.session_state:
    st.session_state.guided_items = []

# ---------- Header ----------
st.markdown("""
<h1 style='text-align:center; font-size:36px; margin-bottom:10px;'>
📘 APP Phrasal Verbs (Grade 1)
</h1>

<div style='text-align:center; font-size:18px; color:#555; line-height:1.8;'>

Learn phrasal verbs through meaning, context, guided practice, and review.
<br>
공통영어1 · 공통영어2 · 구동사를 문맥 속에서 학습하는 고등학교 1학년용 구동사 앱입니다.

</div>
""", unsafe_allow_html=True)

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

lesson_nums = pd.to_numeric(
    filtered_df["lesson"],
    errors="coerce"
).dropna().astype(int)

lesson_options = ["전체"] + sorted(lesson_nums.unique())

selected_lesson = st.selectbox(
    "Lesson 선택",
    lesson_options
)

if selected_lesson != "전체":
    filtered_df = filtered_df[
        pd.to_numeric(filtered_df["lesson"], errors="coerce") == selected_lesson
    ]

items_per_page = st.slider(
    "한 번에 볼 표현 수",
    5,
    20,
    10
)

st.divider()

# ==========================================
# 1. Learn
# ==========================================
if mode == "📘 Learn":

    st.subheader("📘 Learn")
    st.info("목표: 구동사의 뜻, 예문, 학습 팁을 먼저 이해합니다.")

    st.write(f"현재 학습 항목 수: **{len(filtered_df)}개**")

    if filtered_df.empty:
        st.warning("선택한 조건에 해당하는 표현이 없습니다.")
        st.stop()

    total_pages = (len(filtered_df) - 1) // items_per_page + 1
    page = st.selectbox("학습 페이지 선택", list(range(1, total_pages + 1)))

    start = (page - 1) * items_per_page
    end = start + items_per_page
    page_df = filtered_df.iloc[start:end]

    for _, row in page_df.iterrows():
        st.markdown(
            f"""
            <div class="word-card">
                <div class="phrasal-word">{int(row['source_order'])}. {row['phrasal_verb']}</div>
                <div class="meaning-text">뜻: {row['korean_meaning']}</div>
                <div class="example-text">예문: {row['example_sentence']}</div>
                <div class="tip-text">💡 학습 팁: {row['learning_tip']}</div>
                <div class="tip-text">출처: {row['section']} / {row['textbook']} / Lesson {row['lesson']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.success("학습 방법: 표현 → 뜻 → 예문 → 학습 팁 순서로 읽고, 마지막에 표현만 보고 뜻을 떠올려 보세요.")

# ==========================================
# 2. Guided Practice
# ==========================================
elif mode == "🧩 Guided Practice":

    st.subheader("🧩 Guided Practice")
    st.info("목표: 힌트와 예문을 보면서 구동사의 의미를 확인합니다.")

    if filtered_df.empty:
        st.warning("선택한 조건에 해당하는 표현이 없습니다.")
        st.stop()

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
            correct = item["korean_meaning"]

            other_pool = df[
                df["korean_meaning"] != correct
            ]["korean_meaning"].dropna().unique().tolist()

            other_options = random.sample(
                other_pool,
                min(2, len(other_pool))
            )

            options = other_options + [correct]
            random.shuffle(options)

            item["options"] = options

        st.session_state.guided_items = guided_items

    if st.session_state.guided_items:

        answers = []

        for i, item in enumerate(st.session_state.guided_items, start=1):

            st.markdown(
                f"""
                <div class="guided-card">
                    <div class="phrasal-word">Q{i}. {item['phrasal_verb']}</div>
                    <div class="example-text">예문: {item['example_sentence']}</div>
                    <div class="tip-text">💡 Hint: {item['learning_tip']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            answer = st.radio(
                "뜻을 고르세요.",
                item["options"],
                index=None,
                key=f"guided_{i}"
            )

            answers.append((item, answer))
            
if st.button("Guided Practice 확인"):

    score = 0

    for item, answer in answers:

        if answer == item["korean_meaning"]:
            score += 1
            st.success(
                f"정답입니다: {item['phrasal_verb']} = {item['korean_meaning']}"
            )

        else:
            st.warning(
                f"다시 확인해 보세요. {item['phrasal_verb']}의 뜻은 '{item['korean_meaning']}'입니다."
            )

    if score == len(answers):
        st.success("🎉 Perfect Score!")
        st.balloons()
        
# ==========================================
# 3. Practice Check
# ==========================================
elif mode == "✅ Practice Check":

    st.subheader("✅ Practice Check")
    st.info("목표: 힌트 없이 스스로 구동사의 의미를 확인합니다.")

    if filtered_df.empty:
        st.warning("선택한 조건에 해당하는 표현이 없습니다.")
        st.stop()

    quiz_size = st.selectbox(
        "문항 수",
        [5, 10, 15, 20],
        index=1
    )

    if st.button("새 Practice Check 시작"):

        quiz_items = filtered_df.sample(
            min(quiz_size, len(filtered_df)),
            random_state=random.randint(1, 100000)
        ).to_dict("records")

        for item in quiz_items:

            correct = item["korean_meaning"]

            other_pool = df[
                df["korean_meaning"] != correct
            ]["korean_meaning"].dropna().unique().tolist()

            other_options = random.sample(
                other_pool,
                min(3, len(other_pool))
            )

            options = other_options + [correct]
            random.shuffle(options)

            item["options"] = options

        st.session_state.phrasal_quiz_items = quiz_items

    if st.session_state.phrasal_quiz_items:

        answers = []

        for i, item in enumerate(st.session_state.phrasal_quiz_items, start=1):

            st.markdown(f"### Q{i}. {item['phrasal_verb']}")
            st.caption(f"{item['section']} / {item['textbook']} / Lesson {item['lesson']}")

            answer = st.radio(
                "뜻을 고르세요.",
                item["options"],
                index=None,
                key=f"check_{i}"
            )

            answers.append((item, answer))

        if st.button("Practice Check 제출"):

            score = 0

            for item, answer in answers:

                correct = item["korean_meaning"]

                if answer == correct:
                    score += 1
                    st.success(f"정답: {item['phrasal_verb']} = {correct}")
                else:
                    st.error(f"오답: {item['phrasal_verb']} = {correct}")
                    st.write(f"예문: {item['example_sentence']}")
                    st.write(f"학습 팁: {item['learning_tip']}")

                    if item not in st.session_state.phrasal_wrong_items:
                        st.session_state.phrasal_wrong_items.append(item)

            st.subheader(f"점수: {score} / {len(answers)}")

# ==========================================
# 4. Review
# ==========================================
else:

    st.subheader("🔁 Review")
    st.info("목표: Practice Check에서 틀린 표현을 다시 보고 장기 기억으로 연결합니다.")

    if not st.session_state.phrasal_wrong_items:

        st.success("아직 오답이 없습니다. Practice Check를 먼저 풀어 보세요.")

    else:

        st.write(
            f"현재 오답 표현 수: **{len(st.session_state.phrasal_wrong_items)}개**"
        )

        for item in st.session_state.phrasal_wrong_items:

            st.markdown(
                f"""
                <div class="review-card">
                    <div class="phrasal-word">{item['phrasal_verb']}</div>
                    <div class="meaning-text">뜻: {item['korean_meaning']}</div>
                    <div class="example-text">예문: {item['example_sentence']}</div>
                    <div class="tip-text">💡 학습 팁: {item['learning_tip']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        if st.button("오답 목록 초기화"):

            st.session_state.phrasal_wrong_items = []

            st.rerun()

# ---------- Footer ----------
st.divider()
st.caption("Designed for Grade 1 Common English phrasal verb learning.")
