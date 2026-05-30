import streamlit as st
import pandas as pd
import random
from pathlib import Path

# ==========================================
# Grade 1 Common English Phrasal Verbs App
# ==========================================

# ---------- Page Config ----------
st.set_page_config(
    page_title="Grade 1 Phrasal Verbs",
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
📘 APP Phrasal Verbs
</h1>

<p style='text-align:center; font-size:18px; color:#555;'>
공통영어1 · 공통영어2 구동사 학습 앱<br>
동사와 전치사의 결합 표현을 학습하는 앱

</p>
""", unsafe_allow_html=True)
# ---------- Style ----------
st.markdown(
    """
    <style>
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
        font-size: 16px;
        color: #444;
        margin-top: 8px;
    }
    .tip-text {
        font-size: 15px;
        color: #666;
        margin-top: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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

# ---------- Header ----------
st.markdown('<div class="main-title">📘 Grade 1 Phrasal Verbs</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-text">공통영어1 · 공통영어2 · 구동사를 한 번에 학습하는 고등학교 1학년용 구동사 앱입니다.</div>',
    unsafe_allow_html=True
)
st.divider()

# ---------- Learning Settings ----------

st.header("⚙️ 학습 설정")

mode = st.radio(
    "메뉴 선택",
    ["1. Learn", "2. Quick Test", "3. Review Wrong Answers"],
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

lesson_options = ["전체"] + sorted(
    lesson_nums.unique()
)

selected_lesson = st.selectbox(
    "Lesson 선택",
    lesson_options
)

if selected_lesson != "전체":
    filtered_df = filtered_df[
        pd.to_numeric(
            filtered_df["lesson"],
            errors="coerce"
        ) == selected_lesson
    ]

items_per_page = st.slider(
    "한 번에 볼 표현 수",
    5,
    20,
    10
)

# ---------- Learn Mode ----------
if mode == "1. Learn":
    st.subheader("📖 Learn")
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
                <div class="tip-text">학습 팁: {row['learning_tip']}</div>
                <div class="tip-text">출처: {row['section']} / {row['textbook']} / {row['lesson']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.info("추천 학습 방법: 표현 → 뜻 → 예문 순서로 읽고, 마지막에 표현만 보고 뜻을 떠올려 보세요.")

# ---------- Quick Test Mode ----------
elif mode == "2. Quick Test":
    st.subheader("📝 Quick Test")

    if filtered_df.empty:
        st.warning("선택한 조건에 해당하는 표현이 없습니다.")
        st.stop()

    quiz_size = st.selectbox("문항 수", [5, 10, 15, 20], index=1)

    if "quiz_items" not in st.session_state:
        st.session_state.quiz_items = []

    if "wrong_items" not in st.session_state:
        st.session_state.wrong_items = []

    if st.button("새 테스트 시작"):
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

        st.session_state.quiz_items = quiz_items

    if not st.session_state.quiz_items:
        st.warning("먼저 '새 테스트 시작' 버튼을 눌러 주세요.")
        st.stop()

    answers = []

    for i, item in enumerate(st.session_state.quiz_items, start=1):
        st.markdown(f"### Q{i}. {item['phrasal_verb']}")
        st.caption(f"{item['section']} / {item['lesson']}")

        correct = item["korean_meaning"]
        options = item["options"]

        answer = st.radio(
            "뜻을 고르세요.",
            options,
            index=None,
            key=f"quiz_{i}"
        )

        answers.append((item, answer, correct))

    if st.button("제출하기"):
        score = 0
        wrong_now = []

        st.divider()
        st.subheader("결과")

        for item, answer, correct in answers:
            if answer == correct:
                score += 1
                st.success(f"✅ {item['phrasal_verb']} = {correct}")
            else:
                st.error(f"❌ {item['phrasal_verb']} | 선택: {answer} / 정답: {correct}")
                wrong_now.append(item)

        st.session_state.wrong_items.extend(wrong_now)
        st.session_state.wrong_items = list(
            {x['phrasal_verb']: x for x in st.session_state.wrong_items}.values()
        )

        st.markdown(f"## 점수: {score} / {len(answers)}")

# ---------- Review Wrong Answers ----------
else:
    st.subheader("🔁 Review Wrong Answers")

    if not st.session_state.wrong_items:
        st.success("아직 오답이 없습니다. Quick Test를 먼저 풀어 보세요.")
    else:
        st.write(f"현재 오답 표현 수: **{len(st.session_state.wrong_items)}개**")

        for item in st.session_state.wrong_items:
            st.markdown(
                f"""
                <div class="word-card">
                    <div class="phrasal-word">{item['phrasal_verb']}</div>
                    <div class="meaning-text">뜻: {item['korean_meaning']}</div>
                    <div class="example-text">예문: {item['example_sentence']}</div>
                    <div class="tip-text">학습 팁: {item['learning_tip']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        if st.button("오답 목록 초기화"):
            st.session_state.wrong_items = []
            st.rerun()

# ---------- Footer ----------
st.divider()
st.caption("Designed for Grade 1 Common English phrasal verb learning.")
