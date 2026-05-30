import streamlit as st
import pandas as pd
import random
from pathlib import Path

# ==========================================
# Textbook Reading App
# ==========================================

# ---------- Page Config ----------
st.set_page_config(
    page_title="Textbook Reading",
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

st.title("📘 Word Relations Practice")
st.write("다의어 · 반의어 · 유의어를 학습하고 퀴즈로 확인하는 앱입니다.")

# ---------- Learning Settings ----------

st.header("⚙️ 학습 설정")

mode = st.radio(
    "메뉴 선택",
    ["1. Learn", "2. Meaning Test", "3. Relation Test", "4. Review Wrong Answers"]
)

category = st.selectbox(
    "학습 범위",
    ["전체"] + list(df["category"].unique())
)

if category == "전체":
    filtered_df = df.copy()
else:
    filtered_df = df[df["category"] == category].copy()

if "wrong_items" not in st.session_state:
    st.session_state.wrong_items = []

# ==========================================
# 1. Learn
# ==========================================
if mode == "1. Learn":

    st.header("📖 Learn")

    st.write(f"현재 학습 항목 수: {len(filtered_df)}개")

    for _, row in filtered_df.iterrows():

        st.markdown(
            f"""
<div style='background-color:#f7f9fc; padding:24px; border-radius:18px; border:1px solid #d6e4ff; margin-bottom:20px;'>

<div style='color:#1d4ed8; font-size:24px; font-weight:700; margin-bottom:14px;'>
{row['order']}. {row['word']}
</div>

<div style='font-size:18px; margin-bottom:10px;'>
<b>분류:</b> {row['category']}
</div>

<div style='font-size:17px;'>
<b>뜻:</b> {row['meaning_in_context']}
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

    if "meaning_quiz_items" not in st.session_state:
        st.session_state.meaning_quiz_items = []

    if st.button("새 Meaning Test 시작"):

        quiz_df = filtered_df.sample(
            min(quiz_size, len(filtered_df))
        )

        quiz_items = []

        for _, row in quiz_df.iterrows():

            correct = row["meaning_in_context"]

            wrong_pool = df[
                df["meaning_in_context"] != correct
            ]["meaning_in_context"].dropna().tolist()

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

        st.session_state.meaning_quiz_items = quiz_items

    if not st.session_state.meaning_quiz_items:

        st.warning(
            "먼저 '새 Meaning Test 시작' 버튼을 눌러 주세요."
        )

        st.stop()

    answers = []

    for i, item in enumerate(
        st.session_state.meaning_quiz_items,
        start=1
    ):

        answer = st.radio(
            f"Q{i}. {item['word']}",
            item["options"],
            index=None,
            key=f"meaning_{i}"
        )

        answers.append(
            (item, answer, item["meaning_in_context"])
        )

    if st.button("제출하기"):

        score = 0

        for item, answer, correct in answers:

            if answer == correct:

                score += 1

                st.success(
                    f"✅ {item['word']} = {correct}"
                )

            else:

                st.error(
                    f"❌ {item['word']} / 정답: {correct}"
                )

                st.session_state.wrong_items.append(
                    item
                )

        st.markdown(
            f"## 점수: {score} / {len(answers)}"
        )

else:
    st.subheader("🔁 Review Wrong Answers")

    if not st.session_state.wrong_items:
        st.info("아직 오답이 없습니다.")
    else:
        for item in st.session_state.wrong_items:
            st.markdown(f"""
            <div style="
                background-color:#fff7f0;
                padding:18px;
                border-radius:15px;
                border:1px solid #ffd2b8;
                margin-bottom:12px;
            ">
                <h3 style="color:#e85d04;">{item['word']}</h3>
                <p><b>분류:</b> {item['category']}</p>
                <p><b>뜻:</b> {item['meaning_in_context']}</p>
                <p><b>관련어:</b> {item['related_word']} {item['relation_meaning']}</p>
            </div>
            """, unsafe_allow_html=True)

        if st.button("오답 초기화"):
            st.session_state.wrong_items = []
            st.rerun()
