import streamlit as st
import pandas as pd
import random
from pathlib import Path

st.set_page_config(
    page_title="Word Relations",
    page_icon="📘",
    layout="wide"
)

CSV_FILE = "word_relations_polysemy_antonyms_synonyms.csv"

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
        "korean_meaning", "related_word", "relation_meaning", "note"
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

st.sidebar.header("학습 설정")

mode = st.sidebar.radio(
    "메뉴 선택",
    ["1. Learn", "2. Meaning Test", "3. Relation Test", "4. Review Wrong Answers"]
)

category = st.sidebar.selectbox(
    "학습 범위",
    ["전체"] + list(df["category"].unique())
)

if category == "전체":
    filtered_df = df.copy()
else:
    filtered_df = df[df["category"] == category].copy()

if "wrong_items" not in st.session_state:
    st.session_state.wrong_items = []

if mode == "1. Learn":
    st.subheader("📖 Learn")

    st.write(f"현재 학습 항목 수: **{len(filtered_df)}개**")

    for _, row in filtered_df.iterrows():
        relation_text = ""

        if row["category"] in ["반의어", "유의어"]:
            relation_text = f"<p><b>관련어:</b> {row['related_word']} ({row['relation_meaning']})</p>"

        st.markdown(f"""
        <div style="
            background-color:#f4f9ff;
            padding:18px;
            border-radius:15px;
            border:1px solid #cfe3ff;
            margin-bottom:12px;
        ">
            <h3 style="color:#0d47a1;">{row['order']}. {row['word']}</h3>
            <p><b>분류:</b> {row['category']}</p>
            <p><b>뜻:</b> {row['korean_meaning']}</p>
            {relation_text}
            <p style="color:#666;"><b>note:</b> {row['note']}</p>
        </div>
        """, unsafe_allow_html=True)

elif mode == "2. Meaning Test":
    st.subheader("📝 Meaning Test")

    quiz_size = st.selectbox("문항 수", [5, 10, 15, 20], index=1)
    quiz_df = filtered_df.sample(min(quiz_size, len(filtered_df)))

    answers = []

    for i, (_, row) in enumerate(quiz_df.iterrows(), start=1):
        correct = row["korean_meaning"]

        wrong_pool = df[df["korean_meaning"] != correct]["korean_meaning"].tolist()
        wrongs = random.sample(wrong_pool, min(3, len(wrong_pool)))

        options = wrongs + [correct]
        random.shuffle(options)

        answer = st.radio(
            f"Q{i}. {row['word']}",
            options,
            key=f"meaning_{i}"
        )

        answers.append((row, answer, correct))

    if st.button("제출하기"):
        score = 0

        for row, answer, correct in answers:
            if answer == correct:
                score += 1
                st.success(f"✅ {row['word']} = {correct}")
            else:
                st.error(f"❌ {row['word']} / 정답: {correct}")
                st.session_state.wrong_items.append(row.to_dict())

        st.markdown(f"## 점수: {score} / {len(answers)}")

elif mode == "3. Relation Test":
    st.subheader("🔗 Relation Test")

    relation_df = filtered_df[filtered_df["category"].isin(["반의어", "유의어"])]

    if relation_df.empty:
        st.warning("Relation Test는 반의어와 유의어에서만 사용할 수 있습니다.")
        st.stop()

    quiz_size = st.selectbox("문항 수", [5, 10, 15, 20], index=1)
    quiz_df = relation_df.sample(min(quiz_size, len(relation_df)))

    answers = []

    for i, (_, row) in enumerate(quiz_df.iterrows(), start=1):
        correct = row["related_word"]

        wrong_pool = relation_df[
            relation_df["related_word"] != correct
        ]["related_word"].tolist()

        wrongs = random.sample(wrong_pool, min(3, len(wrong_pool)))
        options = wrongs + [correct]
        random.shuffle(options)

        answer = st.radio(
            f"Q{i}. {row['word']}의 {row['category']}는?",
            options,
            key=f"relation_{i}"
        )

        answers.append((row, answer, correct))

    if st.button("채점하기"):
        score = 0

        for row, answer, correct in answers:
            if answer == correct:
                score += 1
                st.success(f"✅ {row['word']} → {correct}")
            else:
                st.error(f"❌ {row['word']} / 정답: {correct}")
                st.session_state.wrong_items.append(row.to_dict())

        st.markdown(f"## 점수: {score} / {len(answers)}")

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
                <p><b>뜻:</b> {item['korean_meaning']}</p>
                <p><b>관련어:</b> {item['related_word']} {item['relation_meaning']}</p>
            </div>
            """, unsafe_allow_html=True)

        if st.button("오답 초기화"):
            st.session_state.wrong_items = []
            st.rerun()
