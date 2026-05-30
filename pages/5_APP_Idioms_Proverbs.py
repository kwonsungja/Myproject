import streamlit as st
import pandas as pd
import random
from pathlib import Path

# ==========================================
# Idioms & Proverbs App
# ==========================================

# ---------- Page Config ----------
st.set_page_config(
    page_title="Idioms & Proverbs",
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
📘 APP Idioms & Proverbs
</h1>

<p style='text-align:center; font-size:18px; color:#555;'>
관용표현 · 속담 학습 앱
</p>
""", unsafe_allow_html=True)

CSV_FILE = "idioms_proverbs_for_grade1.csv"

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

    required = ["order", "category", "expression", "korean_meaning", "cf_note"]
    missing = [c for c in required if c not in df.columns]

    if missing:
        st.error(f"빠진 컬럼: {missing}")
        st.stop()

    df = df.fillna("")
    df = df.sort_values("order").reset_index(drop=True)
    return df

df = load_data()

st.title("📘 Idioms & Proverbs Practice")
st.write("숙어와 속담을 학습하고 퀴즈로 확인하는 고등학교 영어 어휘 학습 앱입니다.")

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

if "wrong_items" not in st.session_state:
    st.session_state.wrong_items = []

# 1. Learn
if mode == "1. Learn":
    st.subheader("📖 Learn")

    st.write(f"현재 학습 항목 수: **{len(filtered_df)}개**")

    for _, row in filtered_df.iterrows():
        st.markdown(f"""
        <div style="
            background-color:#fff7f0;
            padding:18px;
            border-radius:15px;
            border:1px solid #ffd2b8;
            margin-bottom:12px;
        ">
            <h3 style="color:#e85d04;">{row['order']}. {row['expression']}</h3>
            <p style="font-size:18px;"><b>뜻:</b> {row['korean_meaning']}</p>
            <p style="color:#666;"><b>cf.</b> {row['cf_note']}</p>
            <p style="color:#888;"><b>분류:</b> {row['category']}</p>
        </div>
        """, unsafe_allow_html=True)

# 2. Meaning Test
elif mode == "2. Meaning Test":
    st.subheader("📝 Meaning Test")

    quiz_size = st.selectbox("문항 수", [5, 10, 15, 20], index=1)

    if len(filtered_df) == 0:
        st.warning("선택한 범위에 항목이 없습니다.")
        st.stop()

    quiz_df = filtered_df.sample(min(quiz_size, len(filtered_df)))

    answers = []

for i, (_, row) in enumerate(quiz_df.iterrows(), start=1):

    correct = row["korean_meaning"]

    wrong_pool = df[
        df["korean_meaning"] != correct
    ]["korean_meaning"].tolist()

    wrongs = random.sample(
        wrong_pool,
        min(3, len(wrong_pool))
    )

    options = wrongs + [correct]
    random.shuffle(options)

    answer = st.radio(
        f"Q{i}. {row['idiom_proverb']}",
        options,
        index=None,
        key=f"m_{i}"
    )

    answers.append((row, answer, correct))

    if st.button("제출하기"):
        score = 0

        for row, answer, correct in answers:
            if answer == correct:
                score += 1
                st.success(f"✅ {row['expression']} = {correct}")
            else:
                st.error(f"❌ {row['expression']} / 정답: {correct}")
                st.session_state.wrong_items.append(row.to_dict())

        st.markdown(f"## 점수: {score} / {len(answers)}")

# 3. Fill-in Test
elif mode == "3. Fill-in Test":
    st.subheader("✏️ Fill-in Test")

    quiz_size = st.selectbox("문항 수", [5, 10, 15], index=1)

    quiz_df = filtered_df.sample(min(quiz_size, len(filtered_df)))

    user_answers = []

    for i, (_, row) in enumerate(quiz_df.iterrows(), start=1):
        words = row["expression"].split()

        if len(words) >= 2:
            question = "_____ " + " ".join(words[1:])
            correct = words[0]
        else:
            question = "_____"
            correct = row["expression"]

        st.write(f"Q{i}. {question}")
        st.caption(f"뜻: {row['korean_meaning']}")

        answer = st.text_input("빈칸에 들어갈 단어", key=f"fill_{i}")

        user_answers.append((row, answer, correct))

    if st.button("채점하기"):
        score = 0

        for row, answer, correct in user_answers:
            if answer.strip().lower() == correct.lower():
                score += 1
                st.success(f"✅ {row['expression']}")
            else:
                st.error(f"❌ 정답: {row['expression']}")
                st.session_state.wrong_items.append(row.to_dict())

        st.markdown(f"## 점수: {score} / {len(user_answers)}")

# 4. Review
else:
    st.subheader("🔁 Review Wrong Answers")

    if not st.session_state.wrong_items:
        st.info("아직 오답이 없습니다.")
    else:
        for item in st.session_state.wrong_items:
            st.markdown(f"""
            <div style="
                background-color:#f4f9ff;
                padding:18px;
                border-radius:15px;
                border:1px solid #cfe3ff;
                margin-bottom:12px;
            ">
                <h3 style="color:#0d47a1;">{item['expression']}</h3>
                <p><b>뜻:</b> {item['korean_meaning']}</p>
                <p><b>cf.</b> {item['cf_note']}</p>
            </div>
            """, unsafe_allow_html=True)

        if st.button("오답 초기화"):
            st.session_state.wrong_items = []
            st.rerun()
