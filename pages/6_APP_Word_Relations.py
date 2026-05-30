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
section[data-testid="stSidebar"] a,
section[data-testid="stSidebar"] a span,
section[data-testid="stSidebar"] a p {
    font-size: 20px !important;
    font-weight: 500 !important;
}

div[role="radiogroup"] label {
    font-size: 24px !important;
    font-weight: 500 !important;
}

.word-card {
    background-color:#f7f9fc;
    padding:24px;
    border-radius:18px;
    border:1px solid #d6e4ff;
    margin-bottom:20px;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<h1 style='text-align:center; font-size:36px; margin-bottom:5px;'>
📘 APP Word Relations
</h1>

<p style='text-align:center; font-size:18px; color:#555;'>
다의어 · 유의어 · 반의어 학습 앱
</p>
""", unsafe_allow_html=True)

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
        "order", "category", "word", "part_of_speech",
        "meaning_in_context",
        "related_word", "relation_meaning", "note"
    ]

    missing = [c for c in required if c not in df.columns]
    if missing:
        st.error(f"빠진 컬럼: {missing}")
        st.stop()

    df = df.fillna("")
    df = df.sort_values("order").reset_index(drop=True)
    return df

df = load_data()

# ---------- Session ----------
if "word_relation_wrong_items" not in st.session_state:
    st.session_state.word_relation_wrong_items = []

if "word_meaning_quiz_items" not in st.session_state:
    st.session_state.word_meaning_quiz_items = []

if "word_relation_quiz_items" not in st.session_state:
    st.session_state.word_relation_quiz_items = []

st.title("📘 Word Relations Practice")
st.write("다의어 · 반의어 · 유의어를 학습하고 퀴즈로 확인하는 앱입니다.")

# ---------- Learning Settings ----------
st.header("⚙️ 학습 설정")

mode = st.radio(
    "메뉴 선택",
    [
        "1. Learn",
        "2. Meaning Test",
        "3. Relation Test",
        "4. Review Wrong Answers"
    ],
    index=None
)

category = st.selectbox(
    "학습 범위",
    ["전체"] + list(df["category"].unique())
)

if category == "전체":
    filtered_df = df.copy()
else:
    filtered_df = df[df["category"] == category].copy()

if mode is None:
    st.info("학습 메뉴를 선택해 주세요.")

# ==========================================
# 1. Learn
# ==========================================
elif mode == "1. Learn":

    st.header("📖 Learn")
    st.write(f"현재 학습 항목 수: **{len(filtered_df)}개**")

    for _, row in filtered_df.iterrows():
        st.markdown(
            f"""
            <div class="word-card">
                <div style='color:#1d4ed8; font-size:28px; font-weight:800; margin-bottom:14px;'>
                    {row['order']}. {row['word']}
                </div>
                <div style='font-size:20px; margin-bottom:10px;'>
                    <b>분류:</b> {row['category']}
                </div>
                <div style='font-size:20px; margin-bottom:10px;'>
                    <b>뜻:</b> {row['meaning_in_context']}
                </div>
                <div style='font-size:18px; color:#555;'>
                    <b>관련어:</b> {row['related_word']} {row['relation_meaning']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ==========================================
# 2. Meaning Test
# ==========================================
elif mode == "2. Meaning Test":

    st.subheader("📝 Meaning Test")

    quiz_size = st.selectbox(
        "문항 수",
        [5, 10, 15, 20],
        index=1
    )

    if st.button("새 Meaning Test 시작"):

        quiz_df = filtered_df.sample(
            min(quiz_size, len(filtered_df))
        )

        quiz_items = []

        for _, row in quiz_df.iterrows():

            correct = row["meaning_in_context"]

            wrong_pool = df[
                df["meaning_in_context"] != correct
            ]["meaning_in_context"].dropna().unique().tolist()

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

            item = row.to_dict()
            item["options"] = options
            quiz_items.append(item)

        st.session_state.word_meaning_quiz_items = quiz_items

    if not st.session_state.word_meaning_quiz_items:
        st.warning("먼저 '새 Meaning Test 시작' 버튼을 눌러 주세요.")
        st.stop()

    answers = []

    for i, item in enumerate(st.session_state.word_meaning_quiz_items, start=1):

        answer = st.radio(
            f"Q{i}. {item['word']}",
            item["options"],
            index=None,
            key=f"word_meaning_{i}"
        )

        answers.append((item, answer, item["meaning_in_context"]))

    if st.button("제출하기"):

        score = 0

        for item, answer, correct in answers:

            if answer == correct:
                score += 1
                st.success(f"✅ {item['word']} = {correct}")
            else:
                st.error(f"❌ {item['word']} / 정답: {correct}")
                st.session_state.word_relation_wrong_items.append(item)

        st.markdown(f"## 점수: {score} / {len(answers)}")

# ==========================================
# 3. Relation Test
# ==========================================
elif mode == "3. Relation Test":

    st.subheader("🔗 Relation Test")

    relation_df = filtered_df[
        filtered_df["category"].isin(["반의어", "유의어"])
    ].copy()

    if relation_df.empty:
        st.warning("Relation Test는 반의어와 유의어에서만 사용할 수 있습니다.")
        st.stop()

    quiz_size = st.selectbox(
        "문항 수",
        [5, 10, 15, 20],
        index=1
    )

    if st.button("새 Relation Test 시작"):

        quiz_df = relation_df.sample(
            min(quiz_size, len(relation_df))
        )

        quiz_items = []

        for _, row in quiz_df.iterrows():

            correct = row["related_word"]

            wrong_pool = relation_df[
                relation_df["related_word"] != correct
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

            item = row.to_dict()
            item["options"] = options
            quiz_items.append(item)

        st.session_state.word_relation_quiz_items = quiz_items

    if not st.session_state.word_relation_quiz_items:
        st.warning("먼저 '새 Relation Test 시작' 버튼을 눌러 주세요.")
        st.stop()

    answers = []

    for i, item in enumerate(st.session_state.word_relation_quiz_items, start=1):

        answer = st.radio(
            f"Q{i}. {item['word']}의 {item['category']}는?",
            item["options"],
            index=None,
            key=f"word_relation_{i}"
        )

        answers.append((item, answer, item["related_word"]))

    if st.button("채점하기"):

        score = 0

        for item, answer, correct in answers:

            if answer == correct:
                score += 1
                st.success(f"✅ {item['word']} → {correct}")
            else:
                st.error(f"❌ {item['word']} / 정답: {correct}")
                st.session_state.word_relation_wrong_items.append(item)

        st.markdown(f"## 점수: {score} / {len(answers)}")

# ==========================================
# 4. Review Wrong Answers
# ==========================================
elif mode == "4. Review Wrong Answers":

    st.subheader("🔁 Review Wrong Answers")

    if not st.session_state.word_relation_wrong_items:
        st.info("아직 오답이 없습니다.")

    else:
        st.write(f"현재 오답 수: **{len(st.session_state.word_relation_wrong_items)}개**")

        for item in st.session_state.word_relation_wrong_items:

            st.markdown(f"### {item['word']}")
            st.write(f"**분류:** {item['category']}")
            st.write(f"**뜻:** {item['meaning_in_context']}")
            st.write(f"**관련어:** {item['related_word']} {item['relation_meaning']}")
            st.divider()

        if st.button("오답 초기화"):
            st.session_state.word_relation_wrong_items = []
            st.rerun()
