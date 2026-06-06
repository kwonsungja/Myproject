import streamlit as st
import pandas as pd
import random
from pathlib import Path

# ==========================================
# Word Relations App
# ==========================================

st.set_page_config(
    page_title="Word Relations",
    page_icon="📘",
    layout="wide"
)

# ---------- Style ----------
st.markdown("""
<style>

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
    background-color:#f7f9fc;
    padding:20px;
    border-radius:16px;
    border:1px solid #d6e4ff;
    margin-bottom:14px;
}

.guided-card {
    background-color:#f3f8ff;
    padding:20px;
    border-radius:16px;
    border:1px solid #cfe3ff;
    margin-bottom:14px;
}

.review-card {
    background-color:#f7fff4;
    padding:20px;
    border-radius:16px;
    border:1px solid #cdebc3;
    margin-bottom:14px;
}

.word-title {
    font-size:26px;
    font-weight:800;
    color:#1d4ed8;
}

.meaning-text {
    font-size:19px;
    color:#222;
    margin-top:6px;
}

.example-text {
    font-size:17px;
    color:#444;
    margin-top:8px;
}

.tip-text {
    font-size:16px;
    color:#666;
    margin-top:6px;
}

.question-text {
    font-size:26px !important;
    font-weight:700 !important;
    margin-top:24px;
    margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<h1 style='text-align:center; font-size:36px; margin-bottom:10px;'>
📘 APP Word Relations (Grade 1)
</h1>

<div style='text-align:center; font-size:18px; color:#555; line-height:1.8;'>

Learn polysemy, synonyms, and antonyms through meaning, relation, guided practice, and review.
<br>
공통영어1 · 다의어 · 유의어 · 반의어를 문맥 속에서 학습하는 고등학교 1학년용 어휘 관계 앱입니다.

</div>
""", unsafe_allow_html=True)

# ---------- Load Data ----------
CSV_FILE = "grade1_word_relations_integrated_updated.csv"

@st.cache_data
def load_data():

    path1 = Path(CSV_FILE)
    path2 = Path("data") / CSV_FILE

    if path1.exists():
        df = pd.read_csv(path1)
    elif path2.exists():
        df = pd.read_csv(path2)
    else:
        st.error(f"{CSV_FILE} 파일을 찾을 수 없습니다.")
        st.stop()

    required = [
        "order",
        "category",
        "word",
        "part_of_speech",
        "meaning_in_context",
        "related_word",
        "relation_meaning",
        "note"
    ]

    missing = [c for c in required if c not in df.columns]

    if missing:
        st.error(f"빠진 컬럼: {missing}")
        st.stop()

    df = df.fillna("")
    df = df.sort_values("order").reset_index(drop=True)

    return df


df = load_data()

# ---------- Session State ----------
if "word_relation_wrong_items" not in st.session_state:
    st.session_state.word_relation_wrong_items = []

if "word_guided_items" not in st.session_state:
    st.session_state.word_guided_items = []

if "word_check_items" not in st.session_state:
    st.session_state.word_check_items = []

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

category = st.selectbox(
    "학습 범위",
    ["전체"] + list(df["category"].unique())
)

if category == "전체":
    filtered_df = df.copy()
else:
    filtered_df = df[df["category"] == category].copy()

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
    st.info("목표: 다의어, 유의어, 반의어의 의미와 관련어를 먼저 이해합니다.")

    st.write(f"현재 학습 항목 수: **{len(filtered_df)}개**")

    if filtered_df.empty:
        st.warning("선택한 범위에 해당하는 항목이 없습니다.")
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

            <div class="word-title">
            {int(row['order'])}. {row['word']}
            </div>

            <div class="meaning-text">
            분류: {row['category']}
            </div>

            <div class="meaning-text">
            품사: {row['part_of_speech']}
            </div>

            <div class="meaning-text">
            뜻: {row['meaning_in_context']}
            </div>

            <div class="tip-text">
            관련어: {row['related_word']} {row['relation_meaning']}
            </div>

            <div class="tip-text">
            💡 Note: {row['note']}
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
    st.info("목표: 힌트를 보면서 단어의 의미와 관련어를 확인합니다.")

    if filtered_df.empty:
        st.warning("선택한 범위에 해당하는 항목이 없습니다.")
        st.stop()

    practice_size = st.selectbox(
        "연습 문항 수",
        [5, 10, 15],
        index=0
    )

    practice_type = st.radio(
        "연습 유형",
        ["뜻 확인", "관련어 확인"],
        index=0
    )

    if st.button("새 Guided Practice 시작"):

        guided_items = filtered_df.sample(
            min(practice_size, len(filtered_df)),
            random_state=random.randint(1, 100000)
        ).to_dict("records")

        for item in guided_items:

            if practice_type == "뜻 확인":

                correct = item["meaning_in_context"]

                wrong_pool = df[
                    df["meaning_in_context"] != correct
                ]["meaning_in_context"].dropna().unique().tolist()

            else:

                correct = item["related_word"]

                wrong_pool = df[
                    df["related_word"] != correct
                ]["related_word"].dropna().unique().tolist()

            wrong_pool = [
                x for x in wrong_pool
                if str(x).strip() != ""
            ]

            wrongs = random.sample(
                wrong_pool,
                min(2, len(wrong_pool))
            )

            options = wrongs + [correct]
            random.shuffle(options)

            item["options"] = options
            item["practice_type"] = practice_type

        st.session_state.word_guided_items = guided_items

    if st.session_state.word_guided_items:

        answers = []

        for i, item in enumerate(st.session_state.word_guided_items, start=1):

            st.markdown(
                f"""
                <div class="guided-card">

                <div class="word-title">
                Q{i}. {item['word']}
                </div>

                <div class="tip-text">
                분류: {item['category']}
                </div>

                <div class="tip-text">
                💡 Hint: {item['note']}
                </div>

                <div class="tip-text">
                관련 정보: {item['related_word']} {item['relation_meaning']}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            if item["practice_type"] == "뜻 확인":
                question_label = "뜻을 고르세요."
                correct = item["meaning_in_context"]
            else:
                question_label = f"{item['category']}에 해당하는 관련어를 고르세요."
                correct = item["related_word"]

            answer = st.radio(
                question_label,
                item["options"],
                index=None,
                key=f"word_guided_{i}"
            )

            answers.append((item, answer, correct))

        if st.button("Guided Practice 확인"):

            for item, answer, correct in answers:

                if answer == correct:

                    st.success(
                        f"정답입니다: {item['word']} = {correct}"
                    )

                else:

                    st.warning(
                        f"다시 확인해 보세요. 정답은 '{correct}'입니다."
                    )

# ==========================================
# 3. Practice Check
# ==========================================
elif mode == "✅ Practice Check":

    st.subheader("✅ Practice Check")
    st.info("목표: 힌트 없이 단어의 의미 또는 관련어를 스스로 확인합니다.")

    if filtered_df.empty:
        st.warning("선택한 범위에 해당하는 항목이 없습니다.")
        st.stop()

    quiz_size = st.selectbox(
        "문항 수",
        [5, 10, 15, 20],
        index=1
    )

    check_type = st.radio(
        "확인 유형",
        ["뜻 확인", "관련어 확인"],
        index=0
    )

    if st.button("새 Practice Check 시작"):

        if check_type == "관련어 확인":

            check_df = filtered_df[
                filtered_df["category"].isin(["반의어", "유의어"])
            ].copy()

            if check_df.empty:
                st.warning("관련어 확인은 반의어와 유의어에서만 사용할 수 있습니다.")
                st.stop()

        else:
            check_df = filtered_df.copy()

        quiz_items = check_df.sample(
            min(quiz_size, len(check_df)),
            random_state=random.randint(1, 100000)
        ).to_dict("records")

        for item in quiz_items:

            if check_type == "뜻 확인":

                correct = item["meaning_in_context"]

                wrong_pool = df[
                    df["meaning_in_context"] != correct
                ]["meaning_in_context"].dropna().unique().tolist()

            else:

                correct = item["related_word"]

                wrong_pool = df[
                    df["related_word"] != correct
                ]["related_word"].dropna().unique().tolist()

            wrong_pool = [
                x for x in wrong_pool
                if str(x).strip() != ""
            ]

            wrongs = random.sample(
                wrong_pool,
                min(3, len(wrong_pool))
            )

            options = wrongs + [correct]
            random.shuffle(options)

            item["options"] = options
            item["check_type"] = check_type

        st.session_state.word_check_items = quiz_items

    if st.session_state.word_check_items:

        answers = []

        for i, item in enumerate(st.session_state.word_check_items, start=1):

            if item["check_type"] == "뜻 확인":
                question = f"Q{i}. {item['word']}"
                correct = item["meaning_in_context"]
                label = "뜻을 고르세요."
            else:
                question = f"Q{i}. {item['word']}의 {item['category']}는?"
                correct = item["related_word"]
                label = "관련어를 고르세요."

            st.markdown(
                f"<div class='question-text'>{question}</div>",
                unsafe_allow_html=True
            )

            answer = st.radio(
                label,
                item["options"],
                index=None,
                key=f"word_check_{i}"
            )

            answers.append((item, answer, correct))

        if st.button("Practice Check 제출"):

            score = 0

            for item, answer, correct in answers:

                if answer == correct:

                    score += 1
                    st.success(f"✅ {item['word']} = {correct}")

                else:

                    st.error(f"❌ {item['word']} → 정답: {correct}")
                    st.write(f"분류: {item['category']}")
                    st.write(f"뜻: {item['meaning_in_context']}")
                    st.write(f"관련어: {item['related_word']} {item['relation_meaning']}")

                    if item not in st.session_state.word_relation_wrong_items:
                        st.session_state.word_relation_wrong_items.append(item)

            st.markdown(f"## 점수: {score} / {len(answers)}")

# ==========================================
# 4. Review
# ==========================================
else:

    st.subheader("🔁 Review")
    st.info("목표: 틀린 단어 관계를 다시 복습하며 장기 기억으로 연결합니다.")

    if not st.session_state.word_relation_wrong_items:

        st.success("아직 오답이 없습니다. Practice Check를 먼저 풀어 보세요.")

    else:

        st.write(f"현재 오답 수: **{len(st.session_state.word_relation_wrong_items)}개**")

        for item in st.session_state.word_relation_wrong_items:

            st.markdown(
                f"""
                <div class="review-card">

                <div class="word-title">
                {item['word']}
                </div>

                <div class="meaning-text">
                분류: {item['category']}
                </div>

                <div class="meaning-text">
                뜻: {item['meaning_in_context']}
                </div>

                <div class="tip-text">
                관련어: {item['related_word']} {item['relation_meaning']}
                </div>

                <div class="tip-text">
                💡 Note: {item['note']}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        if st.button("오답 초기화"):

            st.session_state.word_relation_wrong_items = []

            st.rerun()

# ---------- Footer ----------
st.divider()
st.caption("Designed for Grade 1 word relations learning.")
